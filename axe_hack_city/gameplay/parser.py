from typing import List, Optional, Tuple

from .types import ParsedCommand, ValidationError

VERB_ALIASES = {
    "go": "move",
    "walk": "move",
    "run": "move",
    "move": "move",
    "talk": "interact",
    "speak": "interact",
    "inspect": "interact",
    "interact": "interact",
    "use": "use",
    "equip": "use",
    "consume": "use",
    "mission": "progress",
    "quest": "progress",
    "progress": "progress",
    "advance": "progress",
}

FILLER_WORDS = {"to", "at", "with", "on", "the", "a", "an"}


def parse_player_command(raw_input: str) -> Tuple[Optional[ParsedCommand], List[ValidationError]]:
    """Parse and validate raw player input into a structured command."""
    errors: List[ValidationError] = []
    normalized = raw_input.strip()

    if not normalized:
        return None, [ValidationError(field="input", message="Command input cannot be empty.")]

    tokens = [token.lower() for token in normalized.split()]
    raw_verb = tokens[0]
    verb = VERB_ALIASES.get(raw_verb)

    if verb is None:
        supported = ", ".join(sorted(set(VERB_ALIASES.values())))
        errors.append(
            ValidationError(
                field="verb",
                message=f"Unknown verb '{raw_verb}'. Supported verbs: {supported}.",
            )
        )
        return None, errors

    payload_tokens = [token for token in tokens[1:] if token not in FILLER_WORDS]
    target = payload_tokens[0] if payload_tokens else None
    args = payload_tokens[1:] if len(payload_tokens) > 1 else []

    if verb in {"move", "interact", "use"} and not target:
        errors.append(
            ValidationError(
                field="target",
                message=f"'{verb}' commands require a target.",
            )
        )

    return ParsedCommand(verb=verb, target=target, args=args), errors
