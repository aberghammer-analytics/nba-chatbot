# NBA Chatbot

The goal of this repo is to build a chatbot that can interact with a tabular SQL database to answer simple questions. The database has player and team statistics and is almost exclusively numeric. The chatbot will use LLMs to convert the question into SQL to interact with the database, then augment the response with additional information.

## Setup

This repo uses [`uv`](https://docs.astral.sh/uv/). To get started, you can run `uv sync` once you have `uv` installed, or you can use `pip`.

## Data Source

The data comes from the NBA API and was ingested using [`nbastatpy`](https://pypi.org/project/nbastatpy/).