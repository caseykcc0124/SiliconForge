"""Future A1/A3 adapter contract. Never tie Owner identity to human chat session."""
from __future__ import annotations
from typing import Any, AsyncIterator, Protocol, TypedDict

class OwnerContext(TypedDict):
    ticket_id: str
    owner_id: str
    mandate_id: str
    accepted_scope: dict[str, Any]
    skill_version: str
    model_policy_id: str
    worktree: str
    evidence_refs: list[str]
    input_event_ids: list[str]

class TurnHandle(Protocol):
    async def stream_events(self) -> AsyncIterator[dict[str,Any]]: ...
    async def cancel(self) -> None: ...
    async def snapshot(self) -> dict[str,Any]: ...
    async def usage(self) -> dict[str,Any]: ...

class HarnessAdapter(Protocol):
    async def start_or_resume(self, context:OwnerContext)->TurnHandle: ...
    async def health(self)->dict[str,Any]: ...
