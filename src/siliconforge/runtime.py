"""SiliconForge A0 local reference, not an authenticated network service or real EDA.

IMPORTANT: A1 must add verified actor identity, ACLs, artifact checks, secure EDA
execution and complete acceptance tests BEFORE serving external requests.
"""
from __future__ import annotations
import hashlib
import json
import sqlite3
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

OWNER_SET = frozenset({
    "spec", "rtl", "verification", "formal", "ppa", "integration",
    "environment", "improvement", "human_interface"
})
ROUTES = {
    "SPEC.CHANGED": ("spec",), "SPEC.ACCEPTED": ("rtl", "verification", "formal"),
    "RTL.CHANGED": ("rtl",),
    "RTL.CANDIDATE_READY": ("verification", "formal", "ppa"),
    "SIM.FAILED": ("verification",), "SIM.REGRESSION_FAILED": ("verification",),
    "SIM.PASSED": ("verification", "integration"),
    "FORMAL.FAILED": ("formal",), "FORMAL.PASSED": ("formal", "integration"),
    "PPA.TARGET_CHANGED": ("ppa",), "PPA.TARGET_CHANGE": ("ppa",),
    "SYNTH.COMPLETE": ("ppa",), "ENV.DRIFT": ("environment",),
    "ENV.PROFILE_READY": ("environment",), "GATE.CHECK_REQUESTED": ("integration",),
    "IMPROVEMENT.REVIEW_DUE": ("improvement",),
    "PEER.RTL_REPAIR_REQUESTED": ("rtl",), "HUMAN.MESSAGE": ("human_interface",)
}
class InvalidEvent(ValueError): pass
class IdempotencyConflict(InvalidEvent): pass
class LeaseConflict(RuntimeError): pass

@dataclass(frozen=True)
class Delivery:
    delivery_id: str
    event_id: str
    event_type: str
    project_id: str
    owner_id: str
    attempt: int
    lease_token: str
    payload: dict[str, Any]
    correlation_id: str
    causation_id: str | None

def _id() -> str: return str(uuid.uuid4())
def _utc() -> str: return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00","Z")
def _json(x: Any) -> str: return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(",",":"),allow_nan=False)

