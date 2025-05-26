import os

import psycopg2
from dotenv import load_dotenv
from flask import (
    Flask,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for,
)

from page_analyzer.repository import UrlRepository
from page_analyzer.validator import validate

app = Flask(__name__)

load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

DATABASE_URL = os.getenv("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)

repo = UrlRepository(conn)
app.logger.setLevel("DEBUG")
debug = app.logger.debug


@app.route("/")
def get_index():
    return render_template("index.html", url={"name": ""})


@app.route("/urls")
def urls_index():
    urls = repo.get_content()
    return render_template("urls.html", urls=urls)


@app.route("/urls/<int:id>")
def url_show(id):
    messages = get_flashed_messages(with_categories=True)
    url = repo.find(id)
    if url is None:
        return render_template("not_found.html")
    return render_template("show.html", url=url, messages=messages)


@app.route("/urls", methods=["POST"])
def urls_post():
    data = request.form.to_dict()
    normal_url = validate(data["url"])
    if normal_url:
        url = {"name": normal_url}
        exist_id = repo.exist(url)
        if exist_id:
            debug("test urrrl exist %s", url)
            flash("Страница уже существует", "info")
            return redirect(url_for("url_show", id=exist_id))
        repo.save(url)
        debug("test urrrl not exist %s", url)
        id = url["id"]
        flash("Страница успешно добавлена", "success")
        return redirect(url_for("url_show", id=id))
    flash("Некорректный URL", "error")
    return render_template("index.html", url={"name": data["url"]})
