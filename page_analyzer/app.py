import psycopg2
import os
from flask import Flask, render_template, request, flash, redirect, url_for, get_flashed_messages
from dotenv import load_dotenv
from page_analyzer.repository import UrlRepository
from page_analyzer.validator import validate


app = Flask(__name__)

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(postgresql://ivan:O2lGqomgjg5HYHQL7DJeo51S73P46ivf@dpg-d0fm5mq4d50c73f25ce0-a.oregon-postgres.render.com/flaskdb_ns0p)

repo = UrlRepository(conn)
debug = app.logger.debug

@app.route('/')
def get_index():
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html',  url={}, messages=messages)

@app.route("/urls")
def urls_index():
        urls = repo.get_content()
        return render_template("urls.html",urls=urls)


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

    errors = validate(data)

    if not errors:
        url = {"name": data["url"]}
        exist_id = repo.exist(url)
        print("exist id", exist_id)
        if exist_id:
            flash("Страница уже существует")
            return redirect(url_for('url_show', id=exist_id))
        repo.save(url)
        id = url['id']
        flash("Страница успешно добавлена", "success")
        return redirect(url_for('url_show', id=id))

    flash("Некорректный URL")
    return render_template('index.html',  url=data['name'])
    