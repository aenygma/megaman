#!/usr/bin/env python
# pylint: disable=W0703,C0103

"""
This module is to manage a schedule of times and speeds
that Megatools downloader should run at.
"""

import sys
import time as ptime
import signal
import subprocess
import configparser

import click
import schedule

from daemonize import Daemonize

PROC_NAME = __file__[:-3]
MEGA_PROC = "megatools"
CONFIG_FILE = "sched.ini"
CONFIG_PROFILE = "normal"
DAEMON_PIDFILE = "/tmp/%s.pid" % PROC_NAME
DAEMON_PIPE = "/tmp/.%s.pipe" % MEGA_PROC

def kill(process, signo=0, cat="name"):
    """ emulate *nix pkill command """

    cmd = "kill"
    if cat == "name":
        cmd = "pkill"

    #import pdb; pdb.set_trace()
    proc = subprocess.Popen([cmd, '-%d'%signo, process],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.communicate()
    return proc.returncode

def check_pidfile(pidfile=DAEMON_PIDFILE):
    """ Check For the existence of a unix pid. """

    try:
        with open(pidfile, 'r') as filehandle:
            return kill(filehandle.read(), cat="pid") == 0
    except ValueError:
        return False
    except OSError:
        return False
    else:
        return False

def validate():
    """ validate configs """

    # Check if megatools is running
    if kill(MEGA_PROC):
        print("Megatools cli is not running.")
        sys.exit(1)
    return True

def run_schedules():
    """ run evertyhing """

    bail = False

    def sig_handler(signo, frame):
        print(bail)
        msg = ("Caught signal: %d | frame: " % signo)  + str(frame)
        print(msg)
        if signo == signal.SIGWINCH:
            msg += " WICNCHYYY!!!! "
        with open(DAEMON_PIPE, 'w') as pipe:
            pipe.write(msg+"\n")
        if signo == signal.SIGHUP:
            bail = True

    signal.signal(signal.SIGUSR1, sig_handler)
    signal.signal(signal.SIGHUP, sig_handler)
    signal.signal(signal.SIGWINCH, sig_handler)

    while not bail:
        ptime.sleep(1)
    with open(DAEMON_PIPE, 'w') as pipe:
        pipe.write("done")
    print('done')

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


@cli.command(name="run", help="start the scheduler")
def daemon_run():
    """ Start the scheduling daemon """

    if daemon_status:
        click.echo("> Scheduler already running.")
        return

    click.echo("> Trying to start daemon")
    daemon = Daemonize(app="test_app", pid=DAEMON_PIDFILE,
                       action=run_schedules)
    daemon.start()

@cli.command(name="stop", help="stop the scheduler")
def daemon_stop():
    """ Stop the scheduling daemon """

    if not daemon_status:
        click.echo("> Scheduler not running.")
        return

    # try stopping it
    with open(DAEMON_PIDFILE, 'r') as filehandle:
        error = kill(filehandle.read(), signo=signal.SIGHUP, cat="pid") != 0
    if error:
        click.echo("Couldn't stop scheduler.")

#                  _
#  _ __ ___   __ _(_)_ __
# | '_ ` _ \ / _` | | '_ \
# | | | | | | (_| | | | | |
# |_| |_| |_|\__,_|_|_| |_|

if __name__ == "__main__":
    click.clear()
    megatools_status = None
    daemon_status = check_pidfile()

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
    print("# MEGA:  ", megatools_status)
    print("# DAEMON:", daemon_status)
    print("##############################################################\n")

    # do cli stuff
    cli()
