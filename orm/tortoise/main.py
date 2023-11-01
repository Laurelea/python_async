import sys
import logging

from tortoise import Tortoise, run_async, functions
from models import Author, Book

# Для отображения SQL-запросов в консоли настроим логирование
fmt = logging.Formatter(
    fmt="%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.DEBUG)
sh.setFormatter(fmt)

logger_db_client = logging.getLogger("db_client")
logger_db_client.setLevel(logging.DEBUG)
logger_db_client.addHandler(sh)


async def main():
    # Замените DSN на свои значения
    DSN =  "postgres://app:123qwe@localhost:5432/movies_database"
    await Tortoise.init(
        db_url=DSN,
        modules={'models': ['models']}
    )
    await Tortoise.generate_schemas()
    await Book.all().delete()
    await Author.all().delete()

    # Создание одной записи
    author = Author(name='Азимов А.')
    await author.save()

    # Прочитать запись
    first_author = await Author.get(id=author.id)
    print(first_author)

    # Создать несколько записей
    books = [
        Book(title=title, author=author, pages=50)
        for title in ['Мать-земля', 'Стальные пещеры', 'Обнажённое солнце']
    ]
    await Book.bulk_create(books)
    # В отличии от SQLAlchemy создать сразу несколько записей можно только через bulk_create
    # Из-за некоторых минусов этот метод рекомендуется использовать
    # только для увеличения скорости создания большого количества объектов
    print(books[0].id)  # В частности этот метод не проставляет id созданным записям.

    # Получить несколько записей
    books = await Book.filter(author__name__iexact='Азимов А.')
    print(books)

    # Агрегировать данные — посчитать количество страниц во всех книгах в базе данных
    pages_count = await Book.annotate(pages_count=functions.Sum('pages')).values('pages_count')
    print(pages_count)

    # Создать одновременно запись и связанные объекты
    book2 = await Book.create(author=await Author.create(name='Гоголь Н.В.'), title='Мёртвые души. Том 1', pages=300)
    await book2.save()
    print(book2, book2.author)

    # Список книг по авторам
    books_and_author = await Book.annotate(count=functions.Count('id')).group_by('author__name').values('author__name',
                                                                                                        'count')
    print(books_and_author)

    # Поиск наибольшего значения в отфильтрованном запросе
    max_pages = await Book.filter(title__icontains='души').annotate(max_pages=functions.Max('pages')).values(
        'max_pages')
    print(max_pages)

    # Удалить запись
    await books[0].delete()


run_async(main())
