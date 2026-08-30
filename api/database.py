import psycopg


DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "postgres",
    "user": "ai_user",
    "password": "ai_password",
}


def get_connection():
    return psycopg.connect(**DB_CONFIG)


if __name__ == "__main__":
    with get_connection() as connection:
        print("Database connection successful")
