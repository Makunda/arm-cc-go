from enum import Enum


class PrintColors(Enum):
    """
    Print Color for the console
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class PrintUtils:

    @staticmethod
    def error(message: str):
        """
        Print errors in red in the console
        :param message:
        :return:
        """
        PrintUtils.print_color(message, PrintColors.WARNING)

    @staticmethod
    def info(message: str):
        """
        Print info in blue/cyan in the console
        :param message:
        :return:
        """
        PrintUtils.print_color(message, PrintColors.OKCYAN)

    @staticmethod
    def print_color(message: str, color: PrintColors):
        """
        Print a message with  a defined color
        :param message:  Message to print
        :param color: Color of the text
        :return:
        """
        print(f"{color.value}{message}{PrintColors.ENDC.value}")
