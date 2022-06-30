import copy
import logging
import os
from logging.handlers import RotatingFileHandler
from flask.logging import default_handler


from logger.LoggerUtils import LoggerUtils
from metaclass.SingletonMeta import SingletonMeta
from secrets.Secrets import LOG_FOLDER, LOG_LEVEL, MODULE_NAME
from utils.FolderUtils import FolderUtils

"""
   Initialize logging and displays information
   :return: None
   """
log_folder = str(LOG_FOLDER)
log_level = str(LOG_LEVEL)

# Create log folder if needed
log_path = os.path.join(log_folder)
FolderUtils.merge_folder(log_path)

# Change the permission over the log folder
os.chmod(log_path, 0o777)

# Print log files and level
message = "Logs will be saved to {0}. Log level is: {1}".format(log_folder, log_level)
logging.debug(message)

timestamp = ""

# define logs files and folders
INFO_FILE = f"{MODULE_NAME}_info_{timestamp}.log"
INFO_FILE = os.path.join(log_folder, INFO_FILE)


# Info File
INFO_LOG_HANDLER = RotatingFileHandler(INFO_FILE, maxBytes=1048576, backupCount=5)
INFO_LOG_HANDLER.setFormatter(
    logging.Formatter(f'%(asctime)s %(levelname)s : {MODULE_NAME} : %(message)s ' '[in %(pathname)s:%(lineno)d]'))
INFO_LOG_HANDLER.setLevel(logging.INFO)


# Error File
ERROR_FILE = f"{MODULE_NAME}_errors_{timestamp}.log"
ERROR_FILE = os.path.join(log_folder, ERROR_FILE)

ERROR_LOG_HANDLER = RotatingFileHandler(ERROR_FILE, maxBytes=1048576, backupCount=5)
ERROR_LOG_HANDLER.setFormatter(
    logging.Formatter(f'%(asctime)s %(levelname)s : {MODULE_NAME} : %(message)s ' '[in %(pathname)s:%(lineno)d]'))
ERROR_LOG_HANDLER.setLevel(logging.ERROR)


class Logger(metaclass=SingletonMeta):
    """
    Singleton class in charge of wrapping the default logger
    """

    @staticmethod
    def get_log_folder_path() -> str:
        """
        Get the path to the log files
        :return:
        """
        return copy.deepcopy(log_folder)

    @staticmethod
    def get(name: str, level: logging = None) -> logging.Logger:
        """
        Get a logger with a prefixed name
        :param level: Log level for this logger. By default the logger will use INFO
        :param name:  Name of the logger
        :return: Wrapped logger class
        """
        local_level = level
        if local_level is None:
            local_level = LoggerUtils.get_default_level()

        logger = logging.getLogger(name)
        logger.addHandler(INFO_LOG_HANDLER)
        logger.addHandler(ERROR_LOG_HANDLER)
        logger.addHandler(default_handler)
        logger.setLevel(local_level)
        return logger