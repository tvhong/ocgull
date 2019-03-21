from abc import ABC, abstractmethod


class Notifier(ABC):
    """
    Abstract class for notifiers.
    """
    @abstractmethod
    def send_notification(self):
        pass
