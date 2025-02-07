from pathlib import Path

import instructor
import load_dotenv
import streamlit as st
import yaml
from chatbot_utils import (
    SqlCodeOutput,
    TablesForSql,
    get_sql_code_prompt,
    initial_prompt_get_table,
)
from openai import OpenAI

load_dotenv.load_dotenv()

TABLE_DICTIONARY_PATH = Path("data/meta/table_dictionary.yaml")
COLUMN_DICTIONARY_PATH = Path("data/meta/column_definitions.yaml")

# Open the YAML file and load its content
with open(TABLE_DICTIONARY_PATH, "r") as file:
    table_dictionary = yaml.safe_load(file)

table_definitions = yaml.dump(
    {k: v["description"] for k, v in table_dictionary["tables"].copy().items()}
)

with open(COLUMN_DICTIONARY_PATH, "r") as file:
    column_dictionary = yaml.safe_load(file)

client_instructor = instructor.patch(OpenAI())

st.title("NBA Stats Chatbot")

with st.expander("README", expanded=False):
    st.markdown(
        "This is a simple chatbot that can answer basic questions about NBA stats."
    )

user_input = st.chat_input("Ask a basic NBA stats question...")

# Initial Response
initial_user_prompt = initial_prompt_get_table(
    user_input=user_input, table_dictionary=table_definitions
)

initial_result = client_instructor.chat.completions.create(
    model="gpt-4o-mini",
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

table_list_output = ", ".join(initial_result.table_list)
column_definitions = yaml.dump(
    {
        k: v
        for k, v in column_dictionary.items()
        if k.lower() in initial_result.table_list
    }
)

# Get SQL Code
sql_code_prompt = get_sql_code_prompt(
    user_input=user_input,
    selected_tables=table_list_output,
    column_definitions=column_definitions,
)

sql_result = client_instructor.chat.completions.create(
    model="gpt-4o-mini",
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

st.markdown(f"SQL CODE: {sql_result.sql_code}")
