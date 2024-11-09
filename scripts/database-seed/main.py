import os
import pandas as pd
from sqlalchemy import create_engine, inspect
from datetime import datetime

POSTGRES_URL = os.environ["POSTGRES_URL"]
ARTIFACTS_PATH = os.environ["ARTIFACTS_PATH"]
CHUNK_SIZE = 1000
CSV_TO_TABLE = {
    "diagnosis.csv": "diagnosis",
    "labs.csv": "labs",
    "medications.csv": "medications",
    "operations.csv": "operations",
    "vitals.csv": "vitals",
    "ward_vitals.csv": "ward_vitals",
}
BASE_DATETIME = datetime(2020, 1, 1)

engine = create_engine(POSTGRES_URL)
inspector = inspect(engine)


def process_file(filename: str, table_name: str):
    print(f"processing {filename}, inserting data into {table_name}")

    file_path = os.path.join(ARTIFACTS_PATH, filename)

    try:
        if not inspector.has_table(table_name):
            raise Exception(f"no such table {table_name}")

        table_columns_info = inspector.get_columns(table_name)
        table_columns = [column["name"] for column in table_columns_info]

        timestamp_columns = [
            col["name"]
            for col in table_columns_info
            if "timestamp" in str(col["type"]).lower()
        ]

        boolean_columns = [
            col["name"]
            for col in table_columns_info
            if str(col["type"]).lower() == "boolean"
        ]

        for chunk in pd.read_csv(file_path, chunksize=CHUNK_SIZE):
            chunk.columns = chunk.columns.str.lower()
            chunk = chunk[[col for col in chunk.columns if col in table_columns]]

            for col in timestamp_columns:
                if col in chunk.columns:
                    chunk[col] = BASE_DATETIME + pd.to_timedelta(
                        chunk[col].mask(chunk[col].isna()), unit="s"
                    )

            for col in boolean_columns:
                if col in chunk.columns:
                    chunk[col] = chunk[col].astype(bool)

            chunk.to_sql(table_name, engine, if_exists="append", index=False)

        print(f"successfully processed {filename}, inserted data into {table_name}")

    except Exception as e:
        print(f"error processing {filename}: {str(e)}")


def main():
    for filename in os.listdir(ARTIFACTS_PATH):
        if filename.endswith(".csv"):
            table_name = CSV_TO_TABLE.get(filename)

            if table_name:
                process_file(filename, table_name)
            else:
                print(f"no table mapping found for {filename}, skipping ...")


if __name__ == "__main__":
    main()
