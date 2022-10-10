from enum import Enum


class Language(Enum):
    GO = "golang"
    DOTNET = "dotnet"

    @staticmethod
    def from_str(label: str) -> 'Language':
        if label == str(Language.DOTNET.value):
            return Language.DOTNET
        if label == str(Language.GO.value):
            return Language.GO
        else:
            raise NotImplementedError(f"Incompatible language [{label}]")
