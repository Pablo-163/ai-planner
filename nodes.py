from state import PlannerState
from llm import invoke_json
#from llm import get_llm
import json

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