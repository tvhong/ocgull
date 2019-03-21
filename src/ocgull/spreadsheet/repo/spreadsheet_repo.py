import logging

from googleapiclient import discovery

from spreadsheet.spreadsheet import Spreadsheet

logger = logging.getLogger(__name__)

class SpreadsheetRepo():
    """
    Class to interact with Google sheets API.
    """

    def __init__(self, config, api_key):
        """
        :param config: The configuration for this repository.
        :type config: RepoConfig.
        :param api_key: The Google Cloud Platform API key.
        :type api_key: str.
        """
        self.spreadsheet_id = config.get_gspreadsheet_id()
        self.service = self._build_spreadsheet_service(api_key)

    def fetch(self):
        """Fetch latest sheet data from the OC signup spreadsheet."""
        gspreadsheet = self.service.spreadsheets().get(spreadsheetId=self.spreadsheet_id).execute()

        logger.info("Fetched latest spreadsheet.", extra={"gspreadsheet": gspreadsheet})
        return Spreadsheet(gspreadsheet)

    def _build_spreadsheet_service(self, api_key):
        return discovery.build('sheets', 'v4', developerKey=api_key)
