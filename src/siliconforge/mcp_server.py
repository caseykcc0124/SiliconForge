"""LOCAL-DEV-ONLY A1 interface sketch. NOT authenticated; do not expose externally."""
from __future__ import annotations
import os
from pathlib import Path
from siliconforge.runtime import EventStore

def main():
    if os.getenv("SF_DEV_MODE")!="1":
        raise SystemExit("MCP DEV ONLY: set SF_DEV_MODE=1 in isolated local environment")
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:
        raise SystemExit("Install optional Python MCP SDK for local experiment") from exc
    db=Path(os.getenv("SF_DB","./local_dev_runtime.sqlite"))
    server=FastMCP("SiliconForge-DEV-NOT-FOR-PRODUCTION")
    @server.tool()
    def sf_get_status()->dict:
        """Read local A0 state. This is not a production gateway."""
        with EventStore(db) as store: return store.summary()
    @server.tool()
    def sf_submit_event(event_type:str,project_id:str,idempotency_key:str,payload:dict)->dict:
        """Insecure local test. Production MUST authenticate actor, mandate and scope."""
        with EventStore(db) as store:
            eid=store.ingest(event_type=event_type,project_id=project_id,
                             payload=payload,idempotency_key=idempotency_key,
                             source="mcp_local_dev",actor_id="INSECURE_DEV_ACTOR")
        return {"event_id":eid,"environment":"DEV_UNAUTHENTICATED_DO_NOT_DEPLOY"}
    server.run(transport="stdio")

if __name__=="__main__":main()
