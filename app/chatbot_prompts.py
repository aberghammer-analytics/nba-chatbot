from typing import List, Literal

from prompts import template
from pydantic import BaseModel, Field


@template
def initial_prompt_get_table(user_input: str, table_dictionary: str):
    return """
    Your task is to select a table from a list of tables along with their definitions that would be most suitable to create a SQL query that would answer the following question from a user:

    {{user_input}}

    Given the user question, please select the required tables for creating a SQL query that would answer the user question from the following list of tables:

    Table Definitions:

    {{table_dictionary}}

    NOTE: the player_stats table only contains basic boxscore statistics and does not contain any advanced statistics or play type information. 
    To get totals from player_stats, you must multiply the per game statistics by the games played.

    NOTE: Do not use the games table unless the user question specifically asks for information about games.
    """


@template
def get_sql_code_prompt(user_input: str, selected_tables: str, column_definitions: str):
    return """
    Given the user question: {{user_input}} and the selected tables: {{selected_tables}} along with the column definitions: {{column_definitions}}

    Write a SQL query that would answer the user question. 

    NOTE: SEASON_ID is always in the format YYYYYY. For example, the 2021-2022 season would be 202122. NOT 202121. The 2020 season would be 202021.

    NOTE: If you are asked for a total, you must multiply the per game statistics by the games played to get the total. This is always true if using the player_stats table.
    - DO NOT SUM THE PER GAME STATISTICS YOU MUST MULTIPLY BY GAMES PLAYED.

    NOTE: You must ensure your column and table names are correct.

    NOTE: Your SQL Code should be as simple as possible using as few tables as possible to answer the user question.

    """


@template
def get_final_output_prompt(table_output: str, user_input: str):
    return """

    Given the users question: {{user_input}} and the resulting data from a sql query {{table_output}}
    
    Please answer the users question using the data provided. 

    If the user question is asking for a specific player or team, please provide the name of the player or team along with the statistic requested.

    If the result is empty, please provide a message to the user that the data is not available.
    """


class TablesForSql(BaseModel):
    table_list: List[
        Literal[
            "combine_stats",
            "common_info",
            "catchshoot_player",
            "catchshoot_team",
            "cut_player",
            "cut_team",
            "defense_player",
            "defense_team",
            "drives_player",
            "drives_team",
            "efficiency_player",
            "efficiency_team",
            "elbowtouch_player",
            "elbowtouch_team",
            "handoff_player",
            "handoff_team",
            "isolation_player",
            "isolation_team",
            "lineup_details",
            "lineups",
            "misc_player",
            "misc_team",
            "offrebound_player",
            "offrebound_team",
            "offscreen_player",
            "offscreen_team",
            "opponent_shooting",
            "painttouch_player",
            "painttouch_team",
            "passing_player",
            "passing_team",
            "player_clutch",
            "player_defense",
            "player_games",
            "player_hustle",
            "player_matchups",
            "player_shot_locations",
            "player_shots",
            "player_stats",
            "possessions_player",
            "possessions_team",
            "posttouch_player",
            "posttouch_team",
            "postup_player",
            "postup_team",
            "prballhandler_player",
            "prballhandler_team",
            "prrollman_player",
            "prrollman_team",
            "pullupshot_player",
            "pullupshot_team",
            "salaries",
            "speeddistance_player",
            "speeddistance_team",
            "spotup_player",
            "spotup_team",
            "team_clutch",
            "team_defense",
            "team_games",
            "team_hustle",
            "team_shot_locations",
            "team_stats",
            "transition_player",
            "transition_team",
        ]
    ] = Field(..., description="List of tables needed for SQL query")


class SqlCodeOutput(BaseModel):
    sql_code: str = Field(..., description="SQL code that answers the user question")


class FinalOutput(BaseModel):
    answer: str = Field(..., description="Answer to the user question")
