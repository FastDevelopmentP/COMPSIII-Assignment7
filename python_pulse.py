# 1) Import sqlite3 for SQLite database access
import sqlite3

# 2) Connect to python_pulse.db in the same folder
connection = sqlite3.connect("python_pulse.db")

# 3) Create a cursor to execute SQL commands
cursor = connection.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

# 5) Drop tables in dependency-safe order so re-runs don’t duplicate data
#    (child tables before parent tables)
cursor.execute("DROP TABLE IF EXISTS user_workouts;")
cursor.execute("DROP TABLE IF EXISTS goals;")
cursor.execute("DROP TABLE IF EXISTS profiles;")
cursor.execute("DROP TABLE IF EXISTS workouts;")
cursor.execute("DROP TABLE IF EXISTS users;")

# 6) Create the users table EXACTLY as the ERD/tests expect
#    Columns: user_id (PK), username, password, email
cursor.execute("""
CREATE TABLE users (
    user_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    username  TEXT    NOT NULL,
    password  TEXT    NOT NULL,
    email     TEXT    NOT NULL
);
""")

# 7) Create the profiles table (one-to-one with users via user_id FK)
#    Columns: profile_id (PK), user_id (UNIQUE/NOT NULL for 1–1), height, weight, age, notes
cursor.execute("""
CREATE TABLE profiles (
    profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL UNIQUE,
    height     INTEGER,
    weight     INTEGER,
    age        INTEGER,
    notes      TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
""")

connection.commit()
