import os
from pathlib import Path


class PathUtils:
    """
        Path utilities
    """

    @staticmethod
    def exists(path: str) -> bool:
        """
        Verify an element exists on the file system
        :param path: Path to verify
        :return:
        """
        return os.path.exists(path)

    @staticmethod
    def is_relative(path: str) -> bool:
        """
        Verify an element exists on the file system
        :param path: Path to verify
        :return:
        """
        return not os.path.isabs(path)

    @staticmethod
    def ensure_is_abs(path: str, base_url: str) -> str:
        """
        Ensure the path provided is absolute, otherwise append the base url
        :param path: Path to test
        :param base_url: Base url to append if the path is relative
        :return:
        """
        if os.path.isabs(path) and os.path.exists(path):
            return path
        else:
            return os.path.join(base_url,path)

    @staticmethod
    def mergeFolder(path: str) -> None:
        """
        Verify the existence of a folder and create it if necessary
        :param path: Path to returned
        :return:
        """
        if not PathUtils.exists(path):
            return os.makedirs(path)

    @staticmethod
    def mergePath(path: Path) -> None:
        """
        Verify the existence of a folder and create it if necessary
        :param path: Path to returned
        :return:
        """
        if not path.exists():
            return os.makedirs(str(path))