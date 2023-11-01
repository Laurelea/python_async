from sqlalchemy import Column, DateTime, ForeignKey, func, Integer, String
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Book(Base):
    # Имя таблицы в базе данных
    __tablename__ = "book"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    pages = Column(Integer)
    create_date = Column(DateTime, server_default=func.now())
    # Внешний ключ на таблицу Автор
    author_id = Column(ForeignKey("author.id"))
    # Связь с объектом класса Автор
    author = relationship("Author", back_populates="books")

    # Значение `eager_defaults` указывает ORM немедленно получать значение
    # сгенерированных сервером значений по умолчанию для INSERT или UPDATE.
    __mapper_args__ = {"eager_defaults": True}

    # Чтобы сделать консольный вывод более информативным, добавим __repr__
    def __repr__(self):
        return "Book(title='%s')" % (self.title,)


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    # Описываем атрибут для связи автора и его книг
    books = relationship("Book")

    def __repr__(self):
        return "Author(name='%s')" % (self.name,)