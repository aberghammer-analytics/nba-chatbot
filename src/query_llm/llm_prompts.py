from typing import List

from prompts import template
from pydantic import BaseModel, Field


@template
def get_definitions(table_name: str, table_cols: str, table_definition: str):
    return """

    Given the table {{table_name}} with the following definition: {{table_definition}} and the following columns: {{table_cols}}
    
    Provide a definition for each column in the table. The definition should be concise and clear. 

    Your response should be a dictionary where the keys are the column names and the values are the definitions.

    NOTE:
    If there is a game ID column, each metric for that table is a total for that game.
    If there is not a game ID column, each metric is an average across all games.
    """


class ColumnDefinitionOutput(BaseModel):
    column_definitions: List = Field(
        ...,
        description="List of dictionaries of column definitions with the format column_name: definition",
    )
