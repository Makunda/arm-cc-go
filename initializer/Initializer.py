import subprocess
import sys

from codes.ExitCodes import ExitCodes
from logger.Logger import Logger
from machine.PlatformChecker import PlatformChecker
from machine.enum.OperatingSystem import OperatingSystem
from modules.ModuleDispatcher import ModuleDispatcher


class Initializer:
    """
    Initialize the package manager
    """
    __logger = Logger.get("Initializer")
    __platform: OperatingSystem = PlatformChecker.get_platform()

    def initialize(self):
        """
        Initialize the module dispatcher
        """
        module_dispatcher = ModuleDispatcher()

    def __init__(self):
        """
        Initialize
        """
        pass
