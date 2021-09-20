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

@huey.task()
def _entry_inprogress(item_id):
    """
    database helper to set in_progress to 1
    """

    entry = Entries.get(item_id)
    entry.in_progress = 1
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
    pipeline = (_entry_inprogress.s(item_id)
                .then(tasks.start_consumer,url)
                .then(_entry_done, item_id))

    # set task status to done in history db
    #  set blocking or add this as callback

    huey.enqueue(pipeline)

    return

def list_items(inprogress=None, completed=None):
    """
    list items
    """

    if inprogress is not None:
        inprogress = True
    else:
        inprogress = False


    if completed is not None:
        completed = True
    else:
        completed = False

    return Entries.get(inprogress=inprogress, completed=completed)
