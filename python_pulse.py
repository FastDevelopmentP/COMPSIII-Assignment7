# Step 5 Import sqlite3 for SQLite database access
import sqlite3

# Step 6 Connect to python_pulse.db in the same folder
connection = sqlite3.connect("python_pulse.db")

# Step 7 Create a cursor to execute SQL commands
cursor = connection.cursor()

# 8) Drop tables in dependency-safe order so re-runs don’t duplicate data
#    (child tables before parent tables)
cursor.execute("DROP TABLE IF EXISTS user_workout;")
cursor.execute("DROP TABLE IF EXISTS goals;")
cursor.execute("DROP TABLE IF EXISTS profiles;")
cursor.execute("DROP TABLE IF EXISTS workouts;")
cursor.execute("DROP TABLE IF EXISTS users;")


# 9,10) Create the users table
#    Columns: user_id (PK), username, password, email
cursor.execute("""
CREATE TABLE users (
    user_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    username  TEXT    NOT NULL,
    password  TEXT    NOT NULL,
    email     TEXT    NOT NULL
);
""")

# 11,12) Create the profiles table (one-to-one with users via user_id FK)
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

# 13) insert sample USERS data (single execute, multi-row VALUES)
cursor.execute("""
INSERT INTO users (username, password, email) VALUES
  ('john_doe',        'password123',    'john_doe@gmail.com'),
  ('jane_smith',      'mypassword',     'jane@gmail.com'),
  ('alice_jones',     'alicepassword',  'ajones@yahoo.com'),
  ('bob_brown',       'bobpassword',    'bobby@yahoo.com'),
  ('rebecca_charles', 'rebeccapassword','becky123@gmail.com');
""")

# 13) insert sample PROFILES data (single execute, multi-row VALUES)
cursor.execute("""
INSERT INTO profiles (user_id, height, weight, age, notes) VALUES
  (1, 180, 75, 28, 'Loves hiking and outdoor activities.'),
  (2, 165, 60, 25, 'Enjoys painting and art.'),
  (3, 170, 65, 30, 'Passionate about technology and coding.'),
  (4, 175, 80, 22, 'Avid reader and writer.'),
  (5, 160, 50, 27, 'Fitness enthusiast and gym lover.');
""")

# 14) Create the goals table
#    Columns: goal_id (PK), name, target_value, user_id (FK to users)
cursor.execute("""
CREATE TABLE goals (
    goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    target_value INTEGER,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
""")

# 15) insert sample GOALS data (single execute, multi-row VALUES)
cursor.execute("""
INSERT INTO goals (name, target_value, user_id) VALUES
    ('Run 5km', 5, 1), 
    ('Lose 10kg', 10, 2), 
    ('Lift 100kg 3x', 100, 3), 
    ('Meditate daily', 1, 5), 
    ('Cycle 100km', 100, 4), 
    ('Complete a marathon', 42, 5), 
    ('Run 5 km', 5, 5);
""");

# 16) Create the workouts table
#    Columns: workout_id (PK), name, description, duration
cursor.execute("""
CREATE TABLE workouts ( 
    workout_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    duration INTEGER
);
""")

# 17) Create the user_workout join table (composite PK)
#    Columns: user_id (FK to users), workout_id (FK to workouts)
cursor.execute("""
CREATE TABLE IF NOT EXISTS user_workout (
    user_id INTEGER NOT NULL,
    workout_id INTEGER NOT NULL,
    PRIMARY KEY (user_id, workout_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (workout_id) REFERENCES workouts(workout_id)
);
""")

# 18) insert sample WORKOUTS data (single execute, multi-row VALUES)
cursor.execute("""
INSERT INTO workouts (name, description, duration) VALUES   
  ('Morning Yoga', 'A refreshing morning yoga session.', 30),
  ('HIIT Workout', 'High-Intensity Interval Training.', 45),
  ('Weightlifting','Full body weightlifting session.', 60),
  ('Cycling',      'Outdoor cycling for endurance.', 120),
  ('Meditation',   'Guided meditation for relaxation.', 15);
""")

# 18) insert sample USER_WORKOUT data (single execute, multi-row VALUES)
cursor.execute("""
INSERT INTO user_workout (user_id, workout_id) VALUES
  (1,1),(1,2),(2,3),(3,4),(4,5),(5,1),(5,2);
""")

# 19) Commit changes and close the connection and take screenshot
connection.commit()
connection.close()
