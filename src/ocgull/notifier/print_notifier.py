from ocgull.notifier.base import Notifier


class PrintNotifier(Notifier):
    def send_notification(self, unlocked_sheets):
        print(unlocked_sheets)
