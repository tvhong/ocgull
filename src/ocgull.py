import json
import os
import sys

from googleapiclient import discovery


class OcGull():
    SPREADSHEET_ID = '1qZCXaYM_gH8vft3InZlhEXixHOfZLtipm95FvhQ_Gqo'

    def __init__(self, api_key):
        self.api_key = api_key

    def pull(self):
        """and create notification
        when there are interesting changes."""

        protected_sheet_ids = self.fetch_protected_sheet_ids()
        return protected_sheet_ids

    def fetch_protected_sheet_ids(self):
        """Fetch latest data from the OC signup spreadsheet."""

        # Read from a stored file that contains the protected_range_sheets ids.
        # Get current protected_range_sheets
        # if set(protected_range_sheets) - set(old_protected_range_sheets)
        #  write a new protected_range_sheets file
        #  create a notification
        # exit
        service = self._get_spreadsheet_service()
        spreadsheet = service.spreadsheets().get(spreadsheetId=self.SPREADSHEET_ID).execute()
        sheets = spreadsheet.get('sheets', [])
        protected_sheet_ids = [
            sheet['properties']['sheetId']
            for sheet in sheets
            if sheet.get('protectedRanges')
        ]

        return protected_sheet_ids

        # sheet['protectedRanges']
        # [{'protectedRangeId': 639046925, 'range': {'sheetId': 1333024752}}]

    def _get_spreadsheet_service(self):
        service = discovery.build('sheets', 'v4', developerKey=self.api_key)

        return service

def handleLambdaEvent(event, context):
    api_key = os.environ.get('GCP_API_KEY')
    gull = OcGull(api_key)
    protected_sheet_ids = gull.pull()
    return {
        'statusCode': 200,
        'body': json.dumps(protected_sheet_ids)
    }

if __name__ == '__main__':
    api_key = sys.argv[1]
    gull = OcGull(api_key)
    print(gull.pull())
