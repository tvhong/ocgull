from fixture import FixtureManager
from fixture.constants import Fixture
from spreadsheet import Spreadsheet


def load_fixture_spreadsheet(fixture=Fixture.AFTER):
    return Spreadsheet(FixtureManager.load_spreadsheet(fixture))
