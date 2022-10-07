import base64


class StringUtils:
    """
    String utils function
    """

    @staticmethod
    def to_base64(text: str):
        """
        Convert the text into base 64
        :param text: Text to convert
        :return: The text converted to base 64
        """
        message_bytes = text.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        return base64_bytes.decode('ascii')

    @staticmethod
    def truncate(text: str, length: int) -> str:
        if not text:
            return ""
        else:
            return (text[:length] + '..') if len(text) > length else text

    @staticmethod
    def is_blank(text: str) -> bool:
        """
        Verify if a text is blank or not
        """
        text = text.strip()
        return not text or text == ""
