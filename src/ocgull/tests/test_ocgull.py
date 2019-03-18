from unittest import TestCase

from mock import Mock

from constants import ProtectionStatus
from fixture import FixtureManager
from ocgull import OcGull
from spreadsheet import Sheet, Spreadsheet


class TestOcGull(TestCase):
    def setUp(self):
        self.spreadsheet_repo = Mock()
        self.prev_spreadsheet_repo = Mock()
        self.notifier = Mock()
        self.gull = OcGull(
            self.spreadsheet_repo,
            self.prev_spreadsheet_repo,
            self.notifier,
        )

    def test_pull_failedFetchingSheets_bubbleError(self):
        self.spreadsheet_repo.fetch.side_effect = ValueError()

        with self.assertRaises(ValueError):
            self.gull.pull()

    def test_getUnlockedSheets_oneSheetUnlocked_returnSheet(self):
        prev_spreadsheet = self._create_stub_spreadsheet([
            (1, ProtectionStatus.LOCKED),
            (2, ProtectionStatus.LOCKED),
        ])
        spreadsheet = self._create_stub_spreadsheet([
            (1, ProtectionStatus.UNLOCKED),
            (2, ProtectionStatus.LOCKED),
        ])

        unlocked_sheets = self.gull._get_unlocked_sheets(spreadsheet, prev_spreadsheet)

        self.assertListEqual([self._create_sheet(1, ProtectionStatus.UNLOCKED)],
                unlocked_sheets)

    def test_getUnlockedSheets_multipleSheetsUnlocked_returnSheets(self):
        prev_spreadsheet = self._create_stub_spreadsheet([
            (1, ProtectionStatus.LOCKED),
            (2, ProtectionStatus.LOCKED),
            (3, ProtectionStatus.LOCKED),
        ])
        spreadsheet = self._create_stub_spreadsheet([
            (1, ProtectionStatus.UNLOCKED),
            (2, ProtectionStatus.UNLOCKED),
            (3, ProtectionStatus.LOCKED),
        ])

        unlocked_sheets = self.gull._get_unlocked_sheets(spreadsheet, prev_spreadsheet)

        expected_sheets = [
            self._create_sheet(1, ProtectionStatus.UNLOCKED),
            self._create_sheet(2, ProtectionStatus.UNLOCKED),
        ]
        self.assertListEqual(expected_sheets, unlocked_sheets)

    def test_getUnlockedSheets_noSheetsUnlocked_returnEmptyList(self):
        prev_spreadsheet = self._create_stub_spreadsheet([
            (1, ProtectionStatus.LOCKED),
            (2, ProtectionStatus.LOCKED),
        ])
        spreadsheet = self._create_stub_spreadsheet([
            (1, ProtectionStatus.LOCKED),
            (2, ProtectionStatus.LOCKED),
        ])

        unlocked_sheets = self.gull._get_unlocked_sheets(spreadsheet, prev_spreadsheet)

        self.assertListEqual([], unlocked_sheets)

    def test_getUnlockedSheets_prevSheetsNotThereAnyMore_ignoreSheet(self):
        prev_spreadsheet = self._create_stub_spreadsheet([
            (1, ProtectionStatus.LOCKED),
            (2, ProtectionStatus.LOCKED),
        ])
        spreadsheet = self._create_stub_spreadsheet([
            (2, ProtectionStatus.UNLOCKED),
        ])

        unlocked_sheets = self.gull._get_unlocked_sheets(spreadsheet, prev_spreadsheet)

        self.assertListEqual([self._create_sheet(2, ProtectionStatus.UNPROTECTED)],
                unlocked_sheets)

    def _create_stub_spreadsheet(self, sheets_info):
        """
        Create a stub spreadsheet given the sheets info.

        :param sheets_info: A list of (id, protection) tuples.
        :type sheets_info: [(int, ProtectionStatus)]
        """
        sheets = [self._create_sheet(si[0], si[1]) for si in sheets_info]

        return Mock(spec=Spreadsheet, sheets=sheets)

    def _create_sheet(self, id, protection):
        gsheet = FixtureManager.load_sheet(protection)
        gsheet['properties']['sheetId'] = id
        gsheet['properties']['title'] = 'Sheet {}'.format(id)
        return Sheet(gsheet)
