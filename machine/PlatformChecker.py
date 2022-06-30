from machine.enum.Architecture import Architecture
from machine.enum.OperatingSystem import OperatingSystem
import platform


class PlatformChecker:
    """
    Check the platform
    """

    @staticmethod
    def get_platform() -> OperatingSystem:
        """
        Get the machine of the current machine
        :return: Platform
        """
        pl = platform.system()
        return OperatingSystem.to_operating_system(pl)

    @staticmethod
    def get_architecture() -> Architecture:
        """
        Get the architecture of the current machine
        :return: Platform
        """
        pl = platform.architecture()[0]
        return Architecture.to_operating_system(pl)
