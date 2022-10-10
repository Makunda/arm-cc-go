from enum import Enum


class Language(Enum):
    GO = "golang",
    DOTNET = "dotnet"

    @staticmethod
    def from_str(label: str):
        if label in [x.value for x in Language]:
            return Language[label]
        else:
            raise NotImplementedError(f"Incompatible language [{label}]")
