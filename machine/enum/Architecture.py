from enum import Enum


class Architecture(Enum):
    """
    Enum listing the different architecture
    """
    X_86 = "32bit",
    X_64 = "64bit",
    ARM = "armv7",
    ARMHF = "armhf",
    UNKNOWN = "unknown"

    @staticmethod
    def to_architecture(value) -> 'Architecture':
        """
        Convert the enumeration to architecture
        :param value: Value to convert
        :return:
        """
        try:
            return Architecture(value)
        except:
            return Architecture.UNKNOWN
