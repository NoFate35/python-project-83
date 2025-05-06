import psycopg2
from psycopg2.extras import DictCursor


class UrlRepository:
    def __init__(self, conn):
        self.conn = conn
    def _update(self, car):
        with self.conn.cursor() as cur:
            cur.execute(
                "UPDATE cars SET manufacturer = %s, model = %s WHERE id = %s",
                (car["manufacturer"], car["model"], car["id"]),
            )
        self.conn.commit()

    def _create(self, car):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO cars (manufacturer, model) VALUES (%s, %s) RETURNING id",
                (car["manufacturer"], car["model"]),
            )
            id = cur.fetchone()[0]
            car["id"] = id
        self.conn.commit()