import yaml
from chatbot_prompts import (
    FinalOutput,
    SqlCodeOutput,
    TablesForSql,
    get_final_output_prompt,
    get_sql_code_prompt,
    initial_prompt_get_table,
)
from openai import OpenAI


def get_tables(
    client_instructor: OpenAI,
    user_input: str,
    table_dictionary: dict,
    model: str = "gpt-4o-mini",
):
    table_definitions = yaml.dump(
        {k: v["description"] for k, v in table_dictionary["tables"].copy().items()}
    )

    # Initial Response
    initial_user_prompt = initial_prompt_get_table(
        user_input=user_input, table_dictionary=table_definitions
    )

    initial_result = client_instructor.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are an NBA data scientist who is writing a SQL query to answer a user question.",
            },
            {"role": "user", "content": initial_user_prompt},
        ],
        response_model=TablesForSql,
        max_retries=5,
    )

    return initial_result.table_list


def get_sql_code(
    client_instructor: OpenAI,
    user_input: str,
    initial_result: TablesForSql,
    column_dictionary: dict,
    model: str = "gpt-4o-mini",
):
    table_list_output = ", ".join(initial_result)

    column_definitions = yaml.dump(
        {k: v for k, v in column_dictionary.items() if k.lower() in initial_result}
    )

    # Get SQL Code
    sql_code_prompt = get_sql_code_prompt(
        user_input=user_input,
        selected_tables=table_list_output,
        column_definitions=column_definitions,
    )

    sql_result = client_instructor.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are an NBA data scientist who is writing a SQL query to answer a user question.",
            },
            {"role": "user", "content": sql_code_prompt},
        ],
        response_model=SqlCodeOutput,
        max_retries=5,
    )

    return sql_result.sql_code


def get_final_answer(
    client_instructor: OpenAI,
    user_input: str,
    table_output: str,
    model: str = "gpt-4o-mini",
):
    # Get SQL Code
    final_output_prompt = get_final_output_prompt(
        user_input=user_input,
        table_output=table_output,
    )

    final_result = client_instructor.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are an NBA data scientist who is writing a SQL query to answer a user question.",
            },
            {"role": "user", "content": final_output_prompt},
        ],
        response_model=FinalOutput,
        max_retries=5,
    )

    return final_result.answer
