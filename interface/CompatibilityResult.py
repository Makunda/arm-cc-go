from enumerations.CompatibiltyStatus import Compatibility
from interface.Package import Package


class CompatibilityResult:
    """
    Check of the result is compatible or not
    """
    package: Package
    message: str
    compatible: str
    error: str

    def __init__(self, package: Package, message: str = "",
                 compatible:  Compatibility = Compatibility.UNKNOWN, error: str = ""):
        """
        Constructor of the Compatibility results
        """
        assert package is not None, "Cannot create a compatibility result from None package"

        self.message = message
        self.package = package
        self.compatible = str(compatible.value)
        self.error = error

    def serialize(self) -> dict:
        """
        Return a dictionary represent
        """
        return {
            "message": self.message,
            "package": self.package.serialize(),
            "compatible": str(self.compatible),
            "error": self.error
        }
