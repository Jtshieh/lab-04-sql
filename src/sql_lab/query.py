"""Run parameterized filters and grouped counts on the mock table."""

import argparse
import logging

import mysql.connector

from sql_lab.database import connect

LOGGER = logging.getLogger(__name__)
# Select complete, fixed statements instead of inserting a user-supplied identifier.
COUNT_QUERIES = {
    "id": "SELECT id AS value, COUNT(*) AS count FROM mock GROUP BY id ORDER BY id",
    "group": "SELECT `group` AS value, COUNT(*) AS count FROM mock GROUP BY `group` ORDER BY `group`",
    "last_name": "SELECT last_name AS value, COUNT(*) AS count FROM mock GROUP BY last_name ORDER BY last_name",
    "email": "SELECT email AS value, COUNT(*) AS count FROM mock GROUP BY email ORDER BY email",
    "gender": "SELECT gender AS value, COUNT(*) AS count FROM mock GROUP BY gender ORDER BY gender",
    "ip_address": "SELECT ip_address AS value, COUNT(*) AS count FROM mock GROUP BY ip_address ORDER BY ip_address",
}


def fetch_rows(statement, parameters=()):
    """Execute a read-only statement and return rows as dictionaries."""
    LOGGER.info("Executing SELECT query")
    connection = None
    cursor = None
    try:
        connection = connect()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(statement, parameters)
        rows = cursor.fetchall()
        LOGGER.info("Retrieved %d rows", len(rows))
        return rows
    except (mysql.connector.Error, ValueError) as error:
        LOGGER.error("Query failed (%s)", type(error).__name__)
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


def get_data_by_group(value):
    """Return all mock rows whose `group` column equals the bound value."""
    LOGGER.info("Filtering the group column")
    return fetch_rows(
        "SELECT id, `group`, last_name, email, gender, ip_address FROM mock WHERE `group` = %s ORDER BY id",
        (value,),
    )


def plot_counts(groupby):
    """Return counts for a validated column, suitable for printing or plotting."""
    LOGGER.info("Counting rows by a requested column")
    if groupby not in COUNT_QUERIES:
        raise ValueError("Unsupported grouping column")
    return fetch_rows(COUNT_QUERIES[groupby])


def main():
    """Print a group filter and counts for a selected column."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--group", default="blue")
    parser.add_argument("--groupby", default="group", choices=COUNT_QUERIES)
    args = parser.parse_args()
    rows = get_data_by_group(args.group)
    print("Rows matching group", repr(args.group))
    for row in rows:
        print(row)
    print("Matched rows:", len(rows))
    print("Counts by", args.groupby)
    for row in plot_counts(args.groupby):
        print(row)


if __name__ == "__main__":
    main()
