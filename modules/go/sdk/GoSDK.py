import subprocess

from errors.pull.MailFormatError import PackagePullError
from interface.CompatibilityResult import CompatibilityResult
from interface.Package import Package
from interface.go.GoPackage import GoPackage
from logger.Logger import Logger
from modules.ModuleSDK import ModuleSDK
from secrets.Secrets import PROCESS_TIMEOUT


class GoSDK(ModuleSDK):
    """
        Engine in charge of the installation
    """

    def wrapped_initialize(self):
        pass

    def get_name(self) -> str:
        return "Go SDK"

    def wrapped_pull_package(self, package: Package) -> CompatibilityResult:
        """
            Pull the go package
            @params Package to pull
        """
        package_name = f"{package.name}@{package.version}"
        args = [f"go install {package_name}"]

        try:
            proc = subprocess.Popen(args,
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    shell=True)
            stdout, stderr = proc.communicate(timeout=PROCESS_TIMEOUT)

            s_stdout = stdout.decode("utf-8")
            s_stderr = stderr.decode("utf-8")

            self.__logger.info(f"Results for {' '.join(args)}. Captured output: {s_stdout} - Error: {s_stderr}")
            return self.__build_results(package, s_stdout, s_stderr)
        except subprocess.TimeoutExpired as e:
            s_stdout = ""
            s_stderr = "Process Timeout"
            self.__logger.info(f"Results for {' '.join(args)}. Captured output: {s_stdout} - Error: {s_stderr}")
            return self.__build_results(package, s_stdout, s_stderr)
        except Exception as e:
            self.__logger.error(f"Failed to pull the package: {package_name}")
            raise PackagePullError(str(e))

    __logger = Logger.get("Go Pull Engine")

    def __build_results(self, package: Package, stdout: str, stderr: str) -> CompatibilityResult:
        """
        Process the output of the subprocess
        """
        results = CompatibilityResult(package)

        # No Error
        if stderr == "":
            results.message = "Package is compatible"
            results.compatible = True

            if "is not a main package" in stdout:
                results.message = "Package is compatible but not a main package"
                results.compatible = True
                results.error = stderr

        # Error
        if stderr != "":
            results.compatible = False
            results.error = stderr

            if "version must not be empty" in stderr:
                results.message = "Package version is empty"

            elif "Process Timeout" in stderr:
                results.message = "Process Timeout. This may indicate an unreachable or a private repository."

            elif "missing dot in first path element" in stderr:
                results.message = "Package path is malformed"

            # If the version is not found : fatal error
            elif "fatal error" in stderr:
                # The pull encountered a fatal error
                results.message = "The version of the package as not been found"

            # If it fails to find the correct path : unrecognized import path
            elif "unrecognized import path" in stderr:
                # The pull encountered a fatal error
                results.message = "Unrecognized package import path"

            # The link does not contain package
            elif "does not contain package" in stderr:
                results.message = "Link does not contain package"

            # Regex success
            else:
                results.message = "Unknown error"

        # Package Name
        self.__logger.info(f"Package with name '{package.name}' as been flagged as '{results.compatible}'."
                           f" Reasons: {results.message}")

        # Return the package
        return results
