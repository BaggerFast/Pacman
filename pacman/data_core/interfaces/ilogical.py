from abc import ABC


class ILogical(ABC):
    def update(self) -> None:
        raise NotImplementedError
