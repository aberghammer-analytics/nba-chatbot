# NBA Chatbot

The goal of this repo is to build a chatbot that can interact with a tabular SQL database to answer simple questions. The database has player and team statistics and is almost exclusively numeric. The chatbot will use LLMs to convert the question into SQL to interact with the database, then augment the response with additional information.

## Setup

This repo uses [uv](https://docs.astral.sh/uv/). To get started, you can run `uv sync` once you have `uv` installed, or you can use `pip`.

## Running the App

Create a `.env` file with the same setup as the `sample.env` file. You can then run the app using `streamlit run app/chatbot_app.py`. 

The application uses [duckdb](https://duckdb.org/docs/) to store data. There are 4 databases each with the same table structure. This allows users in the application to select the type of data they want to query. This could be any of `playoffs` vs `regular season` or `per possession` vs `standard` statistics.

## Data Source

The data comes from the NBA API and was ingested using [`nbastatpy`](https://pypi.org/project/nbastatpy/). This was used to build the databases from the raw `.csv` files.

## Workflow

The application uses the following workflow under the hood:

1. User makes request in chatbox along with stat type selections.
2. LLM determines which tables are required for the request using the table dictionary
3. The selected tables are used to reference a data dictionary for those tables with column definitions
4. The LLM writes a SQL query that uses the tables to get the data
5. The SQL query is ran to get the data
6. The LLM interprets the data and writes a response



