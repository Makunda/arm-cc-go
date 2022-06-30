from enum import Enum


class OperatingSystem(Enum):
    """
    Enumeration listing the different operating system available
    """
    WINDOWS = "Windows",
    LINUX = "Linux",
    MACOS = "Darwin",
    UNKNOWN = "unknown"

    @staticmethod
    def to_operating_system(value) -> 'OperatingSystem':
        """
        Convert the enumeration to operating system
        :param value: Value to convert
        :return:
        """
        try:
            return OperatingSystem(value)
        except:
            return OperatingSystem.UNKNOWN
