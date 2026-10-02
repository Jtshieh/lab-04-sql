"""Shared environment-based MySQL connection configuration."""

import logging
import os

import mysql.connector

LOGGER = logging.getLogger(__name__)


def connect():
    """Connect to the assigned database using environment variables."""
    required = ("DBHOST", "DBNAME", "DBUSER", "DBPASS")
    missing = [name for name in required if not os.environ.get(name)]
    if missing:
        raise ValueError("Missing environment variables: " + ", ".join(missing))
    LOGGER.info("Opening MySQL connection")
    # Passwords stay in the environment and are never included in log messages.
    return mysql.connector.connect(
        host=os.environ["DBHOST"],
        database=os.environ["DBNAME"],
        user=os.environ["DBUSER"],
        password=os.environ["DBPASS"],
        port=int(os.environ.get("DBPORT", "3306")),
        connection_timeout=10,
        charset="utf8mb4",
    )
