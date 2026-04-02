'''
Простой граф сосотояний AI-агента для построения плана действий.

parse_goal
   ├──> missing_info ───> END
   └──> build_subtasks ─> build_plan ─> END

'''


from langgraph.graph import StateGraph, END

from state import PlannerState
from nodes import (
    parse_goal_node,
    handle_missing_info,
    build_subtasks_node,
    build_plan_node,
)


def route_after_parse(state: PlannerState) -> str:
    if state["missing_fields"]:
        return "missing_info"
    return "build_subtasks"


def build_graph():
    '''
    Основной граф состояний помошника
    '''
    builder = StateGraph(PlannerState)

    builder.add_node("parse_goal", parse_goal_node)
    builder.add_node("missing_info", handle_missing_info)
    builder.add_node("build_subtasks", build_subtasks_node)
    builder.add_node("build_plan", build_plan_node)

    builder.set_entry_point("parse_goal")

    builder.add_conditional_edges(
        "parse_goal",
        route_after_parse,
        {
            "missing_info": "missing_info",
            "build_subtasks": "build_subtasks",
        },
    )

    builder.add_edge("missing_info", END)
    builder.add_edge("build_subtasks", "build_plan")
    builder.add_edge("build_plan", END)

    return builder.compile()


graph = build_graph()