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
            (1, ProtectionStatus.PROTECTED),
            (2, ProtectionStatus.PROTECTED),
        ])
        spreadsheet = self._create_stub_spreadsheet([
            (1, ProtectionStatus.UNPROTECTED),
            (2, ProtectionStatus.PROTECTED),
        ])

        unlocked_sheets = self.gull._get_unlocked_sheets(spreadsheet, prev_spreadsheet)

        expected_sheets = self._create_stub_spreadsheet([
            (1, ProtectionStatus.UNPROTECTED)
        ]).sheets
        self.assertListEqual(expected_sheets, unlocked_sheets)

    def test_getUnlockedSheets_multipleSheetsUnlocked_returnSheets(self):
        prev_spreadsheet = self._create_stub_spreadsheet([
            (1, ProtectionStatus.PROTECTED),
            (2, ProtectionStatus.PROTECTED),
            (3, ProtectionStatus.PROTECTED),
        ])
        spreadsheet = self._create_stub_spreadsheet([
            (1, ProtectionStatus.UNPROTECTED),
            (2, ProtectionStatus.UNPROTECTED),
            (3, ProtectionStatus.PROTECTED),
        ])

        unlocked_sheets = self.gull._get_unlocked_sheets(spreadsheet, prev_spreadsheet)

        expected_sheets = self._create_stub_spreadsheet([
            (1, ProtectionStatus.UNPROTECTED),
            (2, ProtectionStatus.UNPROTECTED),
        ]).sheets
        self.assertListEqual(expected_sheets, unlocked_sheets)

    def test_getUnlockedSheets_noSheetsUnlocked_returnEmptyList(self):
        prev_spreadsheet = self._create_stub_spreadsheet([
            (1, ProtectionStatus.PROTECTED),
            (2, ProtectionStatus.PROTECTED),
        ])
        spreadsheet = self._create_stub_spreadsheet([
            (1, ProtectionStatus.PROTECTED),
            (2, ProtectionStatus.PROTECTED),
        ])

        unlocked_sheets = self.gull._get_unlocked_sheets(spreadsheet, prev_spreadsheet)

        self.assertListEqual([], unlocked_sheets)

    def test_getUnlockedSheets_noPrevProtectedSheets_returnEmptyList(self):
        prev_spreadsheet = self._create_stub_spreadsheet([])
        spreadsheet = self._create_stub_spreadsheet([
            (1, ProtectionStatus.PROTECTED),
            (2, ProtectionStatus.PROTECTED),
        ])

        unlocked_sheets = self.gull._get_unlocked_sheets(spreadsheet, prev_spreadsheet)

        self.assertListEqual([], unlocked_sheets)

    def test_getUnlockedSheets_noNewProtectedSheets_returnAllPrevSheets(self):
        prev_spreadsheet = self._create_stub_spreadsheet([
            (1, ProtectionStatus.PROTECTED),
            (2, ProtectionStatus.PROTECTED),
        ])
        spreadsheet = self._create_stub_spreadsheet([
            (1, ProtectionStatus.UNPROTECTED),
            (2, ProtectionStatus.UNPROTECTED),
            (3, ProtectionStatus.UNPROTECTED),
        ])

        unlocked_sheets = self.gull._get_unlocked_sheets(spreadsheet, prev_spreadsheet)

        expected_sheets = self._create_stub_spreadsheet([
            (1, ProtectionStatus.UNPROTECTED),
            (2, ProtectionStatus.UNPROTECTED),
        ]).sheets
        self.assertListEqual(expected_sheets, unlocked_sheets)

    def test_getUnlockedSheets_prevSheetsNotThereAnyMore_ignoreSheet(self):
        prev_spreadsheet = self._create_stub_spreadsheet([
            (1, ProtectionStatus.PROTECTED),
            (2, ProtectionStatus.PROTECTED),
        ])
        spreadsheet = self._create_stub_spreadsheet([
            (2, ProtectionStatus.UNPROTECTED),
        ])

        unlocked_sheets = self.gull._get_unlocked_sheets(spreadsheet, prev_spreadsheet)

        expected_sheets = self._create_stub_spreadsheet([
            (2, ProtectionStatus.UNPROTECTED),
        ]).sheets
        self.assertListEqual(expected_sheets, unlocked_sheets)

    def _create_stub_spreadsheet(self, sheets_info):
        """
        Create a stub spreadsheet given the sheets info.

        :param sheets_info: A list of (id, protection) tuples.
        :type sheets_info: [(int, ProtectionStatus)]
        """
        sheets = []
        for sheet_info in sheets_info:
            gsheet = FixtureManager.load_sheet(sheet_info[1])
            gsheet['properties']['sheetId'] = sheet_info[0]
            gsheet['properties']['title'] = 'Sheet {}'.format(sheet_info[0])
            sheets.append(Sheet(gsheet))

        return Mock(spec=Spreadsheet, sheets=sheets)
