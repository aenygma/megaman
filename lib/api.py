#
# Interface to interact with the whole system as a whole
#

import tasks
from models import Entries
from config import huey

def init():
    """
    generic setup stuff
    """

    # create db tables if not exist
    Entries.create_table()

@huey.task()
def _entry_done(item_id):
    """
    database helper to set completed to 1
    """

    entry = Entries.get(item_id)
    entry.completed = 1
    entry.save()

def add_item(url, name, **kwargs):
    """
    add a item to download
    """

    # add it to history db
    entry = Entries.create(
                url = url,
                name = name,
                completed = 0,
                inprogress = 0,
                refurl = kwargs.get("refurl", None))
    item_id = entry.save()

    # start consumer
    # XXX: set done iff no failures or errors
    pipeline = (tasks.start_consumer.s(url).then(
                _entry_done, item_id))

    # set task status to done in history db
    #  set blocking or add this as callback

    huey.enqueue(pipeline)

    return
