import subprocess

from utils.system.ProcessUtils import ProcessUtils


class ModuleInitializationError(Exception):
    """
    This error the program fails to pull a package from Go
    """

    def __init__(self, name: str):
        """
        Exception constructor
        :param name:  Process analyzed
        :param message: (Optional) Message of the exception
        """
        f_message = f"The module '{name}' has not been initialized properly. Actions are disabled."
        super().__init__(f_message)
