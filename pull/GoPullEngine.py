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

    def __build_results(self, package: Package, output: str) -> CompatibilityResult:
        """
        Process the output of the subprocess
        """
        results = CompatibilityResult(package)

        if not output:
            results.message = "Package is compatible"
            results.compatible = True

        elif "is not a main package" in output:
            results.message = "Package is compatible"
            results.compatible = True

        # If the version is not found : fatal error
        elif "fatal error" in output:
            # The pull encountered a fatal error
            results.message = "The version of the package as not been found"
            results.compatible = False
            results.error = output

        # If it fails to find the correct path : unrecognized import path
        elif "unrecognized import path" in output:
            # The pull encountered a fatal error
            results.message = "Unrecognized package import path"
            results.compatible = False
            results.error = output

        # The link does not contain package
        elif "does not contain package" in output:
            results.message = "Link does not contain package"
            results.compatible = False
            results.error = output

        # Regex success
        else:
            results.message = "No information"
            results.compatible = False
            results.error = output

        # Package Name
        self.__logger.info(f"Package with name '{package.name}' as been flagged as '{results.compatible}'."
                           f" Reasons: {output}")

        # Return the package
        return results

    def pull_package(self, package: GoPackage) -> CompatibilityResult:
        """
        Pull the go package
        """
        package_name = package.get_id()
        args = ["go", "install", package_name]

        try:
            p = subprocess.run(args, capture_output=True, text=True)

            self.__logger.info(f"Results for {' '.join(args)}. Captured output: {p.stdout} - Error: {p.stderr}")
            return self.__build_results(package, p.stdout)
        except Exception as e:
            self.__logger.error(f"Failed to pull the package: {package_name}")
            raise PackagePullError(str(e))
