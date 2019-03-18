from fixture.constants import Fixture
from fixture.fixture_manager import FixtureManager
from spreadsheet.spreadsheet import Spreadsheet


def load_fixture_spreadsheet(fixture=Fixture.AFTER):
    return Spreadsheet.loads(FixtureManager.read_spreadsheet(fixture))
