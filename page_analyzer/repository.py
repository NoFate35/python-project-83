from datetime import datetime

from psycopg2.extras import DictCursor


class UrlRepository:
    def __init__(self, conn):
        self.conn = conn

    def get_content(self):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM urls ORDER BY created_at")
            return [dict(row) for row in cur]

    def exist(self, url):
        name = url["name"]
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM urls WHERE name = %s", (name,))
            row = cur.fetchone()
            return dict(row)["id"] if row else None

    def find(self, id):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM urls WHERE id = %s", (id,))
            row = cur.fetchone()
            return dict(row) if row else None

    def save(self, url):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO urls (name, created_at) \
                VALUES (%s, %s) RETURNING id",
                (
                    url["name"],
                    datetime.now(),
                ),
            )
            id = cur.fetchone()[0]
            url["id"] = id
        self.conn.commit()

    def clear(self):
        with self.conn.cursor() as cur:
            cur.execute("TRUNCATE urls")
        self.conn.commit()
