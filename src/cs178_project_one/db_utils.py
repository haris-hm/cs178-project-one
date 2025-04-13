import cs178_project_one.creds as creds
import pymysql
from typing import Any

def db_connect() -> pymysql.connections.Connection:
    """
    Connects to the database using the credentials stored in creds.py.

    :return: A connection object to the database.
    """

    connection = pymysql.connect(
        host= creds.host,
        user= creds.user, 
        password = creds.password,
        db=creds.db,
    )

    return connection

def run_query(query) -> tuple[tuple[Any]]:
    """
    Executes a SQL query on the database.

    :query: The SQL query to execute.
    :return: A tuple of tuples containing the results of the query.
    """

    connection = db_connect()
    cursor = connection.cursor()

    try:
        cursor.execute(query)

        if query.strip().upper().startswith(("INSERT", "UPDATE", "DELETE")):
            connection.commit()

        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        connection.close()
