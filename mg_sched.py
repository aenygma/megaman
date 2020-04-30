#!/usr/bin/env python
"""
This module is to manage a schedule of times and speeds
that Megatools downloader should run at.
"""

import sys
import subprocess

import schedule

MEGA_PROC = "megatools"

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

def main():
    """ your mother
    """

    validate()


if __name__ == "__main__":
    main()
