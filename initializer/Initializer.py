import subprocess
import sys

from codes.ExitCodes import ExitCodes
from logger.Logger import Logger


class Initializer:
    """
    Initialize the package manager
    """
    __logger = Logger.get("Initializer")

    # Verify Go is installed
    def verify_installed(self) -> bool:
        """
        Verify if the utility is installed
        :return:
        """
        try:
            p = subprocess.run(["go", "version"], capture_output=True, text=True)
            stdout = str(p.stdout).replace("go version ", "")
            self.__logger.info(f"Version of GO detected: {stdout}")
            return True
        except Exception as e:
            self.__logger.error("GoLang is not installed on this computer.")
            self.__logger.error("You need to install GoLang to run this module. The program will now exit")
            self.__logger.error("Exception", e)
            sys.exit(ExitCodes.GOLANG_NOT_INSTALLED)
            # The program stops here 

    # Pull test
    def pull_test(self) -> bool:
        """
        Pull the repository
        :return:
        """
        pass

    def hail_mary(self):
        """
        Test all the cases
        :return: None
        """
        # Verify Go is installed or quit
        self.verify_installed()

        # Try to pull a dummy dependency
        self.pull_test()

    def __init__(self):
        """
        Initialize
        """
        pass
