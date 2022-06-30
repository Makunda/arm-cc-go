import logging

from secrets.Secrets import LOG_LEVEL
from utils.PrintUtils import PrintUtils


class LoggerUtils:
    """
    Defining utilities methods for logging
    """

    @staticmethod
    def get_default_level() -> logging:
        """
        Get the log level declared in the environment
        By default returns INFO
        :return: The default logging level
        """
        # Retrieve the value from env
        log_level = str(LOG_LEVEL).lower()

        # Check the log levels
        if log_level == "info":
            return logging.INFO
        if log_level == "warning":
            return logging.WARNING
        elif log_level == "debug":
            return logging.DEBUG
        else:
            # Print
            PrintUtils.error(f"The log level [{LOG_LEVEL}] corresponds to none known values. Falling back to INFO<")

            # By default return INFO
            return logging.INFO
