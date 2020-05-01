#!/usr/bin/env python
# pylint: disable=W0703,C0103,W0603

"""
This module is to manage a schedule of times and speeds
that Megatools downloader should run at.
"""

import os
import sys
import time as ptime
import signal
import configparser

import click
import schedule

from daemonize import Daemonize

import utils

PROC_NAME = __file__[:-3]
MEGA_PROC = "megatools"
CONFIG_FILE = "sched.ini"
CONFIG_PROFILE = "normal"
DAEMON_PIDFILE = "/tmp/%s.pid" % PROC_NAME
DAEMON_PIPE = "/tmp/.%s.pipe" % MEGA_PROC
DAEMON_BAIL_FLAG = False

def validate():
    """ validate configs """

    # Check if megatools is running
    if utils.kill(MEGA_PROC):
        print("Megatools cli is not running.")
        sys.exit(1)
    return True

def run_schedules():
    """ run evertyhing """

    global DAEMON_BAIL_FLAG
    def kick_downloader(speed):
        """ write speed and signal dowloader to update """

        with open(DAEMON_PIPE, 'w') as filehandle:
            filehandle.write(speed)

        # if running, signal to update config
        if megatools_status:
            log.info("sending signal to megatools")
            utils.kill("megatools", signal.SIGHUP)

    def sig_handler(signo, frame):
        global DAEMON_BAIL_FLAG
        msg = ("Caught signal: %d | frame: " % signo)  + str(frame)

        #print(msg)
        with open(DAEMON_PIPE, 'w') as pipe:
            pipe.write(msg+ " | " + str(DAEMON_BAIL_FLAG)+"\n")
        if signo == signal.SIGTERM:
            DAEMON_BAIL_FLAG = True

    #signal.signal(signal.SIGUSR1, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)
    #signal.signal(signal.SIGWINCH, sig_handler)

    # begin work
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    log.debug("Dir: %s", os.getcwd())

    try:
        for (ttime, speed) in config[CONFIG_PROFILE].items():
            time_str = "%s:%s" % (ttime[0:2], ttime[2:])
            log.debug("> %s", time_str)
            schedule.every().day.at(time_str).do(kick_downloader, speed=speed)
            #ptime.sleep(1)
    except Exception as e:
        log.error(e)

    # now wait.
    # TODO: this needs to be refreshed when entries added/removed
    while not DAEMON_BAIL_FLAG:
        schedule.run_pending()
        ptime.sleep(1)

    with open(DAEMON_PIPE, 'w') as pipe:
        pipe.write("done")


#   ____ _     ___                      _
#  / ___| |   |_ _|   ___ _ __ ___   __| |___
# | |   | |    | |   / __| '_ ` _ \ / _` / __|
# | |___| |___ | |  | (__| | | | | | (_| \__ \
#  \____|_____|___|  \___|_| |_| |_|\__,_|___/

@click.group(name="CLI", help="Manage Megatools downloader schedule")
def cli():
    """ dummy function for click argument parsing """
    return

@cli.command(name='new', help="New/Edit schedule entry")
@click.argument('time')
@click.argument('speed')
def new_sched_entry(time, speed):
    """ new schedule entry """

    # validate time
    try:
        time = int(time)
        if ((time < 0) or (time > 2400)):
            raise IndexError
    except ValueError as exc:
        click.echo("Error: Time must be an Integer. " + str(exc))
    except IndexError as exc:
        click.echo("Error: Time must be between 0 and 2400. " + str(exc))
    except Exception as exc:
        click.echo("Error: WTF did you do? " + str(exc))

    # validate speed
    try:
        speed = int(speed)
        if ((speed < 1) or (speed > 1000)):
            raise IndexError
    except ValueError as exc:
        click.echo("Error: Speed must be an Integer. " + str(exc))
    except IndexError as exc:
        click.echo("Error: Speed must be between 0 and 1000. " + str(exc))
    except Exception as exc:
        click.echo("Error: WTF did you do? " + str(exc))

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    config.set(CONFIG_PROFILE, '%04.f' % int(time), str(speed))

    with open(CONFIG_FILE, 'w') as filehandle:
        config.write(filehandle)

