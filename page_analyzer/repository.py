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
            id = cur.fetchone()[0]
            url["id"] = id
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
        self.conn.commit()

    def get_checks_content(self, url_id):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT id, status_code, h1, description, created_at "
                        "FROM url_checks WHERE url_id = %s "
                        "ORDER BY created_at DESC;", (url_id,))
            return [dict(row) for row in cur]

    def clear(self):
        with self.conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS urls, url_checks;")
            cur.execute("CREATE TABLE urls (id int PRIMARY KEY GENERATED ALWAYS AS IDENTITY, name varchar (255), created_at TIMESTAMP;")
            cur.execute("CREATE TABLE url_checks (id int PRIMARY KEY GENERATED ALWAYS AS IDENTITY, url_id int REFERENCES urls(id), status_code varchar (10), h1 varchar (255), description text, created_at TIMESTAMP);")
        self.conn.commit()
