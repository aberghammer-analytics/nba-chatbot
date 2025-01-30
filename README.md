# NBA Chatbot

The goal of this repo is to build a chatbot that can interact with a tabular SQL database to answer simple questions. The database has player and team statistics and is almost exclusively numeric. The chatbot will use LLMs to convert the question into SQL to interact with the database, then augment the response with additional information.

## Setup

This repo uses (uv)[https://docs.astral.sh/uv/]. To get started, you can run `uv sync` once you have `uv` installed, or you can use `pip`.

## Data Source

The data comes from the NBA API and was ingested using (`nbastatpy`)[https://pypi.org/project/nbastatpy/].

## Workflow

The proposed workflow is shown below. This is currently a work-in-progress and will require adjusting in the future.

1. User makes request
2. LLM determines which tables are required for the request
   1. Table dictionary required
   2. Ask for additional information that may be useful
3. The selected tables are used to reference a data dictionary for those tables
4. The LLM writes a SQL query that uses the tables to get the data
5. The SQL query is ran to get the data
   1. Retry loop may be required
6. The LLM interprets the data and writes a response

