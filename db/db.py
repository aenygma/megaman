"""
db functions for mg_sched
"""
# pylint: disable=C0103

import sqlite3 as sqlite

DB_FILE = "./main.db"

# INTERNALS

def _connect(dbfile=DB_FILE):
    """ internal use: connect to db """

    conn = sqlite.connect(dbfile)
    conn.row_factory = dict_factory
    conn.text_factory = bytes
    return conn

def _close(conn):
    """ internal use: close the db connection """
    conn.close()

def dict_factory(cursor, row):
    """
    to make rows prettier:
    ref: https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.row_factory
    """
    # pylint: disable=C0103

    d = {}

    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# / INTERNALS

# GENERIC GET
def _generic_get(sql):
    """ generic query for database """

    ret = []
    conn = _connect()
    with conn:
        res = None
        if isinstance(sql, tuple):
            res = conn.execute(*sql)
        else:
            res = conn.execute(sql)

        for row in res:
            ret.append(row)

    _close(conn)
    return ret

## GETTERS ##

# get transfers currently in progress
get_in_progress = lambda: _generic_get("SELECT * FROM entries WHERE inprogress = 1")

# get transfers still pending
get_pending = lambda: _generic_get("SELECT * FROM entries WHERE completed = 0")

## SETTERS ##

# set an entry to completed
set_completed = lambda row_id: _generic_get((
    "UPDATE entries SET inprogress = 0, completed = 1 WHERE id = ?",
    (str(row_id),) ))
