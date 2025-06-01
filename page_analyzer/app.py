import os
from bs4 import BeautifulSoup
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
from page_analyzer.validator import validate, get_response

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
    urls_checks = repo.get_url_content()
    return render_template("urls.html", urls_checks=urls_checks)


@app.route("/urls/<int:url_id>")
def url_show(url_id):
    messages = get_flashed_messages(with_categories=True)
    url = repo.find_url(url_id)
    url_checks = repo.get_checks_content(url_id)
    if url is None:
        return render_template("not_found.html")
    return render_template("show.html",
                           url=url,
                           checks=url_checks,
                           messages=messages
                           )


@app.route("/urls", methods=["POST"])
def urls_post():
    data = request.form.to_dict()
    normal_url = validate(data["url"])
    if normal_url:
        url = {"name": normal_url}
        exist_id = repo.exist_url(url)
        if exist_id:
            debug("test urrrl exist %s", url)
            flash("Страница уже существует", "info")
            return redirect(url_for("url_show", url_id=exist_id))
        repo.save_url(url)
        url_id = url["id"]
        flash("Страница успешно добавлена", "success")
        return redirect(url_for("url_show", url_id=url_id))
    flash("Некорректный URL", "error")
    return render_template("index.html", url={"name": data["url"]})


@app.route('/urls/<int:url_id>/checks', methods=['POST'])
def url_checking(url_id):
    url_check = {'url_id': url_id}
    url = repo.find_url(url_id)
    url_response = get_response(url)
    if url_response:
        url_check['status_code'] = url_response.status_code
        html_doc = url_response.text
        
        soup = BeautifulSoup(html_doc, 'html.parser')
        url_title = soup.title
        if url_title:
            url_check['title'] = url_title.string
        else:
            url_check['title'] = None
        url_h1 = soup.h1
        if url_h1:
            url_check['h1'] = url_h1.string
        else:
            url_check['h1'] = None
        url_description = soup.meta
        if url_description['']:
            url_check['description'] = url_h1.string
        else:
            url_check['h1'] = None
            debug('URL_TITLE %s', url_title.string)
        repo.save_check(url_check)
        flash("Страница успешно проверена", "success")
    else:
        flash("Произошла ошибка при проверке", "error")
    return redirect(url_for("url_show", url_id=url_id))
