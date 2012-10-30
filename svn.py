import subprocess
from common import calling_file
from errors import CommandFailed, WrongVCS


def revision(f=None):
    if f is None:
        f = calling_file(1)

    p = subprocess.Popen(["svn", "info", f],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         env={"LANG":"C"})
    if p.wait() == 0:
        for line in p.stdout:
            if line.lower().startswith("revision:"):
                return int(line.split()[1])
        raise RuntimeError("Failed to parse output of 'svn info %s'" % (f,))

    err = p.stderr.read().strip()

    for line in err.split("\n"):
        if line.startswith("svn:") and "not a working copy" in line:
            raise WrongVCS("%s is not in a svn repository" % (f,))
    raise CommandFailed("Calling 'svn info %s' failed with '%s'" % (f, err))


def version(f=None):
    if f is None:
        f = calling_file(1)

    return "r%d" % revision(f)
