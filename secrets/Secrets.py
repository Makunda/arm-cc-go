import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from utils.PathUtils import PathUtils
from utils.PrintUtils import PrintUtils

load_dotenv()

MODULE_NAME = os.getenv("MODULE_NAME", "ARM-CC-GO")

SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = os.getenv("SERVER_PORT", "4000")

# Define the name of the logger
LOGGER_NAME = os.getenv('LOGGER_NAME', None)
if LOGGER_NAME is None:
    PrintUtils.error("Missing LOGGER_NAME parameters. Falling back to default ARM-CC-JAVA.")
    LOGGER_NAME = "ARM-CC-GO"

LOG_FOLDER = os.getenv('LOG_FOLDER', None)
if LOG_FOLDER is None:
    log_path = Path.home().joinpath(f'{MODULE_NAME}/logs/')
    if not log_path.exists():
        os.makedirs(log_path)
    LOG_FOLDER = str(log_path)

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

##########################################################
#       -- Mailer activation --
#       The mailer will only be activated if all the
#       following parameters exist.
##########################################################

MAILER_ACTIVATION = True

# Server Address
MAILER_HOSTNAME = os.getenv("MAILER_HOSTNAME", None)
if not MAILER_HOSTNAME:
    PrintUtils.error("Missing MAILER_HOSTNAME parameter. The Mailer will be deactivated.")
    MAILER_ACTIVATION = False

# Server Port
MAILER_PORT = os.getenv("MAILER_PORT", None)
if not MAILER_PORT:
    PrintUtils.error("Missing MAILER_PORT parameter. The Mailer will be deactivated.")
    MAILER_ACTIVATION = False

# Server TLS
MAILER_TLS = os.getenv("MAILER_TLS", None)
if not MAILER_TLS:
    PrintUtils.error("Missing MAILER_TLS parameter. The Mailer will be deactivated.")
    MAILER_ACTIVATION = False

# Server User
MAILER_USER = os.getenv("MAILER_USER", None)
if not MAILER_USER:
    PrintUtils.error("Missing MAILER_USER parameter. The Mailer will be deactivated.")
    MAILER_ACTIVATION = False

# Server TLS
MAILER_PASSWORD = os.getenv("MAILER_PASSWORD", None)
if not MAILER_PASSWORD:
    PrintUtils.error("Missing MAILER_PASSWORD parameter. The Mailer will be deactivated.")
    MAILER_ACTIVATION = False

##########################################################
# Default recipients
##########################################################
mail_recipient_list = os.getenv("MAILER_RECIPIENTS", None)
MAILER_RECIPIENTS = []
if not mail_recipient_list:
    PrintUtils.error("Missing MAILER_RECIPIENTS parameter. The Mailer will be deactivated.")
    MAILER_ACTIVATION = False
else:
    # Split the recipients address
    MAILER_RECIPIENTS = mail_recipient_list.split(",")
