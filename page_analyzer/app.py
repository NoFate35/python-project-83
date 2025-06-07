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
from page_analyzer.supportive_functions import (
    get_response,
    make_check,
    validate,
)

app = Flask(__name__)

load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

DATABASE_URL = os.getenv("DATABASE_URL")



app.logger.setLevel("DEBUG")
debug = app.logger.debug

#conn = psycopg2.connect(DATABASE_URL)
#repo = UrlRepository(conn)

def get_db_connection():
	conn = psycopg2.connect(DATABASE_URL)
	repo = UrlRepository(conn)
	return conn, repo


@app.route("/")
def get_index():
    return render_template("index.html", url={"name": ""})


@app.route("/urls")
def urls_index():
    conn, repo = get_db_connection()
    urls_checks = repo.get_url_content()
    conn.close()
    return render_template("urls.html", urls_checks=urls_checks)


@app.route("/urls/<int:url_id>")
def url_show(url_id):
    conn, repo = get_db_connection()
    messages = get_flashed_messages(with_categories=True)
    url = repo.find_url(url_id)
    url_checks = repo.get_checks_content(url_id)
    conn.close()
    if url is None:
        return render_template("not_found.html")
    return render_template("show.html",
                           url=url,
                           checks=url_checks,
                           messages=messages
                           )


@app.route("/urls", methods=["POST"])
def urls_post():
    conn, repo = get_db_connection()
    data = request.form.to_dict()
    normal_url = validate(data["url"])
    if normal_url:
        url = {"name": normal_url}
        exist_id = repo.exist_url(url)
        if exist_id:
            flash("Страница уже существует", "info")
            url_id = exist_id
        else:
            repo.save_url(url)
            url_id = url["id"]
            flash("Страница успешно добавлена", "success")
        conn.close()
        return redirect(url_for("url_show", url_id=url_id), code=302)
    flash("Некорректный URL", "error")
    return render_template("index.html", url={"name": data["url"]}), 422


@app.route('/urls/<int:url_id>/checks', methods=['POST'])
def url_checking(url_id):
    conn, repo = get_db_connection()
    url_check = {'url_id': url_id,
                        'status_code': '',
                        'title': '',
                        'h1': '',
                        'description': ''}
    url = repo.find_url(url_id)
    url_response = get_response(url)
    if url_response:
        make_check(url_check, url_response)
        repo.save_check(url_check)
        flash("Страница успешно проверена", "success")
    else:
        flash("Произошла ошибка при проверке", "error")
    conn.close()
    return redirect(url_for("url_show", url_id=url_id), code=302)
