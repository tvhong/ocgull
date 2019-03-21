import json
import logging
import os
import sys

from constants import ProtectionStatus
from notifier import EmailNotifier, PrintNotifier
from spreadsheet.repo import (PreviousSpreadsheetRepo, RepoConfig,
                              SpreadsheetRepo)
from spreadsheet.repo.constants import Environment

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
        logger.info("Recently unlocked sheets", extra={"unlocked_sheets": result})
        return list(result)


def handleLambdaEvent(event, context):
    repoconfig = RepoConfig(Environment.PROD)
    api_key = os.environ.get('GCP_API_KEY')
    gull = OcGull(SpreadsheetRepo(repoconfig, api_key), PreviousSpreadsheetRepo(repoconfig), PrintNotifier())
    return {
        'statusCode': 200,
        'body': json.dumps([(sheet.id, sheet.title, sheet.protection) for sheet in gull.pull()])
    }


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    repoconfig = RepoConfig(Environment.DEV)
    api_key = sys.argv[1]
    gull = OcGull(SpreadsheetRepo(repoconfig, api_key), PreviousSpreadsheetRepo(repoconfig),
            EmailNotifier())
    print(gull.pull())
