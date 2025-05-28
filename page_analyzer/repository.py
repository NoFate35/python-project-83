from datetime import datetime

from psycopg2.extras import DictCursor


class UrlRepository:
    def __init__(self, conn):
        self.conn = conn

    def get_url_content(self):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM urls ORDER BY created_at DESC")
            return [dict(row) for row in cur]

    def exist_url(self, url):
        name = url["name"]
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM urls WHERE name = %s", (name,))
            row = cur.fetchone()
            return dict(row)["id"] if row else None

    def find_url(self, url_id):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM urls WHERE id = %s", (url_id,))
            row = cur.fetchone()
            return dict(row) if row else None

    def save_url(self, url):
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

    def clear_tables(self):
        with self.conn.cursor() as cur:
            cur.execute("TRUNCATE urls")
            cur.execute("TRUNCATE url_checks")
        self.conn.commit()
    
    def save_check(self, url_check):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO url_checks (url_id, created_at) \
                VALUES (%s, %s) RETURNING id",
                (
                    url_check['url_id'],
                    datetime.now(),
                ),
            )
            #id = cur.fetchone()[0]
            #url_check["id"] = id
        self.conn.commit()
    
    def get_checks_content(self, url_id):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM url_checks WHERE url_id = %s " \
            "ORDER BY created_at DESC;", (url_id,))
            return [dict(row) for row in cur]