from typing import Optional


class Package:
    """
    Incoming package to scan
    """
    name: str
    version: str
    target: str
    origin: str

    def __init__(self, name: str, version: str, origin: str = "", target: str = ""):
        self.name = name
        self.version = version
        self.origin = origin
        self.target = target

    def serialize(self) -> dict:
        """
        Return the dictionary representation of the object
        """
        return {
            "name": self.name,
            "version": self.version,
            "origin": self.origin,
            "target": self.target,
        }

    def to_string(self) -> str:
        return f"Package [name={self.name}, version={self.version}, origin={self.origin}, target={self.target}]"
