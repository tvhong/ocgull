import json
import logging
import os
import sys

from email_notifier import EmailNotifier
from previous_sheets_repo import PreviousSheetsRepo
from print_notifier import PrintNotifier
from sheets_repo import SheetsRepo

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

class OcGull():
    """
    Core logic for the notification service.
    """

    def __init__(self, sheets_repo, prev_sheets_repo, notifier):
        self.sheets_repo = sheets_repo
        self.prev_sheets_repo = prev_sheets_repo
        self.notifier = notifier

    def pull(self):
        """Find the unlocked sheets and create notification when there's one."""

        sheets = self.sheets_repo.fetch()
        prev_sheets = self.prev_sheets_repo.fetch()

        unlocked_sheets = self._get_unlocked_sheets(sheets, prev_sheets)
        self.notifier.send_notification(unlocked_sheets)

        self.prev_sheets_repo.save_snapshot(sheets)

        return unlocked_sheets

    def _get_unlocked_sheets(self, sheets, prev_sheets):
        sheets = set(sheets)
        prev_sheets = set(prev_sheets)

        prev_protected_sheets = set(
                sheet for sheet in prev_sheets
                if sheet.protected)
        prev_protected_sheets = prev_protected_sheets & sheets
        protected_sheets = set(sheet for sheet in sheets if sheet.protected)

        unlocked_sheets = prev_protected_sheets - protected_sheets

        logger.info("Calculated unlocked sheets", extra={"unlocked_sheets": unlocked_sheets})
        return list(unlocked_sheets)


def handleLambdaEvent(event, context):
    api_key = os.environ.get('GCP_API_KEY')
    gull = OcGull(SheetsRepo(api_key), PreviousSheetsRepo(), PrintNotifier())
    return {
        'statusCode': 200,
        'body': json.dumps([sheet.to_dict() for sheet in gull.pull()])
    }


if __name__ == '__main__':
    api_key = sys.argv[1]
    gull = OcGull(SheetsRepo(api_key), PreviousSheetsRepo(), EmailNotifier())
    print(gull.pull())
