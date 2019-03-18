import json
from os import path

from constants import ProtectionStatus
from fixture.constants import Fixture

FIXTURE_DIR = path.dirname(path.realpath(__file__))


class FixtureManager():
    PROTECTION_TO_TITLE = {
        Fixture.BEFORE: {
            ProtectionStatus.UNPROTECTED: 'OC1 Damages',
            ProtectionStatus.PROTECTED: 'MAR 17 - MAR 23',
            ProtectionStatus.UNLOCKED: 'MAR 3 - MAR 9',
        },
        Fixture.AFTER: {
            ProtectionStatus.UNPROTECTED: 'OC1 Damages',
            ProtectionStatus.PROTECTED: 'MAR 24 - MAR 30',
            ProtectionStatus.UNLOCKED: 'MAR 17 - MAR 23',
        }
    }

    @classmethod
    def load_spreadsheet(cls, fixture=Fixture.AFTER):
        """
        Load a spreadsheet fixture into memory.

        :param fixture: The desired fixture.
        :return: dict represents the spreadsheet.
        """
        file_path = path.join(FIXTURE_DIR, fixture)
        with open(file_path) as f:
            json_str = f.read()

        return json.loads(json_str)

    @classmethod
    def load_sheet(cls, protection, fixture=Fixture.AFTER):
        """
        Load a sheet fixture into memory.

        :param protection: The desired protection level of the sheet.
        :param fixture: The desired fixture.
        :return: dict represents the sheet.
        """
        gspreadsheet = cls.load_spreadsheet(fixture)
        return next(s for s in gspreadsheet['sheets']
                if s['properties']['title'] == cls.PROTECTION_TO_TITLE[fixture][protection])
