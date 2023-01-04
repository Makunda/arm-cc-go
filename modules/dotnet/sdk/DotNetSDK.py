import glob
import re
import subprocess

from Definitions import DOTNET_DIR
from enumerations.CompatibiltyStatus import CompatibilityStatus, Compatibility
from interface.CompatibilityResult import CompatibilityResult
from interface.Package import Package
from logger.Logger import Logger
from modules.ModuleSDK import ModuleSDK
from secrets.Secrets import PROCESS_TIMEOUT
from templates.dotnet.CsProjTemplate import cs_proj_template_6_0
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

    __template_cs_proj: str = cs_proj_template_6_0

    def clean_cs_proj(self):
        """
            Clean the CS Proj
        """
        cs_files = glob.glob(self._project_path + "*.csproj")
        for file in cs_files:
            try:
                with open(file, mode="w") as f:
                    f.write(cs_proj_template_6_0)
            except:
                self.__logger.error(f"Failed to open file with path: [{file}]")

    def save_cs_proj(self):
        """
            Clean the CS Proj
        """
        cs_files = glob.glob(self._project_path + "*.csproj")
        if len(cs_files) > 0:
            try:
                with open(cs_files[0], mode="r") as f:
                    self.__template_cs_proj = f.read()
            except:
                self.__logger.error(f"Failed to open file with path: [{cs_files[0]}]")

    def wrapped_initialize(self):
        try:
            PathUtils.mergeFolder(self._project_path)
        except Exception as e:
            self.__logger.error(f"Failed to create the dotnet folder at: {self._project_path}")
            raise e

        try:
            ProcessUtils.execute("dotnet new console --framework net6.0", self._project_path)
            self.__logger.info(f"New dotnet project created at {self._project_path}.")
            self.save_cs_proj()

        except Exception as e:
            self.__logger.error(f"Failed to create the dotnet project.")
            raise e

    def wrapped_pull_package(self, package: Package) -> CompatibilityResult:
        # Reset the proj
        self.clean_cs_proj()

        # Add the component
        command = f"dotnet add package {package.name} --version {package.version} --framework {package.target}"

        proc = subprocess.Popen(command,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                cwd=self._project_path,
                                shell=True)
        stdout, stderr = proc.communicate(timeout=20)

        s_stdout = stdout.decode("utf-8")
        s_stderr = stderr.decode("utf-8")

        # Valid output
        packet_added = f"PackageReference for package '{package.name}' version '{package.version}' added to file"
        packet_updated = f"PackageReference for package '{package.name}' version '{package.version}' updated in file"
        packet_not_found = f"Unable to find package {package.name}. No packages exist with this id in source(s): nuget.org"
        packet_version_not_found = f"Unable to find package {package.name} with version"

        san_package_name = str(f"{package.name} {package.version}").replace(".", "\\.")
        re_package_compatible = re.compile(
            f"Package '{san_package_name}' is compatible with all the specified frameworks in project")
        re_package_incompatible = re.compile(f"Package '{san_package_name}' is incompatible with")
        re_package_partially_compatible = re.compile(f"Package '{san_package_name}' was restored using")

        # Compatibility result declaration
        message: str = ""
        compatible: Compatibility = Compatibility.UNKNOWN
        error: str = ""

        if bool(re_package_compatible.search(s_stdout)):
            message = str(CompatibilityStatus.COMPATIBLE.value)
            compatible = Compatibility.COMPATIBLE
            self.__logger.info(f"{package.to_string()} has been installed in the project.")
        elif bool(re_package_partially_compatible.search(s_stdout)) or bool(
                re_package_partially_compatible.search(s_stderr)):
            message = str(CompatibilityStatus.COMPATIBLE.value)
            compatible = Compatibility.PARTIAL
            self.__logger.info(f"{package.to_string()} has been installed in the project.")
        elif bool(re_package_incompatible.search(s_stdout)) or bool(re_package_incompatible.search(s_stderr)):
            message = str(CompatibilityStatus.NON_COMPATIBLE.value)
            compatible = Compatibility.INCOMPATIBLE
            self.__logger.info(f"{package.to_string()} is not compatible.")
        elif packet_not_found in s_stderr:
            # Incompatible package
            message = str(CompatibilityStatus.NON_COMPATIBLE.value)
            compatible = Compatibility.INCOMPATIBLE
            error = f"{package.to_string()} does not exist for this architecture."
            self.__logger.error(f"{package.to_string()} does not exist for this architecture.")
        elif packet_version_not_found in s_stderr:
            message = str(CompatibilityStatus.VERSION_NON_COMPATIBLE.value)
            compatible = Compatibility.INCOMPATIBLE
            error = f"{package.to_string()} does not exist in this version."
            self.__logger.error(f"{package.to_string()} does not exist in this version.")
        else:
            message = str(CompatibilityStatus.UNKNOWN.value)
            compatible = Compatibility.INCOMPATIBLE
            error = "Check server's logs for more details."
            self.__logger.error(f"{package.to_string()} pulled failed. "
                                f"Output: {s_stdout}. "
                                f"Error: {s_stderr}")

        return CompatibilityResult(package, str(message), compatible, error)
