import os
import pandas as pd
from sqlalchemy import create_engine, inspect

DATABASE_URL = os.environ["DATABASE_URL"]
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

engine = create_engine(DATABASE_URL)
inspector = inspect(engine)


def process_file(filename: str, table_name: str):
    print(f"processing {filename}, inserting data into {table_name}")
    file_path = os.path.join(ARTIFACTS_PATH, filename)
    try:
        if not inspector.has_table(table_name):
            raise Exception(f"no such table {table_name}")
        table_columns = [column["name"] for column in inspector.get_columns(table_name)]
        for chunk in pd.read_csv(file_path, chunksize=CHUNK_SIZE):
            chunk.columns = chunk.columns.str.lower()
            chunk = chunk[[col for col in chunk.columns if col in table_columns]]
            date_columns = [
                col for col in chunk.columns if "time" in col or "date" in col
            ]
            for col in date_columns:
                chunk[col] = pd.to_datetime(chunk[col], errors="coerce")
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
