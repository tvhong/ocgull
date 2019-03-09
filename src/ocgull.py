from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from os import path
import json


def handleLambdaEvent(event, context):
    gull = OcGull('./')
    protected_sheet_ids = gull.pull()
    return {
        'statusCode': 200,
        'body': json.dumps(protected_sheet_ids)
    }

class OcGull():
    # If modifying these scopes, delete the file token.json.
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

    # The ID and range of the interested spreadsheet.
    SPREADSHEET_ID = '1v4upQF2OknO9jHAPCvcawW86H5a1KRnc-dWfLHT0jZY'

    def __init__(self, secrets_path):
        self.secrets_path = secrets_path

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
        store = file.Storage(path.join(self.secrets_path, 'token.json'))
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(
                path.join(self.secrets_path, 'credentials.json'),
                self.SCOPES
            )
            creds = tools.run_flow(flow, store)

        service = discovery.build('sheets', 'v4', http=creds.authorize(Http()))

        return service
