import smtplib
from typing import List

from errors.internet.SocketInformationError import SocketInformationError
from errors.mail.MailInitializationError import MailInitializationError
from errors.mail.MailSendingError import MailSendingError
from logger.Logger import Logger
from mailer.Email import Email
from metaclass.SingletonMeta import SingletonMeta

from secrets.Secrets import MAILER_ACTIVATION, MODULE_NAME, MAILER_RECIPIENTS, MAILER_USER, MAILER_HOSTNAME, \
    MAILER_PORT, MAILER_PASSWORD
from utils.InternetUtils import InternetUtils


class Mailer(metaclass=SingletonMeta):
    """
    Mailer class in charge of sending email in the system
    """

    __logger = Logger.get("Mailer")
    __activated: bool = bool(MAILER_ACTIVATION)
    __module_name: str = str(MODULE_NAME)

    def is_operational(self) -> bool:
        """
        Returns True if the mailer has all the properties required to send an email.
        Otherwise, if a parameter is missing False, will be returned.
        You can check in the logs at the initialization of the program which ones are misssing.
        :return: A Boolean
        """
        return self.__activated

    def get_server_stamp(self) -> str or None:
        """
        Build a server stamp using the hostname information as ip and name
        In order to identify the mails more easily
        :return: Stamp as a String, or None if an exception occured
        """
        try:
            hostname = InternetUtils.get_hostname()
            ip = InternetUtils.get_ip_address()
            stamp = f"[Module: {self.__module_name} | Hostname: {hostname} | IP: {ip} ]"

            return stamp
        except SocketInformationError as e:
            self.__logger.error("Failed to create server stamp. Failed to get Host related information", e)
            return None
        except Exception as e:
            self.__logger.error("Failed to create server stamp. Unknown error.", e)
            return None

    def send(self, email: Email) -> None:
        """
        Send the formatted email
        :param email: Email to send.
        :return: None
        """

        # Verify the mailer is up
        if not self.is_operational():
            raise MailInitializationError("Mailer has not been initialized")

        # Apply the stamp
        email.set_sender(self.get_server_stamp())

        # Add the default sender
        email.set_sender(MAILER_USER)

        # Add default recipient
        email.add_recipients(MAILER_RECIPIENTS)

        # Build the email, raise an error if the generation fails
        email_message = email.generate()

        try:
            # Send it
            with smtplib.SMTP(MAILER_HOSTNAME, MAILER_PORT) as server:
                server.login(MAILER_USER, MAILER_PASSWORD)  # Login

                # Send the message built
                server.send_message(email_message)
                server.quit()
        except Exception as e:
            recipient_s = ", ".join(email.get_recipients())
            self.__logger.error(f"Failed to send the email to [{recipient_s}].", e)
            raise MailSendingError(f"An error occured trying to send the email")