"""
db functions for mg_sched
"""

import sqlite3 as sqlite

DB_FILE = "./main.db"

# INTERNALS

def _connect(dbfile=DB_FILE):
    """ internal use: connect to db """

    conn = sqlite.connect(dbfile)
    conn.row_factory = dict_factory
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
        for row in conn.execute(sql):
            ret.append(row)
    _close(conn)
    return ret


# get transfers currently in progress
get_in_progress = lambda : _generic_get("select * from entries where inprogress = 1");

# get transfers still pending
get_pending = lambda : _generic_get("select * from entries where completed = 0");


