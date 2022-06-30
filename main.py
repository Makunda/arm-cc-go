import sys

from codes.ExitCodes import ExitCodes
from initializer.Initializer import Initializer
from secrets.Secrets import SERVER_PORT, SERVER_HOST


def main():
    # Launching
    print("Launching the program...")

    # Load ENV
    print("Loading environment.")
    from secrets.Secrets import MODULE_NAME

    # Importing print utils
    from utils.PrintUtils import PrintUtils

    PrintUtils.info(f"Initializing module: {MODULE_NAME}.")

    # Initiate the logger
    PrintUtils.info(f"Starting Logger.")
    from logger.Logger import Logger
    main_logger = None

    try:
        main_logger = Logger.get("Main")
        main_logger.info(f"Logger is initialized and will log to [{Logger.get_log_folder_path()}]")
    except Exception as e:
        PrintUtils.error(f"Failed to instantiate the logger. Program will now exit. Error: {e}")
        sys.exit(ExitCodes.LOGGER_INITIALIZATION_FAILED)
        # Execution stops here

    # Logger is initialized
    main_logger.info("Starting the initializer")

    try:
        initializer = Initializer()
        initializer.hail_mary()
        main_logger.info(f"{MODULE_NAME} has been properly initialized.")
    except Exception as e:
        main_logger.error(f"Failed to initialize the module", e)
        sys.exit(ExitCodes.MODULE_INITIALIZATION_FAILED)
        # Execution stops here

    # Launch Flask server
    try:
        main_logger.info("Starting the web server.")
        from server import app

        app.run(SERVER_HOST, port=SERVER_PORT)
    except Exception as e:
        main_logger.error(f"Failed to start the web server.", e)
        sys.exit(ExitCodes.MODULE_INITIALIZATION_FAILED)
        # Execution stops here



if __name__ == '__main__':
    main()
