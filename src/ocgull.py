import json
import logging
import os
import sys

import boto3
from googleapiclient import discovery

logger = logging.getLogger(__name__)

class Sheet():
    """
    Data structure represents a Sheet.
    """

    def __init__(self, id, title, protected=False):
        self.id = id
        self.title = title
        self.protected = protected

    @classmethod
    def from_dict(cls, data):
        return Sheet(**data)

    def to_dict(self):
        return self.__dict__

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return "Sheet({}, \"{}\", protected={})".format(
                self.id, self.title, self.protected)

    def __repr__(self):
        return str(self)


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


class SheetsRepo():
    """
    Class to interact with Google sheets API.
    """

    SPREADSHEET_ID = '1qZCXaYM_gH8vft3InZlhEXixHOfZLtipm95FvhQ_Gqo'

    def __init__(self, api_key):
        self.service = self._build_spreadsheet_service(api_key)

    def fetch(self):
        """Fetch latest sheet data from the OC signup spreadsheet."""
        spreadsheet = self.service.spreadsheets().get(spreadsheetId=self.SPREADSHEET_ID).execute()
        return [
            Sheet(
                sheet['properties']['sheetId'],
                sheet['properties']['title'],
                bool(sheet.get('protectedRanges')),
            )
            for sheet in spreadsheet.get('sheets', [])
        ]

    def _build_spreadsheet_service(self, api_key):
        return discovery.build('sheets', 'v4', developerKey=api_key)


class PreviousSheetsRepo():
    """
    Class to read previously stored sheets information.
    """
    BUCKET_NAME = 'ocgull-snapshots'
    LAST_SNAPSHOT = 'last-snapshot.json'

    def __init__(self):
        self.s3 = boto3.resource('s3')

    def fetch_sheets(self):
        try:
            obj = self.s3.Object(self.BUCKET_NAME, self.LAST_SNAPSHOT)
            response = obj.get()
            data = json.loads(response['Body'].read())
        except self.s3.meta.client.exceptions.NoSuchKey:
            logger.info("Last snapshot file does not exist yet.")
            data = []

        return [Sheet.from_dict(d) for d in data]

    def fetch_protected_sheets(self):
        return [sheet for sheet in self.fetch_sheets() if sheet.protected]


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
