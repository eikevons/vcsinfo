import os.path
import subprocess
from errors import CommandFailed, WrongVCS
from common import calling_file

def _get_dir(f):
    if f:
        dir = os.path.dirname(f)
        if dir:
            return dir
    return None


def describe(f=None):
    """Get git version information of caller's the working tree.

    Calls ``git describe`` in the directory of the file of the calling
    frame.

    .. note::

        At least one annotated tag must be defined for ``git describe`` to
        work, e.g. with ``git tag v0.1 -a "initial version"``.

    Parameters
    ----------
    f : string, optional
        The file where ``git`` is called. If `None` (default) the
        directory of the file where the calling frame is defined is called.
    """
    if f is None:
        f = calling_file(1)

    dir = _get_dir(f)

    p = subprocess.Popen(["git", "describe"],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         cwd=dir,
                         env={"LANG":"C"})
    if p.wait() == 0:
        return p.stdout.read().strip()

    err = p.stderr.read().strip()
    if "Not a git repository" in err:
        raise WrongVCS("'%s' is not in a git repository" % dir)
    raise CommandFailed("Calling '%s' in '%s' failed with '%s'" % ("git describe", dir, err))


def sha1(f=None):
    """Get git sha1 sum information of the caller.

    Calls ``git rev-parse HEAD`` in the directory of the file of the calling
    frame.

    Parameters
    ----------
    f : string, optional
        The file where ``git`` is called. If `None` (default) the
        directory of the file where the calling frame is defined is called.
    """
    if f is None:
        f = calling_file(1)

    dir = _get_dir(f)
    p = subprocess.Popen(["git", "rev-parse", "HEAD"],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         cwd=dir,
                         env={"LANG":"C"})

    if p.wait() == 0:
        return p.stdout.read().strip()

    err = p.stderr.read().strip()
    if "Not a git repository" in err:
        raise WrongVCS("'%s' is not in a git repository" % dir)
    raise CommandFailed("Calling '%s' in '%s' failed with '%s'" % ("git rev-parse HEAD", dir, err))


def version(f=None):
    """Get a git version description for `dir`.

    Tries :func:`describe` and :func:`sha1`

    Parameters
    ----------
    f : string, optional
        The file where ``git`` is called. If `None` (default) the
        directory of the file where the calling frame is defined is called.
    """
    if f is None:
        f = calling_file(1)

    try:
        return describe(f)
    except CommandFailed:
        return sha1(f)[:6]
