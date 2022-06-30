import json


class SerializableUtils:
    """
    Utilities related to JSON serialization
    """

    @staticmethod
    def is_jsonable(x) -> bool:
        try:
            json.dumps(x)
            return True
        except (TypeError, OverflowError):
            return False
