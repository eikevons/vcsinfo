from errors import WrongVCS
from common import calling_file
from git import version as git_version

__all__ = ["version", "git_version"]


def version(f=None):
    if f is None:
        f = calling_file(1)

    try:
        return "git: %s" % git_version(f)
    except WrongVCS, err:
        # TODO try svn, hg
        raise err



if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        for f in sys.argv[1:]:
            print "{0}  {1}".format(f, version(f))
    else:
        print version()

