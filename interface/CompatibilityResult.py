from interface.Package import Package


class CompatibilityResult:
    """
    Check of the result is compatible or not
    """
    package: Package
    message: str
    compatible: bool
    error: str

    def __init__(self, package: Package, message: str = "",
                 compatible: bool = False, error: str = ""):
        """
        Constructor of the Compatibility resutls
        """
        assert package is not None, "Cannot create a compatibility result from None package"

        self.message = message
        self.package = package
        self.compatible = compatible
        self.error = error

    def serialize(self) -> dict:
        """
        Return a dictionary represent
        """
        return {
            "message": self.message,
            "package": self.package.serialize(),
            "compatible": bool(self.compatible),
            "error": self.error
        }
