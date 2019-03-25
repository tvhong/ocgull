import logging

from ocgull.constants import ProtectionStatus

logger = logging.getLogger(__name__)

class Ocgull():
    """
    Core logic for the notification service.
    """

    def __init__(self, spreadsheet_repo, prev_spreadsheet_repo, notifier):
        self.spreadsheet_repo = spreadsheet_repo
        self.prev_spreadsheet_repo = prev_spreadsheet_repo
        self.notifier = notifier

    def pull(self):
        """Find the unlocked sheets and create notification when there's one."""

        spreadsheet = self.spreadsheet_repo.fetch()
        prev_spreadsheet = self.prev_spreadsheet_repo.fetch()

        unlocked_sheets = self._get_recently_unlocked_sheets(spreadsheet, prev_spreadsheet)
        if unlocked_sheets:
            self.notifier.send_notification(unlocked_sheets)
            self.prev_spreadsheet_repo.save_snapshot(spreadsheet)

        return unlocked_sheets

    def _get_recently_unlocked_sheets(self, spreadsheet, prev_spreadsheet):
        prev_unlocked_sheets = set(sheet for sheet in prev_spreadsheet.sheets
                if sheet.protection == ProtectionStatus.UNLOCKED)
        curr_unlocked_sheets = set(sheet for sheet in spreadsheet.sheets
                if sheet.protection == ProtectionStatus.UNLOCKED)

        result = curr_unlocked_sheets - prev_unlocked_sheets
        logger.info("Recently unlocked sheets: {}.".format([s.title for s in result]))
        return list(result)
