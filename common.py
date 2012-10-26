import inspect

def calling_file(depth=1):
    """Return the file name of the calling frame of `depth` distance.

    Parameters
    ----------
    depth : int, optional
        The number of frames the call of this function is away from the
        frame of interest. E.g. to reach the frame of the calling function::

            def my_function():
                my_file_name = calling_file(0)
                my_callers_file_name = calling_file(1)
    """
    return inspect.getfile(inspect.stack()[depth+1][0])
