from axe_hack_city.models.game_session_model import GameSession
from axe_hack_city.schemas.game_session_schema import GameStateTransitionSchema
from axe_hack_city.services.game_session_state_service import GameSessionStateService


def _build_session() -> GameSession:
    return GameSession(
        owner_user_id=7,
        name="Runtime Session",
        status="active",
        player_context={"location": "alley"},
        active_encounters={"objectives": [], "encounters": []},
        turn_metadata={"turn_number": 0},
        action_log_summary={"recent_actions": [], "total_actions": 0},
        state_version=3,
        state_payload={},
    )


def test_apply_transition_increments_state_version_and_updates_state() -> None:
    session = _build_session()
    transition = GameStateTransitionSchema(
        status="in_progress",
        player_context_patch={"location": "market"},
        action_log_entry="Moved to market",
    )

    GameSessionStateService.apply_validated_transition(session, transition)

    assert session.state_version == 4
    assert session.status == "in_progress"
    assert session.player_context["location"] == "market"
    assert session.turn_metadata["turn_number"] == 1


def test_apply_transition_rejects_expected_state_version_mismatch_without_mutation() -> None:
    session = _build_session()
    original_status = session.status
    transition = GameStateTransitionSchema(
        status="in_progress",
        expected_state_version=99,
    )

    try:
        GameSessionStateService.apply_validated_transition(session, transition)
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "expected=99" in str(exc)
        assert "actual=3" in str(exc)

    assert session.state_version == 3
    assert session.status == original_status


def test_apply_transition_multi_step_progression_increments_each_step() -> None:
    session = _build_session()

    first_transition = GameStateTransitionSchema(
        player_context_patch={"location": "roof"},
        expected_state_version=3,
    )
    GameSessionStateService.apply_validated_transition(session, first_transition)

    second_transition = GameStateTransitionSchema(
        player_context_patch={"stance": "hidden"},
        active_objectives=[{"id": "find-exit"}],
        expected_state_version=4,
    )
    GameSessionStateService.apply_validated_transition(session, second_transition)

    assert session.state_version == 5
    assert session.turn_metadata["turn_number"] == 2
    assert session.player_context["location"] == "roof"
    assert session.player_context["stance"] == "hidden"
    assert session.active_encounters["objectives"] == [{"id": "find-exit"}]
