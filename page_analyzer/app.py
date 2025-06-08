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


def get_repository_connection():
	connection = psycopg2.connect(DATABASE_URL)
	repository = UrlRepository(connection)
	return connection, repository


@app.route("/")
def get_index():
    return render_template("index.html", url={"name": ""})


@app.route("/urls")
def urls_index():
    connection, repository = get_repository_connection()
    urls_checks = repository.get_url_content()
    connection.close()
    return render_template("urls.html", urls_checks=urls_checks)


@app.route("/urls/<int:url_id>")
def url_show(url_id):
    connection, repository = get_repository_connection()
    messages = get_flashed_messages(with_categories=True)
    url = repository.find_url(url_id)
    url_checks = repository.get_checks_content(url_id)
    connection.close()
    if url is None:
        return render_template("not_found.html")
    return render_template("show.html",
                           url=url,
                           checks=url_checks,
                           messages=messages
                           )


@app.route("/urls", methods=["POST"])
def urls_add():
    connection, repository = get_repository_connection()
    data = request.form.to_dict()
    normal_url = validate(data["url"])
    if normal_url:
        url = {"name": normal_url}
        exist_id = repository.exist_url(url)
        if exist_id:
            flash("Страница уже существует", "info")
            url_id = exist_id
        else:
            repository.save_url(url)
            url_id = url["id"]
            flash("Страница успешно добавлена", "success")
        connection.close()
        return redirect(url_for("url_show", url_id=url_id), code=302)
    flash("Некорректный URL", "error")
    return render_template("index.html", url={"name": data["url"]}), 422


@app.route('/urls/<int:url_id>/checks', methods=['POST'])
def url_checking(url_id):
    connection, repository = get_repository_connection()
    url_check = {'url_id': url_id,
                        'status_code': '',
                        'title': '',
                        'h1': '',
                        'description': ''}
    url = repository.find_url(url_id)
    url_response = get_response(url)
    if url_response:
        make_check(url_check, url_response)
        repository.save_check(url_check)
        flash("Страница успешно проверена", "success")
    else:
        flash("Произошла ошибка при проверке", "error")
    connection.close()
    return redirect(url_for("url_show", url_id=url_id), code=302)
