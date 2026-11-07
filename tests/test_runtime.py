import sqlite3
import tempfile
import unittest
from pathlib import Path
from siliconforge.runtime import EventStore, IdempotencyConflict, InvalidEvent, LeaseConflict

class RuntimeContractTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.db=Path(self.temp.name)/"test.sqlite"
        self.s=EventStore(self.db,max_attempts=3)
    def tearDown(self):
        self.s.close()
        self.temp.cleanup()
    def ingest(self,key="x",project="CRC",payload=None,event="SIM.FAILED"):
        return self.s.ingest(event_type=event,project_id=project,payload=payload or {},idempotency_key=key)
    def test_01_direct_sim_route_no_main(self):
        self.ingest(payload={"seed":1})
        self.assertEqual([d["owner_id"] for d in self.s.deliveries()],["verification"])
        self.assertIsNone(self.s.claim("human_interface",worker_id="main"))
    def test_02_idempotent_event(self):
        a=self.ingest(payload={"seed":1})
        b=self.ingest(payload={"seed":1})
        self.assertEqual(a,b)
        self.assertEqual(len(self.s.deliveries()),1)
    def test_03_idempotency_conflict_rejected(self):
        self.ingest(payload={"seed":1})
        with self.assertRaises(IdempotencyConflict):self.ingest(payload={"seed":2})
        self.assertEqual(len(self.s.journal()),1)
    def test_04_route_unknown(self):
        with self.assertRaises(InvalidEvent):self.ingest(event="UNKNOWN.UNDECLARED")
        self.assertEqual(self.s.journal(),[])
    def test_05_multi_recipient_outbox(self):
        self.ingest(event="RTL.CANDIDATE_READY",payload={"sha":"abc"})
        self.assertEqual({d["owner_id"] for d in self.s.deliveries()},{"verification","formal","ppa"})
    def test_06_crash_replay_unclaimed(self):
        a=self.ingest()
        self.s.close()
        self.s=EventStore(self.db)
        self.assertEqual(self.s.claim("verification",worker_id="v").event_id,a)
    def test_07_lease_fencing(self):
        self.ingest()
        old=self.s.claim("verification",worker_id="w1",now=1000,lease_seconds=10)
        self.assertIsNone(self.s.claim("verification",worker_id="w2",now=1009))
        new=self.s.claim("verification",worker_id="w2",now=1011,lease_seconds=10)
        self.assertNotEqual(old.lease_token,new.lease_token)
        with self.assertRaises(LeaseConflict):
            self.s.complete(old.delivery_id,old.lease_token,outcome="stale")
        self.s.complete(new.delivery_id,new.lease_token,outcome="accepted")
    def test_08_atomic_ack_and_child(self):
        self.ingest()
        d=self.s.claim("verification",worker_id="v")
        ids=self.s.complete(d.delivery_id,d.lease_token,outcome="ready",
                            emitted=[{"event_type":"RTL.CANDIDATE_READY","payload":{"sha":"abc"}}])
        self.assertEqual(len(ids),1)
        self.assertEqual(len(self.s.journal()),2)
        self.assertEqual({x["owner_id"] for x in self.s.deliveries()[1:]},{"verification","formal","ppa"})
    def test_09_invalid_child_rollback(self):
        self.ingest()
        d=self.s.claim("verification",worker_id="v")
        with self.assertRaises(InvalidEvent):
            self.s.complete(d.delivery_id,d.lease_token,outcome="oops",
                            emitted=[{"event_type":"UNKNOWN.INVALID","payload":{}}])
        self.assertEqual(self.s.deliveries()[0]["status"],"LEASED")
        self.assertEqual(len(self.s.journal()),1)
    def test_10_direct_peer_request(self):
        eid=self.s.request_peer(sender_owner="verification",recipient_owner="rtl",
            project_id="CRC",ticket_id="CRC:verification",expected_output="repair bug",
            evidence_refs=["waveform:1"],idempotency_key="peer1")
        self.assertEqual(len(self.s.messages()),1)
        self.assertEqual(self.s.claim("rtl",worker_id="r").event_id,eid)
        self.assertIsNone(self.s.claim("human_interface",worker_id="main"))
    def test_11_peer_evidence_required(self):
        with self.assertRaises(InvalidEvent):
            self.s.request_peer(sender_owner="verification",recipient_owner="rtl",
                project_id="CRC",ticket_id="CRC:verification",expected_output="repair",
                evidence_refs=[],idempotency_key="peer1")
    def test_12_blocked_project_does_not_stop_other(self):
        for p in ("CRC","AES"):self.ingest(key=p,project=p)
        self.assertFalse(self.s.record_failure_signature("CRC","verification","SAME"))
        self.assertTrue(self.s.record_failure_signature("CRC","verification","SAME"))
        self.assertEqual(self.s.claim("verification",worker_id="w").project_id,"AES")
    def test_13_bounded_deadletter(self):
        self.ingest()
        for i in range(3):
            d=self.s.claim("verification",worker_id="v",now=100+2*i,lease_seconds=1)
            self.assertIsNotNone(d)
            result=self.s.fail(d.delivery_id,d.lease_token,"synthetic failure",retryable=True)
        self.assertEqual(result,"DEAD_LETTER")
        self.assertIsNone(self.s.claim("verification",worker_id="v"))
    def test_14_immutable_events(self):
        self.ingest()
        with self.assertRaises(sqlite3.IntegrityError):
            self.s.connection.execute("UPDATE event_journal SET event_type='SIM.PASSED'")
        with self.assertRaises(sqlite3.IntegrityError):
            self.s.connection.execute("DELETE FROM event_journal")
    def test_15_idle_reawakening(self):
        self.ingest()
        d=self.s.claim("verification",worker_id="v")
        self.s.complete(d.delivery_id,d.lease_token,outcome="done")
        self.ingest(key="next",payload={"seed":9})
        self.assertIsNotNone(self.s.claim("verification",worker_id="v"))
    def test_16_unknown_owner(self):
        with self.assertRaises(ValueError):
            self.s.claim("random_superboss",worker_id="r")
    def test_17_oversized_payload(self):
        with self.assertRaises(InvalidEvent):
            self.ingest(payload={"body":"a"*70000})
    def test_18_audit_idempotency_conflict(self):
        self.ingest(payload={"seed":1})
        with self.assertRaises(IdempotencyConflict):self.ingest(payload={"seed":2})
        self.assertEqual(sum(a["kind"]=="IDEMPOTENCY_CONFLICT" for a in self.s.audit()),1)

if __name__=="__main__":
    unittest.main()
