from enum import Enum


class ExitCodes(Enum):
    """
    List of exit codes of the application
    """
    LOGGER_INITIALIZATION_FAILED = 1
    MODULE_INITIALIZATION_FAILED = 2