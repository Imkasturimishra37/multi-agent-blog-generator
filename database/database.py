import sqlite3
import os


DB_PATH = os.path.join(
    os.path.dirname(__file__),
    "history.db"
)


def create_database():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS blog_history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            topic TEXT NOT NULL,

            blog TEXT NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """
    )

    conn.commit()
    conn.close()


def save_blog(topic, blog):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO blog_history(topic, blog)
        VALUES (?, ?)
        """,
        (topic, blog)
    )

    conn.commit()
    conn.close()


def get_history():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT topic, created_at
        FROM blog_history
        ORDER BY id DESC
        """
    )

    history = cursor.fetchall()

    conn.close()

    return history
