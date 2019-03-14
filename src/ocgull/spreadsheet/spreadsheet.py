import json

from spreadsheet.sheet import Sheet


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
        self.gspreadsheet = gspreadsheet

    @property
    def sheets(self):
        return [
            Sheet(
                sheet['properties']['sheetId'],
                sheet['properties']['title'],
                bool(sheet.get('protectedRanges')),
            )
            for sheet in self.gspreadsheet.get('sheets', [])
        ]

    def dumps(self):
        return json.dumps(self.gspreadsheet)
