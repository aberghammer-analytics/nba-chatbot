from pathlib import Path

import instructor
import load_dotenv
import pandas as pd
import streamlit as st
import yaml
from chatbot_utils import get_final_answer, get_sql_code, get_tables
from openai import OpenAI
from sqlalchemy import create_engine

load_dotenv.load_dotenv()

TABLE_DICTIONARY_PATH = Path("data/meta/table_dictionary.yaml")
COLUMN_DICTIONARY_PATH = Path("data/meta/column_definitions.yaml")

DB_PATH_DICT = {
    "Regular Season Per Game": Path("data/database/nba-db-regseason.db"),
    "Regular Season Per Possession": Path("data/database/nba-db-perposs-season.db"),
}


@st.cache_resource()
def get_db_connection(selection: str, db_path_dict: dict = DB_PATH_DICT):
    db_path = db_path_dict[selection]
    return create_engine(f"duckdb:///{str(db_path)}").connect()


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

# Create a form that will only submit when the user confirms their input.
with st.form(key="text_form"):
    # Textbox for user input
    user_input = st.text_input("Ask a basic NBA stats question...")
    # The form_submit_button triggers submission (or user can hit Enter when the text box is focused)
    submit_button = st.form_submit_button(label="Submit")

conn_path = "Regular Season Per Game"


if submit_button:
    if "conn" in st.session_state:
        if st.session_state.previous_conn_path != conn_path:
            st.session_state.conn.close()
            st.session_state.conn = get_db_connection(selection=conn_path)

    # If no connection exists or the user changes the selection, create a new connection
    if (
        "conn" not in st.session_state
        or st.session_state.previous_conn_path != conn_path
    ):
        st.session_state.conn = get_db_connection(conn_path)
        st.session_state.previous_conn_path = conn_path

    # depending on above selections, select correct database path
    conn = get_db_connection(selection="Regular Season Per Game")

    table_results = get_tables(
        client_instructor=client_instructor,
        user_input=user_input,
        table_dictionary=table_dictionary,
    )

    sql_result = get_sql_code(
        client_instructor=client_instructor,
        user_input=user_input,
        initial_result=table_results,
        column_dictionary=column_dictionary,
    )

    print(sql_result)

    if st.session_state.conn:
        # Example query

        out_df = pd.read_sql_query(sql_result, st.session_state.conn).to_string()

    # conn.close()

    answer = get_final_answer(
        client_instructor=client_instructor,
        user_input=user_input,
        table_output=out_df,
    )

    st.markdown(answer)
