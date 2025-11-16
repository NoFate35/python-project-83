## Tests and linter status:
[![Build](https://github.com/NoFate35/python-project-83/actions/workflows/build.yml/badge.svg)](https://github.com/NoFate35/python-project-83/actions/workflows/build.yml)
[![Actions Status](https://github.com/NoFate35/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/NoFate35/python-project-83/actions)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=NoFate35_python-project-83&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=NoFate35_python-project-83)
## Skill badges
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Jinja](https://img.shields.io/badge/jinja-white.svg?style=for-the-badge&logo=jinja&logoColor=black)
![Pytest](https://img.shields.io/badge/pytest-%23ffffff.svg?style=for-the-badge&logo=pytest&logoColor=2f9fe3)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)

# About project
The link to this training project will be available for 25 days, starting from 06/13/2025: <a href="https://python-project-83-production-1113.up.railway.app">Page Analyzer</a>
### Purpose
Page analyzer is a full-fledged application based on the Flask framework. Here the basic principles of building modern sites on the MVC architecture are worked out: work with routing, request handlers and a template engine, interaction with the database.
### Description
<a href="https://python-project-83-production-1113.up.railway.app">Page Analyzer</a> – this is a website that analyzes the specified pages for SEO suitability, similar to <a href="https://pagespeed.web.dev/">PageSpeed Insights</a>:<p><img src="https://cdn2.hexlet.io/derivations/image/original/eyJpZCI6ImRiYzE2ZTNhYjgxMjI1NzdmMTM1ZDQzMjVkZmQ1YWJhLnBuZyIsInN0b3JhZ2UiOiJjYWNoZSJ9?signature=4874cc79b8e3f1a0288cb0d59b09b9129ee0ad591958711786ee0d4f5bad3f8a" title="" alt="Проект Хекслета Анализатор страниц" class="px-2 px-md-3 px-lg-4 px-xl-5 img-fluid" loading="lazy">
<img src="https://cdn2.hexlet.io/derivations/image/original/eyJpZCI6ImM5Mzk5Y2MzY2ZkNWUzNTI0MTE4OTYwYTZkNzEyYWVkLnBuZyIsInN0b3JhZ2UiOiJjYWNoZSJ9?signature=508d9cc44a9cc3880c828c4775df02e09ec9224fe5e84f52325035cc891da4a2" title="" alt="Анализатор страниц" class="px-2 px-md-3 px-lg-4 px-xl-5 img-fluid" loading="lazy">
<img src="https://cdn2.hexlet.io/derivations/image/original/eyJpZCI6IjE2NWRmOGYzYjM2NGUyMTNhOWU1M2E3ZDJmNGQwYjNmLnBuZyIsInN0b3JhZ2UiOiJjYWNoZSJ9?signature=79858c156ec370e5a4a8180a4e26d62a7aef546880d53a823df32cc4e1670a6c" title="" alt="Анализатор страниц" class="px-2 px-md-3 px-lg-4 px-xl-5 img-fluid" loading="lazy"></p>
### Installation
To work with the project must be installed:
* the __uv__ project manager;
* __postgresql__ with "py_flaskdb" database whith no password;

__.env__ file consist of:
```
DATABASE_URL = 'postgresql:///py_flaskdb'
SECRET_KEY = 'verysecretkeyyy'
```
then:
```
git clone https://github.com/NoFate35/python-project-83.git
cd python-project-83
uv sync
make dev
make test
```
URL to try: _http://ya.ru_
