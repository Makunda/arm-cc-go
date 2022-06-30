import email
from email.headerregistry import Address
from email.message import EmailMessage
from typing import List

from errors.mail.MailFormatError import MailFormatError
from secrets.Secrets import MAILER_RECIPIENTS


class Email:
    id_stamp: str  # This parameter is optional, but helps to identify who send the email
    subject: str
    body: str
    sender: str
    recipients: List[str] = []

    def __init__(self, subject: str, body: str):
        """
        Initialize the email
        :param subject: Subject of the Email
        :param body: Content of the email
        """
        self.body = body
        self.subject = subject

    def add_recipient(self, recipient: str):
        """
        Add a single recipient to the mail
        :param recipient: Recipient to add
        :return: None
        """
        if not recipient in self.recipients:
            self.recipients.append(recipient)

    def add_recipients(self, recipients: List[str]):
        """
        Add a single recipient to the mail
        :param recipients: List of recipients to add
        :return: None
        """
        for r in recipients:
            self.add_recipient(r)

    def set_sender(self, sender: str):
        """
        Set the sender of the email.
        This parameter will be override by the Mailer engine
        :param sender: Sender
        :return:
        """
        self.sender = sender

    def set_id_stamp(self, stamp):
        """
        Set the id stamp of the email
        :param stamp: Stamp to assign
        :return: None
        """
        self.id_stamp = stamp

    def get_subject(self) -> str:
        return self.subject

    def get_body(self) -> str:
        return self.body

    def get_sender(self) -> str:
        return self.sender

    def get_recipients(self) -> List[str]:
        return self.recipients

    def get_id_stamp(self):
        return self.id_stamp

    def generate(self) -> EmailMessage:
        """
        Validate all the parameters of the email
        and return the representation of ot
        :raises MailFormatError If an argument is missing building the email
        :return:
        """
        if not self.subject:
            raise MailFormatError("Subject")

        if not self.body:
            raise MailFormatError("Body")

        if not self.sender:
            raise MailFormatError("Sender")

        if not self.recipients:
            raise MailFormatError("Recipients")

        msg = EmailMessage()
        msg['Subject'] = self.get_subject()
        msg['From'] = self.get_sender()
        msg['Date'] = email.utils.formatdate(localtime=True)
        msg['To'] = tuple(self.get_recipients())

        warn = f"THIS EMAIL HAS AUTOMATICALLY BEEN SENT FROM {self.get_id_stamp()}" if self.id_stamp else ""
        msg.set_content(f"{warn}\n"
                        f"\n"
                        f"{self.get_body()}")

        return msg
