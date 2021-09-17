#
# Interface to interact with the whole system as a whole
#

import tasks
from models import Entries

def init():
    """
    generic setup stuff
    """

    # create db tables if not exist
    Entries.create_table()


def _entry_done(item_id):
    """
    database helper to set completed to 1
    """

    entry = Entries.get(item_id)
    entry.completed = 1
    entry.save()

def add_item(url, name):
    """
    add a item to download
    """

    # add it to history db
    entry = entries.create(
                url = url,
                name = kwargs.get("name", None),
                completed = 0,
                inprogress = 0,
                refurl = kwargs.get("refurl", None))

    # start consumer
    # XXX: set done iff no failures or errors
    pipeline = tasks.start_consumer.s(url).then(
                _entry_done, item_id)

    # set task status to done in history db
    #  set blocking or add this as callback

    huey.enqueue(pipeline)

    return
