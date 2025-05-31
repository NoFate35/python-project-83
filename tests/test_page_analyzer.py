import pytest
from page_analyzer.app import repo
from page_analyzer import app
import pook

@pytest.fixture()
def test_app():
    test_app = app
    test_app.config.update({
        "TESTING": True,
    })
    repo.clear_tables()
    print('CLEAR TABLES')
    yield test_app
    repo.clear_tables()



@pytest.fixture()
def client(test_app):
    return test_app.test_client()


@pytest.fixture()
def runner(test_app):
    return test_app.test_cli_runner()




def test_request_example(client):
    response = client.get("/")
    assert '<h1 class="display-3">Анализатор страниц</h1>' in response.text


def test_urls_index_post_error(client):
    response = client.post('/urls', data = {
        "url": 'HttpS//Ya.ru'
    })
    assert "Некорректный URL" in response.text


def test_urls_index_post(client):
    response = client.post('/urls', 
        data = {"url": 'HttpS://Ya.ru'},
        follow_redirects=True)
    assert "Страница успешно добавлена" in response.text

    response = client.post('/urls', 
        data = {"url": 'HttpS://Ya.ru'},
        follow_redirects=True)
    assert "Страница уже существует" in response.text


def test_checks(client):
    _ = client.post('/urls', 
        data = {"url": 'HttpS://Ya.ru'},
        follow_redirects=True)
    response = client.post('/urls/1/checks',
        follow_redirects=True)
    assert "Страница успешно проверена" in response.text

def test_urls_list(client):
    _ = client.post('/urls', 
        data = {"url": 'HttpS://Ya.ru'},
        follow_redirects=True)
    response = client.get('/urls')
    assert "https://Ya.ru" in response.text

@pook.get('http://yopppppp.ru', reply=200)
@pook.get('http://ruuurro.ru', reply=500)
def test_status_code(client):
    _ = client.post('/urls', 
        data = {"url": 'http://yopppppp.ru'},
        follow_redirects=True)
    response = client.post('/urls/1/checks',
        follow_redirects=True)
    assert "200" in response.text
    _ = client.post('/urls', 
        data = {"url": 'http://ruuurro.ru'},
        follow_redirects=True)
    response = client.post('/urls/2/checks',
        follow_redirects=True)
    assert "Произошла ошибка при проверке" in response.text
    