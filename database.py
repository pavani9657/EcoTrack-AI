import sqlite3

DB_NAME = "ecotrack.db"


def create_database():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            distance REAL,
            vehicle TEXT,
            electricity REAL,
            water REAL,
            meals INTEGER,
            meat_meals INTEGER,
            plastic_bottles INTEGER,
            total_impact REAL
        )
    """)

    connection.commit()
    connection.close()


def save_activity(
    date,
    distance,
    vehicle,
    electricity,
    water,
    meals,
    meat_meals,
    plastic_bottles,
    total_impact
):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO activities
        (date, distance, vehicle, electricity, water,
         meals, meat_meals, plastic_bottles, total_impact)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        date,
        distance,
        vehicle,
        electricity,
        water,
        meals,
        meat_meals,
        plastic_bottles,
        total_impact
    ))

    connection.commit()
    connection.close()


def get_activities():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT date, distance, vehicle, electricity,
               water, meals, meat_meals,
               plastic_bottles, total_impact
        FROM activities
        ORDER BY date DESC, id DESC
    """)

    activities = cursor.fetchall()
    connection.close()

    return activities