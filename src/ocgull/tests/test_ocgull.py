from unittest import TestCase

from mock import Mock

from ocgull import OcGull
from spreadsheet.sheet import Sheet


class TestOcGull(TestCase):
    def setUp(self):
        self.sheets_repo = Mock()
        self.prev_sheets_repo = Mock()
        self.notifier = Mock()
        self.gull = OcGull(
            self.sheets_repo,
            self.prev_sheets_repo,
            self.notifier,
        )

    def test_pull_failedFetchingSheets_bubbleError(self):
        self.prev_sheets_repo.fetch.return_value = [
            self._create_sheet(1, protected=True),
            self._create_sheet(2, protected=True),
        ]
        self.sheets_repo.fetch.side_effect = ValueError()

        with self.assertRaises(ValueError):
            self.gull.pull()

    def test_getUnlockedSheets_oneSheetUnlocked_returnSheet(self):
        prev_sheets = [
            self._create_sheet(1, protected=True),
            self._create_sheet(2, protected=True),
        ]
        sheets = [
            self._create_sheet(1, protected=False),
            self._create_sheet(2, protected=True),
        ]

        unlocked_sheets = self.gull._get_unlocked_sheets(sheets, prev_sheets)

        self.assertListEqual([self._create_sheet(1)], unlocked_sheets)

    def test_getUnlockedSheets_multipleSheetsUnlocked_returnSheets(self):
        prev_sheets = [
            self._create_sheet(1, protected=True),
            self._create_sheet(2, protected=True),
            self._create_sheet(3, protected=True),
        ]
        sheets = [
            self._create_sheet(1, protected=False),
            self._create_sheet(2, protected=False),
            self._create_sheet(3, protected=True),
        ]

        unlocked_sheets = self.gull._get_unlocked_sheets(sheets, prev_sheets)

        self.assertListEqual(
                [self._create_sheet(1), self._create_sheet(2)],
                unlocked_sheets)

    def test_getUnlockedSheets_noSheetsUnlocked_returnEmptyList(self):
        prev_sheets = [
            self._create_sheet(1, protected=True),
            self._create_sheet(2, protected=True),
        ]
        sheets = [
            self._create_sheet(1, protected=True),
            self._create_sheet(2, protected=True),
        ]

        unlocked_sheets = self.gull._get_unlocked_sheets(sheets, prev_sheets)

        self.assertListEqual([], unlocked_sheets)

    def test_getUnlockedSheets_noPrevProtectedSheets_returnEmptyList(self):
        prev_sheets = []
        sheets = [
            self._create_sheet(1, protected=True),
            self._create_sheet(2, protected=True),
        ]

        unlocked_sheets = self.gull._get_unlocked_sheets(sheets, prev_sheets)

        self.assertListEqual([], unlocked_sheets)

    def test_getUnlockedSheets_noNewProtectedSheets_returnAllPrevSheets(self):
        prev_sheets = [
            self._create_sheet(1, protected=True),
            self._create_sheet(2, protected=True),
        ]
        sheets = [
            self._create_sheet(1, protected=False),
            self._create_sheet(2, protected=False),
            self._create_sheet(3, protected=False),
        ]

        unlocked_sheets = self.gull._get_unlocked_sheets(sheets, prev_sheets)

        self.assertListEqual(
                [self._create_sheet(1), self._create_sheet(2)],
                unlocked_sheets)

    def test_getUnlockedSheets_prevSheetsNotThereAnyMore_ignoreSheet(self):
        prev_sheets = [
            self._create_sheet(1, protected=True),
            self._create_sheet(2, protected=True),
        ]
        sheets = [
            self._create_sheet(2, protected=False),
        ]

        unlocked_sheets = self.gull._get_unlocked_sheets(sheets, prev_sheets)

        self.assertListEqual([self._create_sheet(2)], unlocked_sheets)

    def _create_sheet(self, id, protected=False):
        gsheet = {
            'properties': {
                'sheetId': id,
                'title': "Sheet {}".format(id),
            },
        }
        if protected:
            gsheet['protectedRanges'] = True

        return Sheet(gsheet)
