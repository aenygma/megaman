#
# This shared file contains the tasks that will be run by huey.
#

import time

from config import huey
from pymegatools import Megatools

# add an item
@huey.task()
def start_consumer(url, name=None):
    """
    add an item to download queue
    """

    mega = Megatools()
    mega.download(url)

    return


# list items in queue
def list_items():
    pass

@huey.task()
# test task for diagnostics
def diag_echo(msg):
    """
    echo back a message
    """

    print("> Consumer: %s\n > Sleeping for 5 seconds" % msg)
    time.sleep(5)

@huey.task()
def diag_add(a,b):
    return a+b
