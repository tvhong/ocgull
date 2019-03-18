
from unittest import TestCase

from constants import ProtectionStatus
from fixture import FixtureManager
from fixture.constants import Fixture
from spreadsheet import Sheet
from utils import load_fixture_spreadsheet


class TestSheet(TestCase):
    def setUp(self):
        self.spreadsheet = load_fixture_spreadsheet(Fixture.AFTER)
        self.unprotected_sheet = Sheet(FixtureManager.load_sheet(ProtectionStatus.UNPROTECTED))
        self.protected_sheet = Sheet(FixtureManager.load_sheet(ProtectionStatus.LOCKED))
        self.unlocked_sheet = Sheet(FixtureManager.load_sheet(ProtectionStatus.UNLOCKED))

    def test_protectedStatus_unprotectedSheet_unprotectedStatus(self):
        self.assertEqual(ProtectionStatus.UNPROTECTED,
                self.unprotected_sheet.protection)

    def test_protectedStatus_protectedSheet_protectedStatus(self):
        self.assertEqual(ProtectionStatus.LOCKED,
                self.protected_sheet.protection)

    def test_protectedStatus_unlockedSheet_unlockedStatus(self):
        self.assertEqual(ProtectionStatus.UNLOCKED,
                self.unlocked_sheet.protection)
