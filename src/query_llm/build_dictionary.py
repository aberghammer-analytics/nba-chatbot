from pathlib import Path

import instructor
import load_dotenv
import pandas as pd
import typer
import yaml
from llm_prompts import ColumnDefinitionOutput, get_definitions
from loguru import logger
from openai import OpenAI
from typing_extensions import Annotated

load_dotenv.load_dotenv()

app = typer.Typer()


@app.command()
def get_column_definitions(
    root_data_folder: Annotated[
        Path,
        typer.Argument(
            help="Path to the root data folder", file_okay=False, dir_okay=True
        ),
    ],
    table_dictionary_path: Annotated[
        Path,
        typer.Argument(
            help="Path to the table dictionary YAML file",
            file_okay=True,
            dir_okay=False,
        ),
    ] = Path("data/meta/table_dictionary.yaml"),
    output_file: Annotated[
        Path,
        typer.Argument(
            help="Path to the output file (.yaml)", file_okay=True, dir_okay=False
        ),
    ] = Path("data/meta/column_definitions.yaml"),
    model: Annotated[
        str, typer.Argument(help="Model to use for querying LLM")
    ] = "gpt-4o-mini",
):
    logger.info("Loading metadata...")
    # Open the YAML file and load its content
    with open(table_dictionary_path, "r") as file:
        table_dictionary = yaml.safe_load(file)

    files = [file for file in list(root_data_folder.iterdir()) if file.is_file()]

    logger.info("Setting up OpenAI API...")
    client = OpenAI()

    client_instructor = instructor.patch(client)

    column_definitions = {}

    for file in files:
        table_name = file.stem
        logger.info(f"Processing {table_name}")
        df = pd.read_csv(file)
        table_cols = ", ".join(list(df.columns))

        table_definition = table_dictionary["tables"][root_data_folder.name][
            table_name.lower()
        ]["description"]

        input_prompt = get_definitions(
            table_name=table_name,
            table_definition=table_definition,
            table_cols=table_cols,
        )

        result = client_instructor.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an NBA data scientist who is building documentation for a database of player statistics.",
                },
                {"role": "user", "content": input_prompt},
            ],
            response_model=ColumnDefinitionOutput,
            max_retries=5,
        )

        column_definitions[table_name] = result.column_definitions

    logger.info("Saving column definitions...")
    with open(output_file, "w") as file:
        yaml.safe_dump(column_definitions, file)


if __name__ == "__main__":
    app()
