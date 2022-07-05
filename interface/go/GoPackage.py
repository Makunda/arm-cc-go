from interface.Package import Package


class GoPackage(Package):
    """
    Extend the package class for Go Lang
    """
    
    def __init__(self, name: str, version: str, origin: str = ""):
        super(GoPackage, self).__init__(name, version, origin)
        
    def get_id(self):
        """
        Get the golang identifier to pull the package
        """
        return f"{self.name}@{self.origin}"
