# memory/sqlite_saver.py

import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver


def from_conn_stringx(cls, conn_string: str) -> "SqliteSaver":
    """
    Create a SqliteSaver from a connection string.

    Args:
    - cls: Class reference for SqliteSaver
    - conn_string (str): SQLite connection string

    Returns:
    - SqliteSaver: An instance of SqliteSaver for checkpoint persistence
    """
    return SqliteSaver(conn=sqlite3.connect(conn_string, check_same_thread=False))


SqliteSaver.from_conn_stringx = classmethod(from_conn_stringx)


def initialize_memory(conn_string: str = ":memory:") -> SqliteSaver:
    """
    Initialize the memory checkpoint system using SQLite.

    Args:
    - conn_string (str): SQLite connection string. Defaults to in-memory.

    Returns:
    - SqliteSaver: An initialized instance of SqliteSaver.
    """
    return SqliteSaver.from_conn_stringx(conn_string)
