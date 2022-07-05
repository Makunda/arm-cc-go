class PackagePullError(Exception):
    """
    This error the program fails to pull a package from Go
    """

    def __init__(self, pull_error: str, message=""):
        """
        Exception constructor
        :param pull_error:  Error sent by the utility
        :param message: (Optional) Message of the exception
        """
        self.pull_error = pull_error
        self.message = message
        f_message = f"{self.message}. Error : [{self.pull_error}]."
        super().__init__(f_message)
