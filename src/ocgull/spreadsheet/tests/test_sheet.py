
from unittest import TestCase

from constants import Fixture, ProtectionStatus
from utils import load_fixture_spreadsheet


class TestSheet(TestCase):
    def setUp(self):
        self.spreadsheet = load_fixture_spreadsheet(Fixture.BEFORE)
        self.unlocked_sheet = [s for s in self.spreadsheet.sheets
                if s.title == 'OC1 Usage Rules'][0]

    def test_protectedStatus_unprotectedSheet_unprotectedStatus(self):
        self.assertEqual(ProtectionStatus.UNPROTECTED, self.unlocked_sheet.protection_status)
