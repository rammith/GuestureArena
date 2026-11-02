from app.core.database import (
    database,
    check_database_connection
)


def test_mongodb_connection():

    is_connected = check_database_connection()

    assert is_connected is True

    print("Database:", database.name)