from abc import ABC, abstractmethod


class ILogical(ABC):
    """Interface for objects with logical functional"""
    @abstractmethod
    def process_logic(self) -> None:
        pass

    def additional_logic(self) -> None:
        pass
