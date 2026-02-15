from typing import List, Optional, Tuple

from .registry import ActionHandler, HandlerRegistry
from .types import ActionResult, DispatchContext, ParsedCommand, ValidationError


def resolve_command_handler(
    command: ParsedCommand, registry: HandlerRegistry
) -> Tuple[Optional[ActionHandler], List[ValidationError]]:
    """Pure resolve step that maps a parsed command to a handler."""
    handler = registry.resolve(command.verb)
    if handler:
        return handler, []

    return None, [
        ValidationError(
            field="verb", message=f"No handler registered for verb '{command.verb}'."
        )
    ]


def dispatch_command(
    context: DispatchContext, command: ParsedCommand, registry: HandlerRegistry
) -> ActionResult:
    handler, resolve_errors = resolve_command_handler(command, registry)
    if resolve_errors or handler is None:
        return ActionResult(
            narration="Command could not be resolved.",
            errors=[error.message for error in resolve_errors],
        )

    return handler(context, command)
