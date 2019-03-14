import logging

from googleapiclient import discovery

from spreadsheet.spreadsheet import Spreadsheet

logger = logging.getLogger(__name__)

class SpreadsheetRepo():
    """
    Class to interact with Google sheets API.
    """

    SPREADSHEET_ID = '1qZCXaYM_gH8vft3InZlhEXixHOfZLtipm95FvhQ_Gqo'

    def __init__(self, api_key):
        self.service = self._build_spreadsheet_service(api_key)

    def fetch(self):
        """Fetch latest sheet data from the OC signup spreadsheet."""
        gspreadsheet = self.service.spreadsheets().get(spreadsheetId=self.SPREADSHEET_ID).execute()
        spreadsheet = Spreadsheet(gspreadsheet)

        logger.info("Fetched latest sheets.", extra={"sheets": spreadsheet.sheets})
        return spreadsheet.sheets

    def _build_spreadsheet_service(self, api_key):
        return discovery.build('sheets', 'v4', developerKey=api_key)
