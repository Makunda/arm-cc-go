from typing import Dict, List

from enumerations.CompatibiltyStatus import CompatibilityStatus
from enumerations.Language import Language
from interface.CompatibilityResult import CompatibilityResult
from interface.Package import Package
from logger.Logger import Logger
from metaclass.SingletonMeta import SingletonMeta
from modules.ModuleSDK import ModuleSDK
from modules.dotnet.sdk.DotNetSDK import DotNetSDK
from modules.go.sdk.GoSDK import GoSDK


class ModuleDispatcher(metaclass=SingletonMeta):
    """
        Module dispatcher
    """
    __logger = Logger.get("Module SDK Dispatcher")
    __sdk_map: Dict[str, ModuleSDK] = {}

    def __init__(self):
        """
            Initialize the dispatcher
        """
        try:
            self.__sdk_map = {
                Language.GO: GoSDK(),
                Language.DOTNET: DotNetSDK(),
            }
        except Exception as e:
            self.__logger.error("Failed to initialize the SDK map.", e)
            raise e

        for key in self.__sdk_map.keys():
            name = self.__sdk_map[key].get_name()
            try:
                self.__sdk_map[key].initialize()
            except Exception as e:
                self.__logger.error(f"Failed to initialize the SDK [{name}].", e)

    def get_defined_languages(self) -> List[str]:
        """
        Return the list of defined languages
        """
        return list(self.__sdk_map.keys())

    def is_language_supported(self, language: str) -> bool:
        """
        Verify that a language is supported
        """
        return language in self.get_defined_languages()

    def analyze(self, language: str, package: Package) -> CompatibilityResult:
        """
        Analyze a package and return the compatibility results
        """
        if language in self.__sdk_map.keys():
            return self.__sdk_map[language].pull_package(package)
        else:
            return CompatibilityResult(package, CompatibilityStatus.LANGUAGE_NOT_SUPPORTED, False)