from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class ValidationError:
    field: str
    message: str


@dataclass(frozen=True)
class ParsedCommand:
    verb: str
    target: Optional[str]
    args: List[str]


@dataclass(frozen=True)
class DispatchContext:
    session_id: int
    session_name: str
    status: str


@dataclass
class ActionResult:
    state_changes: Dict[str, Any] = field(default_factory=dict)
    narration: str = ""
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    @property
    def success(self) -> bool:
        return not self.errors
