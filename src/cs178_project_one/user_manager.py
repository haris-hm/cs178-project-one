import cs178_project_one.db_utils as db_utils
import re

def validate_password(username: str, password: str) -> bool | None:
    result: tuple[tuple[str]] | None = db_utils.run_query(
        f"""
        SELECT * FROM Users
        WHERE name = '{username}';
        """
    )

    if result is None or len(result) == 0:
        return None
    else:
        stored_password: str = result[0][2]
        return password == stored_password        

def create_account(username: str, password: str) -> tuple[bool, str]: 
    # Check if the username and password fit the patterns
    username_pattern = r'^[a-zA-Z0-9]{1,20}$'
    password_pattern = r'^[\x21-\x7E]{8,}$'

    if not re.search(username_pattern, username):
        return (False, 'Username must be alphanumeric and at most 20 characters')
    elif not re.search(password_pattern, password):
        return (False, 'Password must be at least 8 characters with no spaces')
    
    # Check if the username is already in use
    result: tuple[tuple[str]] | None = db_utils.run_query(
        f"""
        SELECT * FROM Users
        WHERE name = '{username}';
        """
    )

    if len(result) > 0:
        return (False, 'That username is already in use')
    
    # Create the account
    result = db_utils.run_query(
        f"""
        INSERT INTO Users (name, password)
        VALUES ('{username}', '{password}');
        """
    )
    
    return (True, '')
