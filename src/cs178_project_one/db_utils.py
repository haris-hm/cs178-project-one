import cs178_project_one.creds as creds
import pymysql

def db_connect():
    connection = pymysql.connect(
        host= creds.host,
        user= creds.user, 
        password = creds.password,
        db=creds.db,
    )

    return connection

def run_query(query):
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
