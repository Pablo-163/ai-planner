from state import PlannerState
from llm import invoke_json
from llm import invoke_text
#from llm import get_llm

'''
def invoke_json(prompt: str) -> dict:
    llm = get_llm()
    response = llm.invoke(prompt)

    print("RAW RESPONSE:")
    print(repr(response.content))

    return json.loads(response.content)
'''

def parse_goal_node(state: PlannerState) -> PlannerState:
    '''
    Извлечение параметров из запроса пользователя
    '''
    prompt = f"""
            Проанализируй запрос пользователя и верни строго JSON.

            Запрос пользователя:
            {state["user_goal"]}

            Извлеки поля:
            - deadline
            - available_time_per_day
            - user_level
            - missing_fields

            Правила:
            - Если значение не указано, верни null
            - Если какого-то поля не хватает, добавь его имя в missing_fields
            - Не придумывай данные от себя
            - Верни только JSON, без пояснений

            Формат ответа:
            {{
            "deadline": "string or null",
            "available_time_per_day": "string or null",
            "user_level": "string or null",
            "missing_fields": ["deadline", "available_time_per_day", "user_level"]
            }}
            """

    data = invoke_json(prompt)

    state["deadline"] = data.get("deadline")
    state["available_time_per_day"] = data.get("available_time_per_day")
    state["user_level"] = data.get("user_level")
    state["missing_fields"] = data.get("missing_fields", [])

    return state

def handle_missing_info(state):
    '''
    Простая обработка пропущенных значений
    '''
    if state["missing_fields"]:
        fields = ", ".join(state["missing_fields"])
        state["final_plan"] = (
            f"Недостаточно данных для построения плана. "
            f"Уточни: {fields}."
        )
    return state


def build_subtasks_node(state):
    '''
    Разбиение на подзадачи
    '''
    prompt = f"""
                Верни только один JSON-блок в формате ```json ... ```.

                Пользовательская цель:
                {state["user_goal"]}

                Параметры:
                - deadline: {state["deadline"]}
                - available_time_per_day: {state["available_time_per_day"]}
                - user_level: {state["user_level"]}

                Нужно:
                - разбить цель на 5-8 логичных подзадач
                - подзадачи должны быть короткими и конкретными
                - не дублируй похожие пункты
                - учитывай уровень пользователя и срок

                Формат ответа:
                {{
                "subtasks": [
                    "подзадача 1",
                    "подзадача 2",
                    "подзадача 3"
                ]
                }}
              """

    data = invoke_json(prompt)
    state["subtasks"] = data.get("subtasks", [])
    return state


def build_plan_node(state):
    '''
    Финальный ответ с конечныс планом действий
    '''
    subtasks_text = "\n".join(f"- {task}" for task in state["subtasks"])

    prompt = f"""
        Составь реалистичный и краткий пошаговый план для пользователя.

        Цель:
        {state["user_goal"]}

        Параметры:
        - deadline: {state["deadline"]}
        - available_time_per_day: {state["available_time_per_day"]}
        - user_level: {state["user_level"]}

        Подзадачи:
        {subtasks_text}

        Требования к ответу:
        - ответ на русском языке
        - план должен быть практичным и реалистичным
        - разбей план на этапы или дни
        - не делай ответ слишком длинным
        - в конце добавь 2-3 короткие рекомендации

        Верни только итоговый текст плана, без пояснений про формат.
        """

    state["final_plan"] = invoke_text(prompt)
    return state