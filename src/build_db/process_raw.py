from pathlib import Path

import pandas as pd
import typer
from loguru import logger
from rich.progress import track
from typing_extensions import Annotated

app = typer.Typer()


@app.command()
def process_source_data(
    input_folder: Annotated[
        Path,
        typer.Argument(
            help="Path to the folder containing the raw data (PLAYER, SEASON, etc.)"
        ),
    ],
    output_folder: Annotated[
        Path,
        typer.Argument(
            help="Path to the folder where the processed data will be saved"
        ),
    ],
):
    folders = [file for file in list(input_folder.iterdir()) if file.is_dir()]

    data = {}

    for folder in track(folders, description="Reading & Processing..."):
        for file in list(folder.iterdir()):
            if file.suffix == ".json":
                continue

            file_name = "_".join(file.stem.split("_", 1)[1:])

            df = pd.read_csv(file)
            if df.shape[0] == 0:
                continue

            if file_name in data.keys():
                data[file_name].append(df)
            else:
                data[file_name] = [df]

    logger.info("Combining and Saving Data...")
    for key, value in data.items():
        data[key] = pd.concat(value).drop_duplicates()
        data[key].to_csv(output_folder.joinpath(f"{key}.csv"), index=False)


if __name__ == "__main__":
    app()
