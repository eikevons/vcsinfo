vcsinfo
=======

This package allows access to revisions of files from within Python. I
wrote it to access the revisions of my projects at runtime.

To get the revision of the file some code resides in simply use::

    from vcsinfo import version

    def print_my_revision():
        print version()

.. note::
    
    The code does not check whether uncommitted changes are lying
    around.
