import psycopg2
import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from page_analyzer.repository import UrlRepository
from page_analyzer.validator import validate


app = Flask(__name__)

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)

repo = UrlRepository(conn)


@app.route('/')
def get_index():
    return render_template('index.html',  url={})

@app.route("/urls")
def urls_index():
        urls = repo.get_content()
        return render_template("urls.html",urls=urls)


@app.route("/urls/<int:id>")
def url_show(id):
    url = repo.find(id)
    if url is None:
        abort(404)
    return render_template("show.html", url=url)


@app.route("/urls", methods=["POST"])
def urls_post():
    data = request.form.to_dict()

    errors = validate(data)

    if not errors:
        url = {"name": data["url"]}
        exist_id = repo.exist(url)
        if exist_id:
            return redirect(url_for('url_show', id=exist_id))
        repo.save(url)
        id = url['id']
        flash("Страница успешно добавлена")
        return redirect(url_for('url_show', id=url.id))

    flash("Некорректный URL")
    return render_template('index.html',  url=data['name'])
    