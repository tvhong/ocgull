import json
from os import path

from fixture.constants import Fixture

FIXTURE_DIR = path.dirname(path.realpath(__file__))


class FixtureManager():
    @classmethod
    def load_spreadsheet(cls, fixture=Fixture.AFTER):
        """
        Load a spreadsheet fixture into memory.

        :param fixture: The desired fixture.
        :return: dict string represents the spreadsheet.
        """
        file_path = path.join(FIXTURE_DIR, fixture)
        with open(file_path) as f:
            json_str = f.read()

        return json.loads(json_str)
