import inspect
import os


def get_absolute_path(relative_path):
    """
    Returns the absolute path relative to the importing module.
    """

    # get the path of the module that imports this function
    frame = inspect.stack()[1]
    caller_file = frame[1]
    caller_dir = os.path.dirname(os.path.abspath(caller_file))

    # construct the absolute path relative to the importing module's directory
    return os.path.abspath(os.path.join(caller_dir, relative_path))
