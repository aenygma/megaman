import peewee

db = peewee.SqliteDatabase("/data/history.db")

class Entries(peewee.Model):

    name = peewee.TextField()
    url = peewee.TextField()
    refurl = peewee.TextField(null=True)
    notes = peewee.TextField(null=True)
    completed = peewee.IntegerField(default=0)
    inprogress = peewee.IntegerField(default=0)
    link_valid = peewee.IntegerField(default=1)
    deprecated_by = peewee.IntegerField(default=0)

    class Meta:
        database = db
        db_table = 'entries'
