import json
import os
import sys

from previous_sheets_repo import PreviousSheetsRepo
from sheets_repo import SheetsRepo


class OcGull():
    """
    Core logic for the notification service.
    """

    def __init__(self, sheets_repo, prev_sheets_repo):
        self.sheets_repo = sheets_repo
        self.prev_sheets_repo = prev_sheets_repo

    def pull(self):
        """Find the unlocked sheets and create notification when there's one."""

        return self._get_unlocked_sheets()

    def _get_unlocked_sheets(self):
        sheets = set(self.sheets_repo.fetch())
        prev_protected_sheets = set(self.prev_sheets_repo.fetch_protected_sheets())
        prev_protected_sheets = prev_protected_sheets & sheets
        protected_sheets = set(sheet for sheet in sheets if sheet.protected)

        unlocked_sheets = prev_protected_sheets - protected_sheets

        return list(unlocked_sheets)


def handleLambdaEvent(event, context):
    api_key = os.environ.get('GCP_API_KEY')
    gull = OcGull(SheetsRepo(api_key), PreviousSheetsRepo())
    return {
        'statusCode': 200,
        'body': json.dumps([sheet.to_dict() for sheet in gull.pull()])
    }


if __name__ == '__main__':
    api_key = sys.argv[1]
    gull = OcGull(SheetsRepo(api_key), PreviousSheetsRepo())
    print(gull.pull())
