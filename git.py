import os.path
import subprocess
from errors import CommandFailed, WrongVCS
from common import calling_file

def describe(dir=None):
    """Get git version information of caller's the working tree.

    Calls ``git describe`` in the directory of the file of the calling
    frame.

    .. note::

        At least one annotated tag must be defined for ``git describe`` to
        work, e.g. with ``git tag v0.1 -a "initial version"``.

    Parameters
    ----------
    dir : string, optional
        The directory where ``git`` is called. If `None` (default) the
        directory of the file where the calling frame is defined is called.
    """
    if dir is None:
        f = calling_file(2)
        if f:
            dir = os.path.dirname(f)

    p = subprocess.Popen(["git" "describe"],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         cwd=dir)
    if p.wait() == 0:
        return p.stdout.read().strip()

    err = p.stderr.read().strip()
    if "Not a git repository" in err:
        raise WrongVCS("'%s' is not in a git repository" % dir)
    raise CommandFailed("Calling '%s' in '%s' failed with '%s'" % ("git describe", dir, err))


def sha1(dir=None):
    """Get git sha1 sum information of the caller.

    Calls ``git rev-parse HEAD`` in the directory of the file of the calling
    frame.

    Parameters
    ----------
    dir : string, optional
        The directory where ``git`` is called. If `None` (default) the
        directory of the file where the calling frame is defined is called.
    """
    if dir is None:
        f = calling_file(2)
        if f:
            dir = os.path.dirname(f)

    p = subprocess.Popen(["git" "rev-parse", "HEAD"],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         cwd=dir)
    if p.wait() == 0:
        return p.stdout.read().strip()

    err = p.stderr.read().strip()
    if "Not a git repository" in err:
        raise WrongVCS("'%s' is not in a git repository" % dir)
    raise CommandFailed("Calling '%s' in '%s' failed with '%s'" % ("git rev-parse HEAD", dir, err))
