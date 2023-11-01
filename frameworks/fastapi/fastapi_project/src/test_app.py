from fastapi.testclient import TestClient

# Импортируем сюда переменную приложения app, инициализированную в файле app.py
from main import app

client = TestClient(app)


def test_read_main():
    response = client.get('/api/v1/text')
    # Проверяем, что запрос успешно обработан...
    assert response.status_code == 200
    # ... и что текст сообщения при доставке не пострадал.
    # assert response.json() == {'msg': 'Hello World'}
    assert response.text == 'Custom text for test'
