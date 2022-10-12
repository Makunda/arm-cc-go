import re
import subprocess

from utils.object.StringUtils import StringUtils


class ProcessUtils:
    """
    Utilities related to system processes and command
    """

    @staticmethod
    def execute(command: str, cwd=".") -> subprocess.Popen:
        """
        Launch a new process using the command
        """
        proc = subprocess.Popen([command],
                                shell=True,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                universal_newlines=True,
                                cwd=cwd,
                                bufsize=0)
        stdout, stderr = proc.communicate(timeout=PROCESS_TIMEOUT)

        proc.stdout = stdout.decode("utf-8")
        proc.stderr = stderr.decode("utf-8")


    @staticmethod
    def get_output(popen: subprocess.Popen) -> str:
        content = ""
        for line in popen.stdout:
            content += line.strip() + "\n"
        return content

    @staticmethod
    def output_contains(popen: subprocess.Popen, text: str, throw_error: bool = False) -> bool:
        """
        Verify that the output match a specific string
        """
        # Fetch output
        content = ProcessUtils.get_output(popen)

        if text in content:
            return True
        else:
            if throw_error:
                raise ValueError(f"Cannot find [{text}] in the output of the process.")
            else:
                return False

    @staticmethod
    def get_regex_group(popen: subprocess.Popen, regexp: str, throw_error: bool = False) -> str:
        content = ProcessUtils.get_output(popen)
        result = re.search(regexp, content, re.MULTILINE)
        if result:
            return result.group(1).strip()
        else:
            if throw_error:
                raise ValueError(f"Cannot find matching [{regexp}] in the output of the process.")
            else:
                return False

    @staticmethod
    def get_error_block(popen: subprocess.Popen) -> str:
        """
        Verify the output contains or not errors
        """
        content = ""
        for line in popen.stderr:
            content += line.strip() + " "
        return content

    @staticmethod
    def contains_error(popen: subprocess.Popen, throw_error: bool = False) -> bool:
        """
        Verify the output contains or not errors
        """
        content = ""
        for line in popen.stderr:
            content += line.strip() + " "

        if StringUtils.is_blank(content):
            return False
        else:
            if throw_error:
                raise ValueError(f"The process returned an error.")
            else:
                return True
