from enum import Enum


class CompatibilityStatus(Enum):
    COMPATIBLE = "Package is compatible"
    NON_COMPATIBLE = "Package not found"
    VERSION_NON_COMPATIBLE = "Package version not found"
    VERSION_PARTIALLY_COMPATIBLE = "Package is partially compatible"
    FAULTY_COMMAND = "Incorrect command"
    UNKNOWN = "Unknown error"
    LANGUAGE_NOT_SUPPORTED = "Language not supported"


class Compatibility(Enum):
    """
        Compatibility results
    """
    COMPATIBLE = "compatible",
    PARTIAL = "partial",
    INCOMPATIBLE = "incompatible",
    UNKNOWN = "unknown"
