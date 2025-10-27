#The database for project-gigachad containing all the necessary tables and relationships.

#What tables are the db going to contain?

import sqlite3

# Sourcematerial= https://docs.python.org/3/library/sqlite3.html

class Database():
    def __init__(self):
        # 'pass' is the standard placeholder for an empty block
        pass

    def create_db(self):
        """
        Connects to the app.db and creates the 'deployed_apps'
        table if it does not already exist.
        Returns True on success, False on failure.
        """
        # We can use triple-quotes for a multi-line SQL command,
        # which makes it much easier to read.
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS deployed_apps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            app_name TEXT,
            github_url TEXT,
            status TEXT,
            port INTEGER,
            container_id INTEGER
        );
        """
        
        try:
            # 'with' handles connection closing automatically
            with sqlite3.connect("app.db") as conn:
                cur = conn.cursor()
                cur.execute(create_table_sql)
                
            # If we get here, the 'with' block finished without error
            # and the transaction was automatically committed.
            return True
            
        except sqlite3.Error as e:
            # Catching the more general sqlite3.Error is good practice
            print(f"Failed to create database or table: {e}")
            return False

# --- How to use the class ---
open_database = Database()
if open_database.create_db():
    print("Database and table are ready!")
else:
    print("Database setup failed.")

# Now you can try to connect and check
try:
    conn = sqlite3.connect("app.db")
    cur = conn.cursor()
    
    # This query will now work!
    # It won't return anything yet, but it won't error.
    cur.execute('SELECT * FROM deployed_apps')
    print("\nSuccessfully executed 'SELECT * FROM deployed_apps'")
    print(cur.fetchall()) # .fetchall() will return an empty list: []

except sqlite3.Error as e:
    print(f"Error querying database: {e}")

finally:
    if conn:
        conn.close()