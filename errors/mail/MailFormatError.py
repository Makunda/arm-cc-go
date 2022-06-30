class MailFormatError(Exception):
    """
    This error is raised when an email contains a missing parameter
    """

    def __init__(self, missing_arg: str, message="The mail is not properly formatted"):
        """
        Exception constructor
        :param missing_arg: Name of the missing parameter
        :param message: (Optional) Message of the exception
        """
        self.missing_arg = missing_arg
        self.message = message
        f_message = f"{self.message}. Missing argument: [{self.missing_arg}]."
        super().__init__(f_message)
