from definitions import DOTNET_DIR
from enumerations.CompatibiltyStatus import CompatibilityStatus
from interface.CompatibilityResult import CompatibilityResult
from interface.Package import Package
from logger.Logger import Logger
from modules.ModuleSDK import ModuleSDK
from utils.system.PathUtils import PathUtils
from utils.system.ProcessUtils import ProcessUtils


class DotNetSDK(ModuleSDK):
    """
        Class piloting the Dotnet SDK
    """

    def get_name(self) -> str:
        return "DotNet SDK"

    __logger = Logger.get("DotNet SDK")

    _project_path = DOTNET_DIR
    _initialized: bool = False

    def wrapped_initialize(self):
        try:
            PathUtils.mergeFolder(self._project_path)
        except Exception as e:
            self.__logger.error(f"Failed to create the dotnet folder at: {self._project_path}")
            raise e

        try:
            ProcessUtils.execute("dotnet new console", self._project_path)
        except Exception as e:
            self.__logger.error(f"Failed to create the dotnet project.")
            raise e

    def wrapped_pull_package(self, package: Package) -> CompatibilityResult:
        command = f"dotnet add package {package.name} --version {package.version}"
        process = ProcessUtils.execute(command, self._project_path)

        # Valid output
        packet_added = f"PackageReference for package '{package.name}' version '{package.version}' added to file"
        packet_updated = f"PackageReference for package '{package.name}' version '{package.version}' updated in file"
        packet_not_found = f"Unable to find package {package.name}. No packages exist with this id in source(s): nuget.org"
        packet_version_not_found = f"Unable to find package {package.name} with version"

        # Compatibility result declaration
        message = ""
        compatible = False
        error = ""

        if ProcessUtils.output_contains(process, packet_added):
            message = CompatibilityStatus.COMPATIBLE
            compatible = True
            self.__logger.info(f"{package.to_string()} has been installed in the project.")
        elif ProcessUtils.output_contains(process, packet_updated):
            # Updated package
            message = CompatibilityStatus.COMPATIBLE
            compatible = True
            self.__logger.info(f"{package.to_string()} has been updated in the project.")
        elif ProcessUtils.output_contains(process, packet_not_found):
            # Incompatible package
            message = CompatibilityStatus.NON_COMPATIBLE
            compatible = False
            error = f"{package.to_string()} does not exist for this architecture."
            self.__logger.error(f"{package.to_string()} does not exist for this architecture.")
        elif ProcessUtils.output_contains(process, packet_version_not_found):
            message = CompatibilityStatus.VERSION_NON_COMPATIBLE
            compatible = False
            error = f"{package.to_string()} does not exist in this version."
            self.__logger.error(f"{package.to_string()} does not exist in this version.")
        else:
            message = CompatibilityStatus.UNKNOWN
            compatible = True
            error = ProcessUtils.get_output(process)
            self.__logger.error(f"{package.to_string()} failed to ")

        return CompatibilityResult(package, message, compatible, error)
