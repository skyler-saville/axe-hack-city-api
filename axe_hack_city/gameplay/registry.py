from typing import Callable, Dict, Optional

from .types import ActionResult, DispatchContext, ParsedCommand

ActionHandler = Callable[[DispatchContext, ParsedCommand], ActionResult]


class HandlerRegistry:
    def __init__(self) -> None:
        self._handlers: Dict[str, ActionHandler] = {}

    def register(self, verb: str, handler: ActionHandler) -> None:
        self._handlers[verb] = handler

    def resolve(self, verb: str) -> Optional[ActionHandler]:
        return self._handlers.get(verb)
