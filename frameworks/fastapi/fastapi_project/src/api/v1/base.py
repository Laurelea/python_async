"""
.get() — получение данных с сервера, но не для их изменения. Может передавать в адресе запроса параметры, например, для фильтрации данных.
.post() — создание новых объектов. Служит для передачи чувствительных данных на сервер: например, логина и пароля.
.put() — полное обновление объектов в БД, а именно — замещение старого объекта новым.
.patch() — частичное обновление объектов БД.
.delete() — удаление объектов.
.options() — получение параметров HTTP-соединения и другой служебной информации.
.head() — получение заголовков ответа. Это аналог метода GET, только без тела ответа.
.trace() — диагностика и получение сведений о том, какую информацию промежуточные серверы добавляют или изменяют в запросе.
"""
import sys
from typing import Union, Optional, List
from fastapi.responses import PlainTextResponse
from fastapi import APIRouter, Response, Request
from pydantic import BaseModel
from fastapi.exceptions import RequestValidationError

# Объект router, в котором регистрируем обработчики
router = APIRouter()


# @router.get('/')
@router.options('')
async def root_handler():
    # return {'version': 'v1'}
    return


@router.get('/info')
async def info_handler():
    return {
        'api': 'v1',
        'python': sys.version_info
    }


# @router.get('/{action}')
# async def action_handler(action):
#     return {
#         'action': action
#     }


@router.get('/filter')
async def filter_handler(
        param1: str,  # обязательный параметр
        param2: Optional[int] = None
        # Чтобы сделать параметр необязательным, необходимо задать ему дефолтное значение или None, обернув аннотацию типа в Optional[...]
) -> dict[str, Union[str, int, None]]:
    return {
        'action': 'filter',
        'param1': param1,
        'param2': param2
    }


# возвращаем простой текст вместо json
@router.get('/text', response_class=PlainTextResponse)
async def main():
    return 'Custom text for test'


# Название хэндлера и возвращаемый тип данных не кореллируют между собой :)
# возвращаем xml вместо json
@router.get('/xml-data/')
def get_legacy_data():
    data = """<?xml version="1.0" encoding="UTF-8"?>
    <note>
      <to>Tove</to>
      <from>Jani</from>
      <heading>Reminder</heading>
      <body>Don't forget me this weekend!</body>
    </note>
    """
    return Response(content=data, media_type='application/xml')


# Например, вот так можно проверить входящий JSON-объект, передаваемый через метод POST с помощью Pydantic:
# Этот код будет принимать данные в формате JSON через метод POST с полями title, pub_year, tags. Каждый тип поля будет провалидирован.
class CollectionItem(BaseModel):
    title: str
    pub_year: int
    tags: List[str] = []


@router.post('/collection/', response_model=CollectionItem)
async def create_item(item: CollectionItem):
    return item

# пример кастомного хэндлера ошибок валидации
# @app.exception_handler(RequestValidationError)
# async def handle_error(request: Request, exc: RequestValidationError) -> PlainTextResponse:
#     return PlainTextResponse(str(exc.errors()), status_code=400)
