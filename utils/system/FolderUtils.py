import glob
import os
from typing import List

import checksumdir


class FolderUtils:
    """
    Static class managing the folders
    """


    @staticmethod
    def merge_folder(path: str) -> str:
        """
        Check a folder and create it if necessary
        :param path of the folder to create
        :return: Path of the folder
        """
        # Check whether the specified path exists or not
        try:
            isExist = os.path.exists(path)

            if not isExist:
                # Create a new directory because it does not exist
                os.makedirs(path)
            return path
        except Exception as e:
            raise FileNotFoundError("Failed to create the file at [%s]" % path)
    @staticmethod
    def merge_file(path: str) -> str:
        """
        Check a folder and create it if necessary
        :param path of the folder to create
        :return: Path of the folder
        """
        # Check whether the specified path exists or not
        isExist = os.path.isfile(path)

        if not isExist:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                f.write("")

        return path


    @staticmethod
    def get_folder_checksum(path: str):
        """
        Calculate and return the checksum of a directory
        :param path: Path of the directory to hash
        :return: The checksum
        """
        # Check whether the specified path exists or not
        isExist = os.path.exists(path)

        if not isExist:
            raise FileNotFoundError("Cannot calculate the checksum of a nonexistent folder. Path: {}".format(path))
        return checksumdir.dirhash(path)

    @staticmethod
    def list_folder(path: str, recursive=False, extension=None) -> List[str]:
        """
        List all the files in the folder
        :param path: Path of the folder
        :param recursive: Activate the recursively
        :param extension: Extension of files to discover
        :return:
        """
        if extension is not None:
            path = os.path.join(path, "**/*" + str(extension))
        return glob.glob(path, recursive=recursive)
