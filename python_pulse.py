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

# --- Step 13: insert sample USERS data (single execute, multi-row VALUES) ---
cursor.execute("""
INSERT INTO users (username, password, email) VALUES
  ('john_doe',        'password123',    'john_doe@gmail.com'),
  ('jane_smith',      'mypassword',     'jane@gmail.com'),
  ('alice_jones',     'alicepassword',  'ajones@yahoo.com'),
  ('bob_brown',       'bobpassword',    'bobby@yahoo.com'),
  ('rebecca_charles', 'rebeccapassword','becky123@gmail.com');
""")

# --- Step 13: insert sample PROFILES data (single execute, multi-row VALUES) ---
cursor.execute("""
INSERT INTO profiles (user_id, height, weight, age, notes) VALUES
  (1, 180, 75, 28, 'Loves hiking and outdoor activities.'),
  (2, 165, 60, 25, 'Enjoys painting and art.'),
  (3, 170, 65, 30, 'Passionate about technology and coding.'),
  (4, 175, 80, 22, 'Avid reader and writer.'),
  (5, 160, 50, 27, 'Fitness enthusiast and gym lover.');
""")

cursor.execute("""
CREATE TABLE goals (
    goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    target_value INTEGER,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
""")

cursor.execute("""
CREATE TABLE workouts ( 
    workout_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    duration INTEGER
);
""")

cursor.execute("""
CREATE TABLE user_workouts (    
    user_workout_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    workout_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (workout_id) REFERENCES workouts(workout_id)
);
""")
connection.commit()
