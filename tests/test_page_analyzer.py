import pytest
from page_analyzer import app

@pytest.fixture()
def test_app():
    test_app = app
    test_app.config.update({
        "TESTING": True,
    })

    yield test_app


@pytest.fixture()
def client(test_app):
    return test_app.test_client()


@pytest.fixture()
def runner(test_app):
    return test_app.test_cli_runner()

def test_request_example(client):
    response = client.get("/")
    assert '<h1 class="display-3">Анализатор страниц</h1>' in response.text

def test_urls_index_post(client):
    response = client.post('/urls', data = {
        "url": 'HttpS://Ya.ru'
    })
    assert "Некорректный URL" in response.text