class EventStore:
    """Single-process SQLite WAL reference. No real models, EDA or source authentication."""
    def __init__(self, database: str | Path = ":memory:", max_attempts: int = 3):
        if max_attempts < 1: raise ValueError("max_attempts must be >=1")
        self.max_attempts = max_attempts
        self.connection = sqlite3.connect(str(database), timeout=15, isolation_level=None)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA journal_mode=WAL")
        self.connection.execute("PRAGMA foreign_keys=ON")
        self.connection.executescript("""
        CREATE TABLE IF NOT EXISTS event_journal (
          seq INTEGER PRIMARY KEY AUTOINCREMENT, event_id TEXT NOT NULL UNIQUE,
          event_type TEXT NOT NULL, source TEXT NOT NULL, actor_id TEXT NOT NULL,
          project_id TEXT NOT NULL, correlation_id TEXT NOT NULL, causation_id TEXT,
          idempotency_key TEXT NOT NULL, mandate_id TEXT NOT NULL,
          payload_json TEXT NOT NULL, payload_sha256 TEXT NOT NULL,
          created_at_utc TEXT NOT NULL, UNIQUE(source,idempotency_key));
        CREATE TRIGGER IF NOT EXISTS forbid_event_update BEFORE UPDATE ON event_journal
          BEGIN SELECT RAISE(ABORT,'immutable event'); END;
        CREATE TRIGGER IF NOT EXISTS forbid_event_delete BEFORE DELETE ON event_journal
          BEGIN SELECT RAISE(ABORT,'immutable event'); END;
        CREATE TABLE IF NOT EXISTS deliveries(
          delivery_id TEXT PRIMARY KEY, event_id TEXT NOT NULL REFERENCES event_journal(event_id),
          owner_id TEXT NOT NULL, status TEXT NOT NULL CHECK(status IN
            ('READY','LEASED','ACKED','DEAD_LETTER')),
          attempt INTEGER NOT NULL DEFAULT 0, lease_token TEXT, leased_until REAL,
          last_error TEXT, UNIQUE(event_id,owner_id));
        CREATE INDEX IF NOT EXISTS ix_delivery ON deliveries(owner_id,status,leased_until);
        CREATE TABLE IF NOT EXISTS tickets(
          ticket_id TEXT PRIMARY KEY, project_id TEXT NOT NULL,
          owner_id TEXT NOT NULL, state TEXT NOT NULL,
          last_progress_signature TEXT, same_failure_count INTEGER NOT NULL DEFAULT 0,
          updated_at_utc TEXT NOT NULL, UNIQUE(project_id,owner_id));
        CREATE TABLE IF NOT EXISTS communication(
          message_id TEXT PRIMARY KEY, sender_owner TEXT NOT NULL,
          recipient_owner TEXT NOT NULL, project_id TEXT NOT NULL,
          ticket_id TEXT NOT NULL, expected_output TEXT NOT NULL,
          evidence_refs_json TEXT NOT NULL, event_id TEXT NOT NULL REFERENCES event_journal(event_id),
          status TEXT NOT NULL, created_at_utc TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS decisions(
          decision_id TEXT PRIMARY KEY, delivery_id TEXT NOT NULL,
          owner_id TEXT NOT NULL, outcome TEXT NOT NULL,
          evidence_refs_json TEXT NOT NULL, created_at_utc TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS audit(
          audit_id TEXT PRIMARY KEY, kind TEXT NOT NULL, object_id TEXT,
          detail_json TEXT NOT NULL, created_at_utc TEXT NOT NULL);
        """)
    def close(self): self.connection.close()
    def __enter__(self): return self
    def __exit__(self,*_): self.close()
    def _start(self): self.connection.execute("BEGIN IMMEDIATE")
    def _audit(self, kind, obj, detail):
        self.connection.execute("INSERT INTO audit VALUES(?,?,?,?,?)",
           (_id(),kind,obj,_json(detail),_utc()))
    def _insert(self, *, event_type, project_id, payload, idempotency_key,
                source, actor_id, mandate_id, correlation_id=None,
                causation_id=None, direct_owner=None):
        if not all((event_type,project_id,idempotency_key,source,actor_id,mandate_id)):
            raise InvalidEvent("missing identity, scope or idempotency")
        if not isinstance(payload,dict): raise InvalidEvent("payload must be object")
        canon=_json(payload)
        if len(canon.encode("utf8"))>65536: raise InvalidEvent("payload > 64 KiB")
        if direct_owner and direct_owner not in OWNER_SET:
            raise InvalidEvent("invalid direct owner")
        if direct_owner is None and event_type not in ROUTES:
            raise InvalidEvent("unknown event route: "+event_type)
        fp=hashlib.sha256(("\n".join((event_type,project_id,direct_owner or "ROUTED",canon))).encode()).hexdigest()
        old=self.connection.execute("SELECT * FROM event_journal WHERE source=? AND idempotency_key=?",
                                    (source,idempotency_key)).fetchone()
        if old:
            if old["payload_sha256"]!=fp or old["mandate_id"]!=mandate_id:
                raise IdempotencyConflict("idempotency key reused with different payload")
            return old["event_id"], False
        eid=_id()
        self.connection.execute("""INSERT INTO event_journal
             (event_id,event_type,source,actor_id,project_id,correlation_id,
              causation_id,idempotency_key,mandate_id,payload_json,payload_sha256,created_at_utc)
             VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
             (eid,event_type,source,actor_id,project_id,correlation_id or eid,
              causation_id,idempotency_key,mandate_id,canon,fp,_utc()))
        owners=(direct_owner,) if direct_owner else ROUTES[event_type]
        for owner in dict.fromkeys(owners):
            if owner not in OWNER_SET: raise InvalidEvent("invalid route owner")
            self.connection.execute("""INSERT INTO deliveries
               (delivery_id,event_id,owner_id,status) VALUES(?,?,?,'READY')""",
               (_id(),eid,owner))
            tid=f"{project_id}:{owner}"
            self.connection.execute("""INSERT OR IGNORE INTO tickets
               (ticket_id,project_id,owner_id,state,updated_at_utc)
               VALUES(?,?,?,'NEW',?)""",(tid,project_id,owner,_utc()))
        self._audit("EVENT_ACCEPTED",eid,{"recipients":owners,"type":event_type})
        return eid, True
    def ingest(self, *, event_type:str, project_id:str, payload:dict[str,Any],
               idempotency_key:str, source="local_test", actor_id="local_actor",
               mandate_id="a0_local_scope",correlation_id=None,causation_id=None)->str:
        """LOCAL TEST TRUST ONLY. Gateway MUST authenticate identity in A1."""
        try:
            self._start()
            eid,_=self._insert(event_type=event_type,project_id=project_id,
              payload=payload,idempotency_key=idempotency_key,
              source=source,actor_id=actor_id,mandate_id=mandate_id,
              correlation_id=correlation_id,causation_id=causation_id)
            self.connection.commit()
            return eid
        except IdempotencyConflict:
            if self.connection.in_transaction:self.connection.rollback()
            self._start()
            self._audit("IDEMPOTENCY_CONFLICT",idempotency_key,{"source":source})
            self.connection.commit()
            raise
        except Exception:
            if self.connection.in_transaction:self.connection.rollback()
            raise
    def claim(self, owner_id:str, *,worker_id:str,now:float|None=None,
              lease_seconds:int=60)->Delivery|None:
        if owner_id not in OWNER_SET or not worker_id or lease_seconds<=0:
            raise ValueError("invalid owner/worker/lease")
        now=time.time() if now is None else now
        try:
            self._start()
            row=self.connection.execute("""SELECT d.*,j.event_type,j.project_id,
              j.payload_json,j.correlation_id,j.causation_id
              FROM deliveries d JOIN event_journal j ON d.event_id=j.event_id
              JOIN tickets t ON t.project_id=j.project_id AND t.owner_id=d.owner_id
              WHERE d.owner_id=? AND d.attempt<? AND t.state NOT IN('BLOCKED','CANCELLED')
              AND (d.status='READY' OR (d.status='LEASED' AND d.leased_until<=?))
              ORDER BY j.seq LIMIT 1""",(owner_id,self.max_attempts,now)).fetchone()
            if row is None:
                self.connection.commit()
                return None
            token=_id()
            self.connection.execute("""UPDATE deliveries
              SET status='LEASED', attempt=attempt+1,lease_token=?,leased_until=?
              WHERE delivery_id=?""",(token,now+lease_seconds,row["delivery_id"]))
            self.connection.execute("UPDATE tickets SET state='ACTIVE',updated_at_utc=? WHERE ticket_id=?",
              (_utc(),f'{row["project_id"]}:{owner_id}'))
            self._audit("DELIVERY_CLAIMED",row["delivery_id"],{"worker":worker_id,"attempt":row["attempt"]+1})
            self.connection.commit()
            return Delivery(row["delivery_id"],row["event_id"],row["event_type"],
              row["project_id"],owner_id,row["attempt"]+1,token,
              json.loads(row["payload_json"]),row["correlation_id"],row["causation_id"])
        except Exception:
            if self.connection.in_transaction:self.connection.rollback()
            raise
    def _check(self,delivery_id,lease_token):
        row=self.connection.execute("""SELECT d.*,j.project_id FROM deliveries d
          JOIN event_journal j ON d.event_id=j.event_id WHERE d.delivery_id=?""",
          (delivery_id,)).fetchone()
        if not row or row["status"]!="LEASED" or row["lease_token"]!=lease_token:
            raise LeaseConflict("stale or unknown lease")
        return row
    def complete(self,delivery_id,lease_token,*,outcome,
                 evidence_refs=None,emitted=None)->list[str]:
        if not outcome or len(outcome)>120:raise ValueError("outcome required")
        try:
            self._start()
            row=self._check(delivery_id,lease_token)
            self.connection.execute("INSERT INTO decisions VALUES(?,?,?,?,?,?)",
              (_id(),delivery_id,row["owner_id"],outcome,_json({"refs":evidence_refs or []}),_utc()))
            child_ids=[]
            for i,item in enumerate(emitted or []):
                eid,_=self._insert(event_type=item["event_type"],project_id=row["project_id"],
                  payload=item.get("payload",{}),source=f'owner:{row["owner_id"]}',
                  actor_id=row["owner_id"],mandate_id=item.get("mandate_id","a0_local_scope"),
                  idempotency_key=item.get("idempotency_key",f'{delivery_id}:{i}:{item["event_type"]}'),
                  correlation_id=item.get("correlation_id"),causation_id=row["event_id"],
                  direct_owner=item.get("direct_owner"))
                child_ids.append(eid)
            self.connection.execute("""UPDATE deliveries
              SET status='ACKED',lease_token=NULL,leased_until=NULL WHERE delivery_id=?""",
              (delivery_id,))
            self.connection.execute("UPDATE tickets SET state='WAITING',updated_at_utc=? WHERE ticket_id=?",
              (_utc(),f'{row["project_id"]}:{row["owner_id"]}'))
            self._audit("DELIVERY_ACKED",delivery_id,{"outcome":outcome,"children":child_ids})
            self.connection.commit()
            return child_ids
        except Exception:
            if self.connection.in_transaction:self.connection.rollback()
            raise
    def fail(self,delivery_id,lease_token,reason,retryable=True)->str:
        try:
            self._start()
            row=self._check(delivery_id,lease_token)
            state="READY" if retryable and row["attempt"]<self.max_attempts else "DEAD_LETTER"
            self.connection.execute("""UPDATE deliveries SET status=?,lease_token=NULL,
               leased_until=NULL,last_error=? WHERE delivery_id=?""",
               (state,reason[:1000],delivery_id))
            self._audit("DELIVERY_FAILED",delivery_id,{"reason":reason[:300],"new_state":state})
            self.connection.commit()
            return state
        except Exception:
            if self.connection.in_transaction:self.connection.rollback()
            raise
    def request_peer(self,*,sender_owner,recipient_owner,project_id,ticket_id,
                     expected_output,evidence_refs,idempotency_key,causation_id=None)->str:
        if sender_owner not in OWNER_SET or recipient_owner not in OWNER_SET:
            raise InvalidEvent("invalid peer owner")
        if sender_owner==recipient_owner or not expected_output.strip() or not evidence_refs:
            raise InvalidEvent("peer requires distinct owner, output and evidence")
        try:
            self._start()
            payload={"sender":sender_owner,"recipient":recipient_owner,
                     "ticket_id":ticket_id,"expected_output":expected_output,
                     "evidence_refs":evidence_refs}
            eid,inserted=self._insert(event_type="PEER.REQUEST",project_id=project_id,
              payload=payload,source=f"peer:{sender_owner}",actor_id=sender_owner,
              idempotency_key=idempotency_key,mandate_id="a0_peer_scope",
              causation_id=causation_id,direct_owner=recipient_owner)
            if inserted:self.connection.execute("INSERT INTO communication VALUES(?,?,?,?,?,?,?,?,?,?)",
              (_id(),sender_owner,recipient_owner,project_id,ticket_id,expected_output,
               _json({"refs":evidence_refs}),eid,"OPEN",_utc()))
            self.connection.commit()
            return eid
        except Exception:
            if self.connection.in_transaction:self.connection.rollback()
            raise
    def record_failure_signature(self,project_id,owner_id,signature,max_repeats=2)->bool:
        if not signature or max_repeats<2:raise ValueError("invalid failure policy")
        try:
            self._start()
            tid=f"{project_id}:{owner_id}"
            row=self.connection.execute("SELECT * FROM tickets WHERE ticket_id=?",(tid,)).fetchone()
            if row is None:raise InvalidEvent("unknown domain ticket")
            count=row["same_failure_count"]+1 if row["last_progress_signature"]==signature else 1
            blocked=count>=max_repeats
            self.connection.execute("""UPDATE tickets SET last_progress_signature=?,
              same_failure_count=?,state=?,updated_at_utc=? WHERE ticket_id=?""",
              (signature,count,"BLOCKED" if blocked else row["state"],_utc(),tid))
            if blocked:self._audit("NO_PROGRESS_BLOCKED",tid,{"signature":signature,"count":count})
            self.connection.commit()
            return blocked
        except Exception:
            if self.connection.in_transaction:self.connection.rollback()
            raise
    def journal(self):return [dict(r) for r in self.connection.execute("SELECT * FROM event_journal ORDER BY seq")]
    def deliveries(self):return [dict(r) for r in self.connection.execute("SELECT * FROM deliveries ORDER BY rowid")]
    def tickets(self):return [dict(r) for r in self.connection.execute("SELECT * FROM tickets ORDER BY project_id,owner_id")]
    def messages(self):return [dict(r) for r in self.connection.execute("SELECT * FROM communication ORDER BY created_at_utc")]
    def audit(self):return [dict(r) for r in self.connection.execute("SELECT * FROM audit ORDER BY rowid")]
    def summary(self):
        return {"events":len(self.journal()),
          "deliveries_by_status":{s:self.connection.execute(
            "SELECT COUNT(*) FROM deliveries WHERE status=?",(s,)).fetchone()[0]
            for s in ("READY","LEASED","ACKED","DEAD_LETTER")},
          "tickets":self.tickets(),"peer_messages":len(self.messages()),
          "mode":"A0_LOCAL_MOCK_NO_AUTH_NO_EDA"}
