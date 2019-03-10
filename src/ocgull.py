import json
import os
import sys

from googleapiclient import discovery


class Sheet():
    def __init__(self, id, title, protected):
        self.id = id
        self.title = title
        self.protected = protected

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str(self)

class OcGull():
    SPREADSHEET_ID = '1qZCXaYM_gH8vft3InZlhEXixHOfZLtipm95FvhQ_Gqo'

    def __init__(self, api_key):
        self.api_key = api_key

    def pull(self):
        """and create notification
        when there are interesting changes."""

        return self.fetch_protected_sheet_ids()

    def fetch_protected_sheet_ids(self):
        """Fetch latest data from the OC signup spreadsheet."""

        # Read from a stored file that contains the protected_sheets ids.
        # Get current protected_sheets
        # unlocked_sheets = (set(prev_protected_sheets) - set(protected_sheets)).intersect(all_sheets)
        # if set(protected_sheets) - set(prev_protected_sheets)
        #  write a new protected_sheets file
        #  create a notification
        # exit
        service = self._get_spreadsheet_service()
        spreadsheet = service.spreadsheets().get(spreadsheetId=self.SPREADSHEET_ID).execute()
        sheets = [
            Sheet(
                sheet['properties']['sheetId'],
                sheet['properties']['title'],
                bool(sheet.get('protectedRanges')),
            )
            for sheet in spreadsheet.get('sheets', [])
        ]
        protected_sheets = [sheet for sheet in sheets if sheet.protected]

        return protected_sheets

        # sheet['protectedRanges']
        # [{'protectedRangeId': 639046925, 'range': {'sheetId': 1333024752}}]

    def _get_spreadsheet_service(self):
        service = discovery.build('sheets', 'v4', developerKey=self.api_key)

        return service

def handleLambdaEvent(event, context):
    api_key = os.environ.get('GCP_API_KEY')
    gull = OcGull(api_key)
    return {
        'statusCode': 200,
        'body': json.dumps(gull.pull())
    }

if __name__ == '__main__':
    api_key = sys.argv[1]
    gull = OcGull(api_key)
    print(gull.pull())
