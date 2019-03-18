import json
import logging
import os
import sys

from notifier import EmailNotifier, PrintNotifier
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
        prev_spreadsheet = self.prev_spreadsheet_repo.fetch()

        unlocked_sheets = self._get_unlocked_sheets(spreadsheet, prev_spreadsheet)
        self.notifier.send_notification(unlocked_sheets)

        self.prev_spreadsheet_repo.save_snapshot(spreadsheet)

        return unlocked_sheets

    def _get_unlocked_sheets(self, spreadsheet, prev_spreadsheet):
        sheets = set(spreadsheet.sheets)
        prev_sheets = set(prev_spreadsheet.sheets)

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
        'body': json.dumps([(sheet.id, sheet.title, sheet.protected) for sheet in gull.pull()])
    }


if __name__ == '__main__':
    api_key = sys.argv[1]
    gull = OcGull(SpreadsheetRepo(api_key), PreviousSpreadsheetRepo(), EmailNotifier())
    print(gull.pull())
