# pylint: disable=W0703
"""
    utils library for menial tasks/charlie work
"""
import subprocess

import psutil

def get_pid_by_name(proc_name):
    """ get the pid of a given process """

    ret = filter(lambda x:
                 x.name() == proc_name,
                 psutil.process_iter())

    ret = list(map(lambda x: str(x.pid), ret))
    return ret

def kill(process, signo=0, cat="name"):
    """ emulate *nix pkill command """

    cmd = "kill"
    if cat == "name":
        cmd = "pkill"

    proc = subprocess.Popen([cmd, '-%d'%signo, process],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.communicate()
    return proc.returncode


def get_pid(pidfile):
    """ get pid from pidfile """

    try:
        with open(pidfile, 'r') as filehandle:
            return filehandle.read()
    except Exception:
        return False

def check_pidfile(pidfile):
    """ Check For the existence of a unix pid. """

    try:
        with open(pidfile, 'r') as filehandle:
            pid = filehandle.read()
            err = kill(pid, cat="pid") == 1 # True on error
            return pid, err
    except ValueError:
        return False
    except OSError:
        return False
    else:
        return False

def open_nonblock_pipe(pipe):
    """ open and read from pipe in non-blocking way """

    import fcntl
    with open(pipe, 'r') as filehandle:
        fd = filehandle.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
    return fd

def validate():
    """ validate configs """

    # Check if megatools is running
    if utils.kill(MEGA_PROC):
        print("Megatools cli is not running.")
        sys.exit(1)
    return True

