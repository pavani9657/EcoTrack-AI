import sqlite3
import pandas as pd
from sklearn.linear_model import LinearRegression

DB_NAME = "ecotrack.db"


def predict_next_impact():
    connection = sqlite3.connect(DB_NAME)

    df = pd.read_sql_query(
        """
        SELECT distance, electricity, water, meals,
               meat_meals, plastic_bottles, total_impact
        FROM activities
        ORDER BY id
        """,
        connection
    )

    connection.close()

    if len(df) < 3:
        return None

    # Use previous activity to predict the next activity
    df["previous_impact"] = df["total_impact"].shift(1)

    df = df.dropna()

    X = df[["previous_impact"]]
    y = df["total_impact"]

    model = LinearRegression()
    model.fit(X, y)

    latest_impact = df["total_impact"].iloc[-1]

    prediction = model.predict(
        [[latest_impact]]
    )[0]

    return max(0, prediction)