from huey import SqliteHuey

huey = SqliteHuey("megaman", filename="/data/queuedb/huey.db")
