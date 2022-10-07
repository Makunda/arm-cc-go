import socket

from errors.internet.SocketInformationError import SocketInformationError


class InternetUtils:
    """
    Utility class allowing the easy retrieval of information related to the machine
    """

    @staticmethod
    def get_ip_address() -> str:
        """
        Get the current IP address of the host
        :raises SocketInformationError if cannot find the hostname
        :return:
        """
        try:
            host_name = socket.gethostname()
            return str(host_name)
        except:
            raise SocketInformationError("Unable to get Hostname")

    @staticmethod
    def get_hostname() -> str:
        """
        Get the current hostname
        :raises SocketInformationError if cannot find the ip
        :return: The IP Address
        """
        try:
            hostname = InternetUtils.get_hostname()
            host_ip = socket.gethostbyname(hostname)
            return str(host_ip)
        except:
            raise SocketInformationError("Unable to get Ip Address")
