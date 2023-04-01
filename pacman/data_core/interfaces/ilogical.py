from abc import ABC


class ILocal(ABC):
    def update(self) -> None:
        raise NotImplementedError

    def secondary_update(self) -> None:
        pass
