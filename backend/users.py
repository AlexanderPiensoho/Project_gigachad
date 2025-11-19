#users.py
import sqlite3
import os
import random
import pwinput
from colorama import Fore, init
init(autoreset=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "Users.db")

def create_db():
    #The db is named Users.db
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, pwd TEXT, account_no INTEGER)")
    con.commit()
    con.close()
    #Close the connection after creating the db

def new_user():
    while True:
        name = input("Please enter your name: ")
        usermail = input("Please enter your email: ")
        if user_exists(usermail) == False:
            password = pwinput.pwinput(prompt="Enter a password: ", mask='*')
            pwd_check = pwinput.pwinput(prompt="Enter the same password again: ", mask='*')
            if password == pwd_check:
                data = ( name, usermail, password)
                sql_query = """
                INSERT INTO users (id, name, email, pwd) 
                VALUES (NULL, ?, ?, ?);
                """
                with sqlite3.connect(DB_PATH) as conn:
                    cur = conn.cursor()
                    cur.execute(sql_query, data)
                    conn.commit()

                print("User created!")
                return
            elif password != pwd_check:
                print(Fore.RED + "Passwords do not match. Please try again.")
                continue

def delete_user():
    pass

def fetch_user():
    pass

def user_exists(email):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT email FROM users WHERE email = ?", (email,))
        if cur.fetchone() is None:
            return False