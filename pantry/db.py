import mysql.connector
from config import DB_CONFIG

def get_connection():
    """
    Returns a live MySQL connection.

    Raises
    ------
    ConnectionError
        If the underlying connector cannot establish a connection.
    """
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as exc:  # pragma: no cover
        # Optionally add structured logging here
        raise ConnectionError("Could not establish MySQL connection") from exc