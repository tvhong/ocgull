
from unittest import TestCase

from constants import ProtectionStatus
from fixture.constants import Fixture
from utils import load_fixture_spreadsheet


class TestSheet(TestCase):
    def setUp(self):
        self.spreadsheet = load_fixture_spreadsheet(Fixture.AFTER)
        self.unprotected_sheet = [s for s in self.spreadsheet.sheets
                if s.title == 'OC1 Damages'][0]
        self.protected_sheet = [s for s in self.spreadsheet.sheets
                if s.title == 'MAR 24 - MAR 30'][0]
        self.unlocked_sheet = [s for s in self.spreadsheet.sheets
                if s.title == 'MAR 17 - MAR 23'][0]

    def test_protectedStatus_unprotectedSheet_unprotectedStatus(self):
        self.assertEqual(ProtectionStatus.UNPROTECTED,
                self.unprotected_sheet.protection_status)

    def test_protectedStatus_protectedSheet_protectedStatus(self):
        self.assertEqual(ProtectionStatus.PROTECTED,
                self.protected_sheet.protection_status)

    def test_protectedStatus_unlockedSheet_unlockedStatus(self):
        self.assertEqual(ProtectionStatus.UNLOCKED,
                self.unlocked_sheet.protection_status)
