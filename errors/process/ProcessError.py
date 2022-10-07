import subprocess

from utils.system.ProcessUtils import ProcessUtils


class ProcessError(Exception):
    """
    This error the program fails to pull a package from Go
    """

    def __init__(self, process: subprocess.Popen, message=""):
        """
        Exception constructor
        :param process:  Process analyzed
        :param message: (Optional) Message of the exception
        """
        self.error_content = ProcessUtils.get_error_block(process)
        self.error_content = self.error_content if len(self.error_content) > 0 else "No content has been found in Stderr."
        self.message = message + ". " if message != "" else ""
        f_message = f"{self.message}Error : [{self.error_content}]."
        super().__init__(f_message)
