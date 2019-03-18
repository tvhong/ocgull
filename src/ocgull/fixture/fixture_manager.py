from os import path

from constants import Fixture

FIXTURE_DIR = path.dirname(path.realpath(__file__))


class FixtureManager():
    @classmethod
    def read_spreadsheet(cls, fixture=Fixture.AFTER):
        """
        Read contents of a spreadsheet fixture.

        :param fixture: The desired fixture.
        :return: string represents the spreadsheet.
        """
        file_path = path.join(FIXTURE_DIR, fixture)
        with open(file_path) as f:
            data = f.read()

        return data
