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

@cli.command(name='new', help="New schedule entry")
def new_sched_entry():
    """ new schedule entry """

    click.echo("new")

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

@cli.command(name='edit', help="Edit schedule entry")
def edit_sched():
    """ edit schedule entry """

    click.echo("edit")

@cli.command(name='remove', help="Delete schedule entry")
def delete_schedule():
    """ delete schedule entry """

    click.echo("remove")

if __name__ == "__main__":
    # validate config
    #validate()
    cli()
