from typing import TypedDict, Optional, List

class PlannerState(TypedDict):
    '''
    Состояния графа AI-планировщика
    '''
    user_goal: str
    deadline: Optional[str]
    available_time_per_day: Optional[str]
    user_level: Optional[str]

    missing_fields: List[str]
    subtasks: List[str]

    draft_plan: str
    final_plan: str