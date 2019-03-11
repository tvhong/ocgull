import json
import os
import sys

from googleapiclient import discovery


class Sheet():
    """
    Data structure represents a Sheet.
    """

    def __init__(self, id, title, protected=False):
        self.id = id
        self.title = title
        self.protected = protected

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return str(self.id)

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

    PREV_PROTECTED_SHEETS = [
        Sheet(id=589148432123, title='BOOM!', protected=True),
        Sheet(id=589148479, title='OC1 Usage Rules', protected=True),
        Sheet(id=1192726443, title='OC1/Flatwater news (Please Read)', protected=True),
        Sheet(id=1394447626, title='DEC 09 - DEC 15', protected=True),
        Sheet(id=879674378, title='OCT 28 - NOV 03', protected=True),
        Sheet(id=1333024752, title='OCT 21 - OCT 27', protected=True),
        Sheet(id=873233306, title='OCT 07 - OCT 13', protected=True),
        Sheet(id=1544152156, title='SEP 30 - OCT 06', protected=True),
        Sheet(id=395761944, title='JULY 15 - JULY 21', protected=True),
        Sheet(id=2086915214, title='JULY 22 - JULY 28', protected=True),
        Sheet(id=1116728725, title='JULY 29 - AUG 4', protected=True),
        Sheet(id=1874836324, title='AUG 5 - AUG 11', protected=True),
        Sheet(id=1781950393, title='AUG 12 - AUG 18', protected=True),
        Sheet(id=1751513204, title='AUG 19 - AUG 25', protected=True),
        Sheet(id=1415661822, title='AUG 26 - SEP 1', protected=True),
        Sheet(id=798973055, title='SEP 2 - SEP 8', protected=True),
        Sheet(id=729061354, title='SEP 9 - SEP 15', protected=True),
        Sheet(id=1862557961, title='SEP 16 - SEP 22', protected=True),
        Sheet(id=1280390141, title='SEP 23 - SEP 29', protected=True),
        Sheet(id=2033923253, title='OCT 14 - OCT 20', protected=True),
        Sheet(id=1433915197, title='NOV 04 - NOV 10', protected=True),
        Sheet(id=1373566089, title='NOV 11 - NOV 17', protected=True),
        Sheet(id=1777459837, title='NOV 18 - NOV 24', protected=True),
        Sheet(id=1954205344, title='NOV 25 - DEC 01', protected=True),
        Sheet(id=1133137872, title='DEC 02 - DEC 08', protected=True),
        Sheet(id=936305205, title='DEC 16 - DEC 22', protected=True),
        Sheet(id=792088175, title='DEC 23 - DEC 29', protected=True),
        Sheet(id=1514881401, title='DEC 30 - JAN 5', protected=True),
        Sheet(id=162489332, title='JAN 6 - Jan 12', protected=True),
        Sheet(id=2035210929, title='JAN 13 - Jan 19', protected=True),
        Sheet(id=1674516027, title='JAN 20 - JAN 26', protected=True),
        Sheet(id=663065838, title='JAN 27 - FEB 2', protected=True),
        Sheet(id=1373408719, title='FEB 3 - FEB 9', protected=True),
        Sheet(id=2094748847, title='FEB 10 - FEB 16', protected=True),
        Sheet(id=720058275, title='FEB 17 - Feb 23', protected=True),
        Sheet(id=1437243646, title='FEB 24 - MAR 2', protected=True),
        Sheet(id=8966938, title='MAR 3 - MAR 9', protected=True),
        Sheet(id=499503122, title='MAR 10 - MAR 16', protected=True),
        Sheet(id=1891545419, title='MAR 17 - MAR 23', protected=True)
    ]

    def fetch_protected_sheets(self):
        return self.PREV_PROTECTED_SHEETS


def handleLambdaEvent(event, context):
    api_key = os.environ.get('GCP_API_KEY')
    gull = OcGull(SheetsRepo(api_key), PreviousSheetsRepo())
    return {
        'statusCode': 200,
        'body': json.dumps([sheet.title for sheet in gull.pull()])
    }


if __name__ == '__main__':
    api_key = sys.argv[1]
    gull = OcGull(SheetsRepo(api_key), PreviousSheetsRepo())
    print(gull.pull())
