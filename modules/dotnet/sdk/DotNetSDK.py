import subprocess

from definitions import DOTNET_DIR
from enumerations.CompatibiltyStatus import CompatibilityStatus
from interface.CompatibilityResult import CompatibilityResult
from interface.Package import Package
from logger.Logger import Logger
from modules.ModuleSDK import ModuleSDK
from secrets.Secrets import PROCESS_TIMEOUT
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
            self.__logger.info(f"New dotnet project created at {self._project_path}.")

        except Exception as e:
            self.__logger.error(f"Failed to create the dotnet project.")
            raise e

    def wrapped_pull_package(self, package: Package) -> CompatibilityResult:
        command = f"dotnet add package {package.name} --version {package.version}"
        process = ProcessUtils.execute(command, self._project_path)

        proc = subprocess.Popen(command,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                cwd=self._project_path,
                                shell=True)
        stdout, stderr = proc.communicate(timeout=PROCESS_TIMEOUT)

        s_stdout = stdout.decode("utf-8")
        s_stderr = stderr.decode("utf-8")

        print("DotNetSDK Pull results (s_stdout):", s_stdout)
        print("DotNetSDK Pull results (s_stderr):", s_stderr)

        # Valid output
        packet_added = f"PackageReference for package '{package.name}' version '{package.version}' added to file"
        packet_updated = f"PackageReference for package '{package.name}' version '{package.version}' updated in file"
        packet_not_found = f"Unable to find package {package.name}. No packages exist with this id in source(s): nuget.org"
        packet_version_not_found = f"Unable to find package {package.name} with version"

        # Compatibility result declaration
        message: str = ""
        compatible: bool = False
        error: str = ""

        if  packet_added in s_stdout:
            message = str(CompatibilityStatus.COMPATIBLE.value)
            compatible = True
            self.__logger.info(f"{package.to_string()} has been installed in the project.")
        elif packet_updated in s_stdout:
            # Updated package
            message = str(CompatibilityStatus.COMPATIBLE.value)
            compatible = True
            self.__logger.info(f"{package.to_string()} has been updated in the project.")
        elif packet_not_found in s_stderr:
            # Incompatible package
            message = str(CompatibilityStatus.NON_COMPATIBLE.value)
            compatible = False
            error = f"{package.to_string()} does not exist for this architecture."
            self.__logger.error(f"{package.to_string()} does not exist for this architecture.")
        elif packet_version_not_found in s_stderr:
            message = str(CompatibilityStatus.VERSION_NON_COMPATIBLE.value)
            compatible = False
            error = f"{package.to_string()} does not exist in this version."
            self.__logger.error(f"{package.to_string()} does not exist in this version.")
        else:
            message = str(CompatibilityStatus.UNKNOWN.value)
            compatible = False
            error = "Check server's logs for more details."
            self.__logger.error(f"{package.to_string()} pulled failed. "
                                f"Output: {s_stdout}. "
                                f"Error: {s_stderr}")

        return CompatibilityResult(package, str(message), compatible, error)
