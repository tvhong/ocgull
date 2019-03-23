import json
import logging

from ocgull.spreadsheet.sheet import Sheet

logger = logging.getLogger(__name__)

class Spreadsheet():
    """
    Class to encapsulate the Google spreadsheet object.
    """

    @classmethod
    def loads(cls, json_str):
        return Spreadsheet(json.loads(json_str))

    def __init__(self, gspreadsheet):
        """
        :param gspreadsheet: The Google spreadsheet data.
        :type gspreadsheet: dict()
        """
        if type(gspreadsheet) != dict:
            logger.error("Expect gspreadsheet to be of type dict",
                    extra={"gspreadsheet": gspreadsheet})
            raise ValueError("Expect gspreadsheet to be of type dict, instead get {}".format(type(gspreadsheet)))

        self._gspreadsheet = gspreadsheet

    @property
    def spreadsheet(self):
        return self._spreadsheet

    @property
    def sheets(self):
        return [
            Sheet(gsheet)
            for gsheet in self._gspreadsheet.get('sheets', [])
        ]

    def dumps(self):
        """
        Dumps a JSON string of this spreadsheet
        """
        return json.dumps(self._gspreadsheet)
