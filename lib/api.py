#
# Interface to interact with the whole system as a whole
#

import tasks

def add_item(url):
    """
    add a item to download
    """

    # add it to history db
    item_id = history_db.add(url)

    # start consumer
    # XXX: set done iff no failures or errors
    pipeline = tasks.start_consumer.s(url).then(history_db.done, item_id)

    # set task status to done in history db
    #  set blocking or add this as callback

    huey.enqueue(pipeline)

    return
