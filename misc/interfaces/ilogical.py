from abc import ABC, abstractmethod


class ILogical(ABC):

    @abstractmethod
    def process_logic(self) -> None:
        pass

    def additional_logic(self) -> None:
        pass
