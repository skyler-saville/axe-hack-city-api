from .adapters import GameplayStateAdapter
from .dispatcher import dispatch_command
from .handlers import build_default_registry
from .parser import parse_player_command
from .types import ActionResult


class GameplayService:
    def __init__(self, adapter: GameplayStateAdapter):
        self.adapter = adapter
        self.registry = build_default_registry()

    def execute(self, session_id: int, raw_input: str) -> ActionResult:
        parsed_command, parse_errors = parse_player_command(raw_input)
        if parse_errors:
            return ActionResult(
                narration="Unable to understand that command.",
                errors=[error.message for error in parse_errors],
            )

        if parsed_command is None:
            return ActionResult(
                narration="Unable to understand that command.",
                errors=["No command could be parsed."],
            )

        context = self.adapter.get_context(session_id)
        result = dispatch_command(context, parsed_command, self.registry)

        if result.success:
            self.adapter.apply_state_changes(session_id, result.state_changes)

        return result
