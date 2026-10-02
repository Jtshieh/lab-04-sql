"""Read, clean, and load the Mockaroo CSV into the assigned MySQL database."""

import argparse
import logging
from pathlib import Path

import mysql.connector
import pandas as pd

from sql_lab.database import connect

LOGGER = logging.getLogger(__name__)
COLUMNS = ["id", "group", "last_name", "email", "gender", "ip_address"]
DEFAULT_CSV = Path(__file__).resolve().parents[2] / "MOCK_DATA.csv"
CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS mock (
    id BIGINT PRIMARY KEY,
    `group` VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    gender VARCHAR(255) NOT NULL,
    ip_address VARCHAR(255) NOT NULL
)
"""
INSERT_ROW = """
INSERT INTO mock (id, `group`, last_name, email, gender, ip_address)
VALUES (%s, %s, %s, %s, %s, %s)
"""


def read_data(filename):
    """Read a CSV file into a pandas DataFrame."""
    LOGGER.info("Reading %s", filename)
    try:
        data = pd.read_csv(filename)
    except (OSError, pd.errors.ParserError, pd.errors.EmptyDataError):
        LOGGER.error("Could not read CSV file")
        raise
    LOGGER.info("Read %d rows and %d columns", *data.shape)
    return data


def clean_data(data):
    """Drop incomplete rows and validate the six expected columns and IDs."""
    LOGGER.info("Cleaning %d rows", len(data))
    if list(data.columns) != COLUMNS:
        raise ValueError("CSV columns must be: " + ", ".join(COLUMNS))
    cleaned = data.copy()
    for column in COLUMNS[1:]:
        cleaned[column] = cleaned[column].astype("string").str.strip()
        cleaned[column] = cleaned[column].replace("", pd.NA)
    cleaned = cleaned.dropna().copy()
    ids = pd.to_numeric(cleaned["id"], errors="raise")
    if ((ids % 1 != 0) | (ids <= 0)).any() or ids.duplicated().any():
        raise ValueError("IDs must be unique positive integers")
    cleaned["id"] = ids.astype("int64")
    for column in COLUMNS[1:]:
        if cleaned[column].str.len().gt(255).any():
            raise ValueError("Text values must fit VARCHAR(255)")
    LOGGER.info("Removed %d incomplete rows; kept %d", len(data) - len(cleaned), len(cleaned))
    return cleaned.reset_index(drop=True)


def load_data(data, table):
    """Create mock and insert cleaned rows, preserving any different existing data."""
    LOGGER.info("Preparing to load %d rows", len(data))
    # SQL identifiers cannot be bound as values. This lab has one fixed table.
    if table != "mock":
        raise ValueError('The destination table must be "mock"')
    connection = None
    cursor = None
    try:
        connection = connect()
        cursor = connection.cursor()
        cursor.execute(CREATE_TABLE)
        cursor.execute("SELECT id, `group`, last_name, email, gender, ip_address FROM mock ORDER BY id")
        existing = cursor.fetchall()
        expected = sorted(data.itertuples(index=False, name=None))
        if existing:
            if existing == expected:
                LOGGER.info("Database already contains the same %d rows; no changes needed", len(existing))
                return
            raise ValueError("mock already contains different data; refusing to overwrite it")
        for row in data.itertuples(index=False, name=None):
            cursor.execute(INSERT_ROW, tuple(row))
        cursor.execute("SELECT COUNT(*) FROM mock")
        count = cursor.fetchone()[0]
        if count != len(data):
            raise ValueError("Database row count differs from the cleaned DataFrame")
        connection.commit()
        LOGGER.info("Committed and verified %d rows in mock", count)
    except (mysql.connector.Error, ValueError) as error:
        if connection is not None:
            connection.rollback()
        LOGGER.error("Load failed (%s)", type(error).__name__)
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


def main():
    """Run the read, clean, and load workflow for a CSV file."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("filename", nargs="?", default=DEFAULT_CSV)
    args = parser.parse_args()
    load_data(clean_data(read_data(args.filename)), "mock")


if __name__ == "__main__":
    main()
