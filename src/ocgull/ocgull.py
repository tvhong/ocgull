import json
import logging
import os
import sys

from notifiers.email_notifier import EmailNotifier
from notifiers.print_notifier import PrintNotifier
from spreadsheet.previous_spreadsheet_repo import PreviousSpreadsheetRepo
from spreadsheet.spreadsheet_repo import SpreadsheetRepo

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

class OcGull():
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
        prev_sheets = self.prev_spreadsheet_repo.fetch()

        unlocked_sheets = self._get_unlocked_sheets(spreadsheet.sheets, prev_sheets)
        self.notifier.send_notification(unlocked_sheets)

        self.prev_spreadsheet_repo.save_snapshot(spreadsheet.sheets)

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
    gull = OcGull(SpreadsheetRepo(api_key), PreviousSpreadsheetRepo(), PrintNotifier())
    return {
        'statusCode': 200,
        'body': json.dumps([sheet.to_dict() for sheet in gull.pull()])
    }


if __name__ == '__main__':
    api_key = sys.argv[1]
    gull = OcGull(SpreadsheetRepo(api_key), PreviousSpreadsheetRepo(), EmailNotifier())
    print(gull.pull())
