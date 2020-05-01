#!/usr/bin/env python
"""
This module is to manage a schedule of times and speeds
that Megatools downloader should run at.
"""

import sys
import subprocess
import configparser

import click
import schedule

MEGA_PROC = "megatools"
CONFIG_FILE = "sched.ini"
CONFIG_PROFILE = "normal"

def pkill(process_name, signal=0):
    """ emulate *nix pkill command """

    proc = subprocess.Popen(['pkill', '-%d'%signal, process_name],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.communicate()
    return proc.returncode

def validate():
    """ validate configs """

    # Check if megatools is running
    if pkill(MEGA_PROC):
        print("Megatools cli is not running.")
        sys.exit(1)
    return True

@click.group()
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
    except ValueError as e:
        click.echo("Error: Time must be an Integer. " + str(e))
    except IndexError as e:
        click.echo("Error: Time must be between 0 and 2400. " + str(e))
    except Exception as e:
        click.echo("Error: WTF did you do? " + str(e))

    # validate speed
    try:
        speed = int(speed)
        if ((speed < 1) or (speed > 1000)):
            raise IndexError
    except ValueError as e:
        click.echo("Error: Speed must be an Integer. " + str(e))
    except IndexError as e:
        click.echo("Error: Speed must be between 0 and 1000. " + str(e))
    except Exception as e:
        click.echo("Error: WTF did you do? " + str(e))

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    config.set(CONFIG_PROFILE, '%04.f' % int(time), str(speed))

    with open(CONFIG_FILE, 'w') as fp:
        config.write(fp)

@cli.command(name='list', help="List schedule entries")
def list_sched():
    """ list schedule entries """

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    print()
    print("Time", "\t", "Speed")
    print("====", "\t", "=====")
    for (k,v) in config[CONFIG_PROFILE].items():
        print(k, "\t", v)
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

    with open(CONFIG_FILE, 'w') as fp:
        config.write(fp)
    click.echo("Removed entry for time: %s" % time)

if __name__ == "__main__":
    # validate config
    #validate()
    cli()
