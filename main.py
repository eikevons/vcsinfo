from errors import WrongVCS
from common import calling_file
from git import version as git_version
from svn import version as svn_version

__all__ = ["version", "git_version", "svn_version", "calling_file"]


def version(f=None):
    if f is None:
        f = calling_file(1)

    for name, func in (("git", git_version), ("svn", svn_version)):
        try:
            vers = func(f)
            return "%s: %s" % (name, vers)
        except WrongVCS:
            pass
    raise WrongVCS("'%s' is not in a known vcs" % (f,))



if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        for f in sys.argv[1:]:
            print "{0}  {1}".format(f, version(f))
    else:
        print version()

