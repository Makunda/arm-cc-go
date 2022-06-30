import copy
from typing import List

from secrets.Secrets import MAILER_RECIPIENTS


class MailerUtils:
    """
        Utilities methods related to mailer parameters
    """

    @staticmethod
    def get_default_recipients() -> List[str]:
        """
        Get the list of default recipients for the mail server
        :return:
        """
        return copy.deepcopy(MAILER_RECIPIENTS)
