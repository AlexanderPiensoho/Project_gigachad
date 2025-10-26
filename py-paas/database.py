"""
Databashantering med SQLite för Py-PaaS
Hanterar deployed_apps tabell
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'py-paas.db')


def get_db_connection():
    """Skapa en anslutning till databasen"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # För att få dict-liknande resultat
    return conn


def init_db():
    """Initiera databasen och skapa tabellen om den inte finns"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS deployed_apps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            app_name TEXT NOT NULL,
            github_url TEXT NOT NULL,
            status TEXT NOT NULL,
            port INTEGER,
            container_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")


def get_all_apps():
    """Hämta alla deployade appar från databasen"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM deployed_apps ORDER BY created_at DESC')
    apps = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    return apps


def get_app_by_id(app_id):
    """Hämta en specifik app från databasen"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM deployed_apps WHERE id = ?', (app_id,))
    row = cursor.fetchone()
    app = dict(row) if row else None
    
    conn.close()
    return app


def add_app(app_name, github_url, status, port, container_id):
    """Lägg till en ny app i databasen"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO deployed_apps (app_name, github_url, status, port, container_id)
        VALUES (?, ?, ?, ?, ?)
    ''', (app_name, github_url, status, port, container_id))
    
    app_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return app_id


def update_app_status(app_id, status, container_id):
    """Uppdatera status för en app"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE deployed_apps
        SET status = ?, container_id = ?
        WHERE id = ?
    ''', (status, container_id, app_id))
    
    conn.commit()
    conn.close()


def delete_app(app_id):
    """Ta bort en app från databasen"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM deployed_apps WHERE id = ?', (app_id,))
    
    conn.commit()
    conn.close()
