from .registry import HandlerRegistry
from .types import ActionResult, DispatchContext, ParsedCommand


def movement_handler(context: DispatchContext, command: ParsedCommand) -> ActionResult:
    destination = command.target
    return ActionResult(
        state_changes={"status": f"at:{destination}"},
        narration=f"{context.session_name} moves toward {destination}.",
    )


def interaction_handler(context: DispatchContext, command: ParsedCommand) -> ActionResult:
    subject = command.target
    return ActionResult(
        state_changes={"last_interaction": subject},
        narration=f"{context.session_name} interacts with {subject}.",
    )


def inventory_use_handler(context: DispatchContext, command: ParsedCommand) -> ActionResult:
    item = command.target
    return ActionResult(
        state_changes={"last_item_used": item},
        narration=f"{context.session_name} uses {item}.",
    )


def mission_progress_handler(context: DispatchContext, command: ParsedCommand) -> ActionResult:
    mission = command.target or "current mission"
    return ActionResult(
        state_changes={"last_mission_update": mission},
        narration=f"Mission progress has been updated for {mission}.",
    )


def build_default_registry() -> HandlerRegistry:
    registry = HandlerRegistry()
    registry.register("move", movement_handler)
    registry.register("interact", interaction_handler)
    registry.register("use", inventory_use_handler)
    registry.register("progress", mission_progress_handler)
    return registry
