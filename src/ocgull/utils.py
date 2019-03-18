from os import path

from constants import Fixture
from fixtures.fixture_manager import FixtureManager
from spreadsheet.spreadsheet import Spreadsheet

FIXTURE_DIR = path.join('.', 'fixtures/')


def load_fixture_spreadsheet(fixture=Fixture.AFTER):
    return Spreadsheet.loads(FixtureManager.read_spreadsheet(fixture))
