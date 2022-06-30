class BadResponseDataError(Exception):
    """
    This error is raised when improper data are passed to the ApiResponse
    """

    def __init__(self, field_name: str, issue: str, message="This variable contains improper data."):
        """
        Exception constructor
        :param missing_arg: Name of the missing parameter
        :param message: (Optional) Message of the exception
        """
        self.field_name = field_name
        self.issue = issue
        self.message = message
        f_message = f"{self.message}. ${issue}: [{self.field_name}]."
        super().__init__(f_message)
