from os import path

from constants import Fixture
from spreadsheet.spreadsheet import Spreadsheet

FIXTURE_DIR = path.join('.', 'fixtures/')


def load_fixture_spreadsheet(fixture=Fixture.AFTER):
    file_path = path.join(FIXTURE_DIR, fixture)
    with open(file_path) as f:
        data = f.read()

    return Spreadsheet.loads(data)
