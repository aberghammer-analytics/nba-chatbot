from pathlib import Path

import pandas as pd
import typer
from loguru import logger
from rich.progress import track
from sqlalchemy import create_engine
from typing_extensions import Annotated

app = typer.Typer()


@app.command()
def build_db(
    input_folder: Annotated[
        Path, typer.Argument(help="Path to the folder containing the processed data")
    ] = Path("data/processed/"),
    output_folder: Annotated[
        Path,
        typer.Argument(
            help="Path to the folder where the database will be saved",
            dir_okay=True,
            file_okay=False,
        ),
    ] = Path("data/database/"),
    db_name: Annotated[str, typer.Argument(help="Name of the database")] = "nba-all",
):
    logger.info("Setting up paths and database connection")
    all_files = [
        file
        for file in input_folder.rglob("*")
        if (file.is_file()) & (file.suffix == ".csv")
    ]
    conn = create_engine(
        f"duckdb:///{output_folder.joinpath(f'{db_name}.db')}"
    ).connect()

    for file in track(all_files):
        logger.info(f"Processing {file}")
        # TODO: If standard/per_possession, add to table name
        if "per_possession" in str(file):
            table_name = f"{file.stem}_per_possession"
        else:
            table_name = f"{file.stem}_standard"

        df = pd.read_csv(file)
        df.to_sql(table_name, conn, if_exists="replace", index=False)

    conn.close()


if __name__ == "__main__":
    app()
