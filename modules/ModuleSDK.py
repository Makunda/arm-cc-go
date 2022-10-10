import abc

from errors.modules.ModuleInitializationError import ModuleInitializationError
from interface.CompatibilityResult import CompatibilityResult
from interface.Package import Package
from logger.Logger import Logger


class ModuleSDK(abc.ABC):
    """
        Abstract representation of a module
    """
    __activated = False
    __logger = Logger.get("Module SDK")

    def set_activated(self, value: bool):
        self.__activated = value

    def is_active(self) -> bool:
        return self.__activated

    @abc.abstractmethod
    def get_name(self) -> str:
        pass

    def initialize(self):
        self.wrapped_initialize()
        self.set_activated(True)

    @abc.abstractmethod
    def wrapped_initialize(self):
        pass

    @abc.abstractmethod
    def wrapped_pull_package(self, package: Package) -> CompatibilityResult:
        pass

    def pull_package(self, package: Package) -> CompatibilityResult:
        """
        Verify if the module is active and pull the package
        """
        if not self.is_active():
            raise ModuleInitializationError(self.get_name())
        else:
            return self.wrapped_pull_package(package)
