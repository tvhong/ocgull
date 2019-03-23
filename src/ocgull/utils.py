from ocgull.fixture import FixtureManager
from ocgull.fixture.constants import Fixture
from ocgull.spreadsheet import Spreadsheet


def load_fixture_spreadsheet(fixture=Fixture.AFTER):
    return Spreadsheet(FixtureManager.load_spreadsheet(fixture))