@cli.command(name='list', help="List schedule entries")
def list_sched():
    """ list schedule entries """

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    print()
    print("Time", "\t", "Speed")
    print("====", "\t", "=====")
    for (time, speed) in config[CONFIG_PROFILE].items():
        print(time, "\t", speed)
    print()

@cli.command(name='remove', help="Delete schedule entry")
@click.argument('time')
def delete_schedule(time):
    """ delete schedule entry """

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    # remove
    if not config.remove_option(CONFIG_PROFILE, time):
        click.echo("Error: Couldn't find the entry.")
        return

    with open(CONFIG_FILE, 'w') as filehandle:
        config.write(filehandle)
    click.echo("Removed entry for time: %s" % time)


@cli.command(name="start", help="start the scheduler")
def daemon_start():
    """ Start the scheduling daemon """

    if daemon_status:
        click.echo("> Scheduler already running.")
        return

    try:
        pid = os.fork()
    except OSError as exc:
        click.echo("> Error: " +  str(exc))

    # child
    if pid == 0:
        click.echo("> Trying to start daemon")
        daemon = Daemonize(app="megatools scheduler", pid=DAEMON_PIDFILE,
                           action=run_schedules, verbose=True, foreground=True,
                           logger=log, chdir=os.getcwd())
        daemon.start()
    #parent
    return

@cli.command(name="stop", help="stop the scheduler")
def daemon_stop():
    """ Stop the scheduling daemon """

    if not daemon_status:
        click.echo("> Scheduler not running.")
        return

    # try stopping it
    with open(DAEMON_PIDFILE, 'r') as filehandle:
        error = utils.kill(filehandle.read(), signo=signal.SIGHUP, cat="pid") != 0
    if error:
        click.echo("Couldn't stop scheduler.")

#                  _
#  _ __ ___   __ _(_)_ __
# | '_ ` _ \ / _` | | '_ \
# | | | | | | (_| | | | | |
# |_| |_| |_|\__,_|_|_| |_|

if __name__ == "__main__":
    click.clear()

    # megatools status
    megatools_status = False
    megatools_msg = "Not Running."
    pids = utils.get_pid_by_name(MEGA_PROC)
    # if no error
    if pids:
        megatools_status = True
        megatools_msg = "Running. PID(s): " + ", ".join(pids)

    # mg_sched daemon status
    out, err = utils.check_pidfile(DAEMON_PIDFILE)
    daemon_msg = "Not Running."
    daemon_status = False
    if not err:
        daemon_status = True
        daemon_msg = "Running. PID(s): %s" % str(out)

    # logging
    import logging
    log = logging.getLogger(__name__)
    out_hdlr = logging.StreamHandler(sys.stdout)
    out_hdlr.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
    out_hdlr.setLevel(logging.INFO)
    log.addHandler(out_hdlr)
    log.setLevel(logging.INFO)

    # TODO: Display status: Red/Green Icons?
    print("\n".join([
        r"##############################################################",
        r"#                                         _              _   #",
        r"#   _ __ ___   ___  __ _  __ _   ___  ___| |__   ___  __| |  #",
        r"#  | '_ ` _ \ / _ \/ _` |/ _` | / __|/ __| '_ \ / _ \/ _` |  #",
        r"#  | | | | | |  __/ (_| | (_| | \__ \ (__| | | |  __/ (_| |  #",
        r"#  |_| |_| |_|\___|\__, |\__,_| |___/\___|_| |_|\___|\__,_|  #",
        r"#                  |___/                                     #",
        r"#                                                            #",
    ]))
    print("# MEGA:  ", megatools_msg)
    print("# DAEMON:", daemon_msg)
    print("##############################################################\n")

    # do cli stuff
    cli()
