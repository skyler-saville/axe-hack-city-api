from axe_hack_city.gameplay.dispatcher import resolve_command_handler
from axe_hack_city.gameplay.handlers import build_default_registry
from axe_hack_city.gameplay.parser import parse_player_command
from axe_hack_city.gameplay.types import ParsedCommand


def test_parse_player_command_maps_aliases_and_extracts_parts() -> None:
    command, errors = parse_player_command("go to market square")

    assert errors == []
    assert command is not None
    assert command.verb == "move"
    assert command.target == "market"
    assert command.args == ["square"]


def test_parse_player_command_requires_target_for_move() -> None:
    command, errors = parse_player_command("move")

    assert command is not None
    assert len(errors) == 1
    assert errors[0].field == "target"


def test_resolve_command_handler_returns_error_for_unregistered_verb() -> None:
    registry = build_default_registry()
    command = ParsedCommand(verb="custom", target="door", args=[])

    handler, resolve_errors = resolve_command_handler(command, registry)

    assert handler is None
    assert len(resolve_errors) == 1
    assert "No handler registered" in resolve_errors[0].message
