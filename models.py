import peewee


db = peewee.SqliteDatabase('data.db')


class Users(peewee.Model):
    id = peewee.IntegerField(primary_key=True)
    username = peewee.CharField(unique=True)
    chat_id = peewee.IntegerField(unique=True)
    name = peewee.CharField()
    surname = peewee.CharField()
    is_admin = peewee.BooleanField(default=False)
    is_teacher = peewee.BooleanField(default=False)

    class Meta:
        database = db
