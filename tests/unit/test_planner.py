from contextcore.agent.planner import PlanState


def test_plan_state_progression():
    state = PlanState(
        original_query="What is our revenue?",
        sub_queries=["Q1", "Q2"],
    )
    assert not state.is_complete
    assert state.next_sub_query() == "Q1"
    state.record_hop("Q1", [{"text": "Revenue is $1M"}])
    assert state.next_sub_query() == "Q2"
    state.record_hop("Q2", [{"text": "Growth is 20%"}])
    assert state.is_complete
    assert len(state.context_buffer) == 2
