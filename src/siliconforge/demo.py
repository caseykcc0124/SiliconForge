"""Mock local event loop, not real RTL/EDA or LLM."""
import json
import tempfile
from pathlib import Path
from siliconforge.runtime import EventStore

def main():
    with tempfile.TemporaryDirectory() as tmp:
        with EventStore(Path(tmp)/"demo.sqlite") as s:
            s.ingest(event_type="SIM.FAILED",project_id="APB_CRC32",
              idempotency_key="run-001",payload={"seed":173,"waveform":"mock://wave1"})
            v=s.claim("verification",worker_id="mock_verifier")
            assert v is not None
            s.request_peer(sender_owner="verification",recipient_owner="rtl",
              project_id="APB_CRC32",ticket_id="APB_CRC32:verification",
              expected_output="Repair reset carryover",evidence_refs=["mock://wave1"],
              idempotency_key="peer-001",causation_id=v.event_id)
            s.complete(v.delivery_id,v.lease_token,outcome="MOCK: referred repro to RTL")
            r=s.claim("rtl",worker_id="mock_rtl")
            assert r is not None
            s.complete(r.delivery_id,r.lease_token,outcome="MOCK: candidate ready",
              emitted=[{"event_type":"RTL.CANDIDATE_READY","payload":{"revision":"FAKE_SHA_DEMO"}}])
            print(json.dumps(s.summary(),ensure_ascii=False,indent=2))
            print("IMPORTANT: mock only; no real agent/EDA or milestone verified")

if __name__=="__main__":main()
