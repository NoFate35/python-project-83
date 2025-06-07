import pytest
from page_analyzer.app import get_db_connection
from page_analyzer import app
import responses


@pytest.fixture()
def test_app():
    test_app = app
    test_app.config.update({
        "TESTING": True,
    })
    conn, repo = get_db_connection()
    repo.clear_tables()
    #print('CLEAR TABLES')
    yield test_app
    repo.clear_tables()
    conn.close()



@pytest.fixture()
def client(test_app):
    return test_app.test_client()


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


def test_checks_for_flash(client):
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


@responses.activate
def test_checks(client):
    responses.add(
        responses.GET,
        'http://rightcheck.ru',
        body = '''<h1>yyyy</h1>
        			  <title>tatle</title>
        			  <meta name="description" content="contemp">''',
        status=200,
    )
    responses.add(
        responses.GET,
        'http://wrongcheck.ru',
        body = '''<h1>yyyy</h1>
        			  <title>tatle</title>
        			  <meta name="wrongTag" content="contemp">''',
        status=200,
    )
    responses.add(
        responses.GET,
        'http://wrongstatus.ru',
        status=500,
    )
    _ = client.post('/urls', 
        data = {"url": 'http://rightcheck.ru'},
        follow_redirects=True)
    wright_response = client.post('/urls/1/checks',
        follow_redirects=True)
    #print("response.tttext", response.text.split())
    assert "200" in wright_response.text
    assert "yyyy" in wright_response.text
    assert "tatle" in wright_response.text
    assert "contemp" in wright_response.text
    _ = client.post('/urls', 
        data = {"url": 'http://wrongstatus.ru'},
        follow_redirects=True)
    wrong_status_response = client.post('/urls/2/checks',
        follow_redirects=True)
    assert "Произошла ошибка при проверке" in wrong_status_response.text
    _ = client.post('/urls', 
        data = {"url": 'http://wrongcheck.ru'},
        follow_redirects=True)
    wright_response = client.post('/urls/3/checks',
        follow_redirects=True)
    assert "contemp" not in wright_response.text
    