from datetime import datetime

from psycopg2.extras import DictCursor


class UrlRepository:
    def __init__(self, conn):
        self.conn = conn

    def get_url_content(self):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT "
                        "DISTINCT ON (id) urls.id AS id, "
                        "urls.name AS name, "
                        "checks.created_at AS last_date, "
                        "checks.status_code "
                        "FROM urls LEFT JOIN url_checks AS checks "
                        "ON urls.id = checks.url_id "
                        "ORDER BY id DESC, last_date DESC;")
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
                "INSERT INTO urls (name, created_at) "
                "VALUES (%s, %s) RETURNING id",
                (
                    url["name"],
                    datetime.now(),
                ),
            )
            url_id = cur.fetchone()[0]
            url["id"] = url_id
        self.conn.commit()

    def save_check(self, url_check):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO url_checks (url_id,"
                                        "status_code,"
                                        "h1,"
                                        "title,"
                                        "description,"
                                        "created_at) \
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                (
                    url_check['url_id'],
                    url_check['status_code'],
                    url_check['h1'],
                    url_check['title'],
                    url_check['description'],
                    datetime.now(),
                ),
            )
        self.conn.commit()

    def get_checks_content(self, url_id):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT *"
                        "FROM url_checks WHERE url_id = %s "
                        "ORDER BY id DESC;", (url_id,))
            return [dict(row) for row in cur]

    def clear_tables(self):
        with self.conn.cursor() as cur:
            cur.execute(
                "TRUNCATE urls RESTART IDENTITY CASCADE;"
                "TRUNCATE url_checks RESTART IDENTITY;"
            )
        self.conn.commit()
