import sqlite3

# Database file name
DB_NAME = "inventory.db"

# Create connection
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn


# Create tables if they do not exist
def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        Users_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Users_Name TEXT UNIQUE NOT NULL,
        Users_Email TEXT NOT NULL,
        User_Password TEXT NOT NULL,
        Created_At DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


# Run automatically when file is executed
if __name__ == "__main__":
    create_tables()
    print("Database and table created successfully")
