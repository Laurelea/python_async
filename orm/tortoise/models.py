from tortoise.models import Model
from tortoise import fields


class Book(Model):
    id = fields.IntField(pk=True)
    title = fields.TextField()
    pages = fields.IntField()
    create_date = fields.DatetimeField(autho_now=True)
    author = fields.ForeignKeyField(
        "models.Author", related_name="books"
    )

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Book(title='%s')" % (self.title,)


class Author(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    books: fields.ReverseRelation["Book"]

    def __str__(self):
        return "Author(name='%s')" % (self.name,)

    def __repr__(self):
        return self.__str__()