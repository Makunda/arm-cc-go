import subprocess

from codes.ExitCodes import ExitCodes
from errors.process.ProcessError import ProcessError
from logger.Logger import Logger
from machine.PlatformChecker import PlatformChecker
from machine.enum.OperatingSystem import OperatingSystem
from utils.system.ProcessUtils import ProcessUtils

VERIFY_INSTALLATION = "dotnet --info"


class DotNetInstaller:
    __logger = Logger.get("Net Installer")
    __platform: OperatingSystem = PlatformChecker.get_platform()

    def __init__(self):
        pass

    def verify_installed(self) -> bool:
        """
        Verify if the utility is installed
        :return:
        """
        try:
            p = ProcessUtils.execute(VERIFY_INSTALLATION)
            sdk_versions = ProcessUtils.get_regex_group(p, r"\.NET SDKs installed:\s*([0-9]+.[0-9]+.[0-9]+)", True)
            self.__logger.info("Dotnet core SDK detected:", sdk_versions)

            runtime_versions = ProcessUtils.get_regex_group(p, r"\.NET runtimes installed:((?:\n.+)+)", True)
            self.__logger.info("Runtime environment detected:", runtime_versions)

            return True
        except Exception as e:
            self.__logger.error("Dotnet Core is not installed on this computer.")
            return False
