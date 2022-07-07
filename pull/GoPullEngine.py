import subprocess

from errors.pull.MailFormatError import PackagePullError
from interface.CompatibilityResult import CompatibilityResult
from interface.Package import Package
from interface.go.GoPackage import GoPackage
from logger.Logger import Logger


class GoPullEngine:
    """
        Engine in charge of the installation
    """

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

    def pull_package(self, package: GoPackage) -> CompatibilityResult:
        """
        Pull the go package
        """
        package_name = package.get_id()
        args = ["go", "get", package_name]

        try:
            p = subprocess.run(args, capture_output=True, text=True)

            self.__logger.info(f"Results for {' '.join(args)}. Captured output: {p.stdout} - Error: {p.stderr}")
            return self.__build_results(package, p.stdout, p.stderr)
        except Exception as e:
            self.__logger.error(f"Failed to pull the package: {package_name}")
            raise PackagePullError(str(e))
