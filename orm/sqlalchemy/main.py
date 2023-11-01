import asyncio

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.future import select

from models import Author, Book
from models import Base


async def main():
    # Замените DSN на свои значения
    DSN = "postgresql+asyncpg://app:123qwe@localhost:5432/movies_database"

    engine = create_async_engine(DSN, echo=True, future=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # Дальнейшие участки кода, кроме импортов, располагайте в функции main

    # SQLAlchemy использует паттерн UnitOfWork
    # Программист явным образом открывает сессию и добавляет в неё необходимые изменения, которые должны отправиться в БД

    async with AsyncSession(engine) as session:
        # Воспользуемся классом Author, чтобы создать новую запись
        author = Author(name='Азимов А.')
        # Добавляем изменения в сессию
        session.add(author)
        # Можно посмотреть, какие записи изменятся или создадутся в рамках сессии
        print(session.dirty)
        print(session.new)
        # Отправляем изменения в базу данных
        await session.commit()

        # Прочитать запись
        first_author = await session.get(Author, 1)
        print(first_author)

        ## Создать несколько записей
        books = (
            Book(title=title, author=author, pages=50)
            for title in ['Мать-земля', 'Стальные пещеры', 'Обнажённое солнце']
        )
        session.add_all(books)
        await session.commit()

        # Получить несколько записей
        query = select(Book).join(Book.author).where(Author.name == "Азимов А.")
        books = (await session.scalars(query)).all()
        print(books)

        # Агрегировать данные — посчитать количество страниц во всех книгах в базе данных
        pages_count = (await session.execute(select(func.sum(Book.pages).label('pages_sum')))).scalar()
        print(pages_count)

        # Создать одновременно запись и связанные объекты
        author2 = Author(name='Гоголь Н.В.',
                         books=[Book(title='Мёртвые души. Том 1', pages=300),
                                Book(title='Мёртвые души. Том 2', pages=170)])
        session.add(author2)
        await session.commit()

        # Список книг по авторам
        books_and_author = (await session.execute(
            select(Author.name, func.count(Book.title)).group_by(Author.name))
                            ).all()
        print(books_and_author)

        # Поиск наибольшего значения в отфильтрованном запросе
        max_pages = (await session.execute(select(func.max(Book.pages)).filter(Book.title.like("%души%")))).scalar()
        print(max_pages)

        # Удалить запись
        await session.delete(books[0])
        await session.commit()

    # Перед закрытием приложения нужно закрыть все соединения с базой данных
    await engine.dispose()


asyncio.run(main())