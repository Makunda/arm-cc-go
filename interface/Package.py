class Package:
    """
    Incoming package to scan
    """
    name: str
    version: str
    origin: str

    def __init__(self, name: str, version: str, origin: str = ""):
        self.name = name
        self.version = version
        self.origin = origin

    def serialize(self) -> dict:
        """
        Return the dictionary representation of the object
        """
        return {
            "name": self.name,
            "version": self.version,
            "origin": self.origin
        }
