#!/usr/bin/env python
# pylint: disable=W0603,I1101

"""
    This module is to help test a process
"""

import time
import signal

import setproctitle

VALUE = None
PIPE = "/tmp/.megatools.pipe"

def sig_handler(signo, frame):
    """ signal handler """

    global VALUE
    print("Caught signal: %d" % signo, frame)
    with open(PIPE, 'r') as filehandle:
        VALUE = filehandle.read()

    print("Value is now: ", VALUE)

def main():
    """ main() """

    signal.signal(signal.SIGUSR1, sig_handler)
    signal.signal(signal.SIGHUP, sig_handler)

    while True:
        time.sleep(1)
    print('done')

if __name__ == "__main__":
    setproctitle.setproctitle('megatools')
    main()
