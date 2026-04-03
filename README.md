# Простой AI-планнер задач

Использует LangGraph и GigaChat.
Граф состояний планера:

parse_goal
   ├──> missing_info ───> END \
   └──> build_subtasks ─> build_plan ─> END

## Установка и запуск

Установка необходимых пакетов:
```
pip install -r requirements.txt
````
Примеры запуска расопложены в `notebooks\demo.ipynb`