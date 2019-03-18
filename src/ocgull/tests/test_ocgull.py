from unittest import TestCase

from mock import Mock

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
        prev_spreadsheet = self._create_spreadsheet([
            self._create_gsheet(1, protected=True),
            self._create_gsheet(2, protected=True),
        ])
        spreadsheet = self._create_spreadsheet([
            self._create_gsheet(1, protected=False),
            self._create_gsheet(2, protected=True),
        ])

        unlocked_sheets = self.gull._get_unlocked_sheets(spreadsheet, prev_spreadsheet)

        self.assertListEqual([Sheet(self._create_gsheet(1))], unlocked_sheets)

    def test_getUnlockedSheets_multipleSheetsUnlocked_returnSheets(self):
        prev_spreadsheet = self._create_spreadsheet([
            self._create_gsheet(1, protected=True),
            self._create_gsheet(2, protected=True),
            self._create_gsheet(3, protected=True),
        ])
        spreadsheet = self._create_spreadsheet([
            self._create_gsheet(1, protected=False),
            self._create_gsheet(2, protected=False),
            self._create_gsheet(3, protected=True),
        ])

        unlocked_sheets = self.gull._get_unlocked_sheets(spreadsheet, prev_spreadsheet)

        self.assertListEqual(
                [Sheet(self._create_gsheet(1)), Sheet(self._create_gsheet(2))],
                unlocked_sheets)

    def test_getUnlockedSheets_noSheetsUnlocked_returnEmptyList(self):
        prev_spreadsheet = self._create_spreadsheet([
            self._create_gsheet(1, protected=True),
            self._create_gsheet(2, protected=True),
        ])
        spreadsheet = self._create_spreadsheet([
            self._create_gsheet(1, protected=True),
            self._create_gsheet(2, protected=True),
        ])

        unlocked_sheets = self.gull._get_unlocked_sheets(spreadsheet, prev_spreadsheet)

        self.assertListEqual([], unlocked_sheets)

    def test_getUnlockedSheets_noPrevProtectedSheets_returnEmptyList(self):
        prev_spreadsheet = self._create_spreadsheet([])
        spreadsheet = self._create_spreadsheet([
            self._create_gsheet(1, protected=True),
            self._create_gsheet(2, protected=True),
        ])

        unlocked_sheets = self.gull._get_unlocked_sheets(spreadsheet, prev_spreadsheet)

        self.assertListEqual([], unlocked_sheets)

    def test_getUnlockedSheets_noNewProtectedSheets_returnAllPrevSheets(self):
        prev_spreadsheet = self._create_spreadsheet([
            self._create_gsheet(1, protected=True),
            self._create_gsheet(2, protected=True),
        ])
        spreadsheet = self._create_spreadsheet([
            self._create_gsheet(1, protected=False),
            self._create_gsheet(2, protected=False),
            self._create_gsheet(3, protected=False),
        ])

        unlocked_sheets = self.gull._get_unlocked_sheets(spreadsheet, prev_spreadsheet)

        self.assertListEqual(
                [Sheet(self._create_gsheet(1)), Sheet(self._create_gsheet(2))],
                unlocked_sheets)

    def test_getUnlockedSheets_prevSheetsNotThereAnyMore_ignoreSheet(self):
        prev_spreadsheet = self._create_spreadsheet([
            self._create_gsheet(1, protected=True),
            self._create_gsheet(2, protected=True),
        ])
        spreadsheet = self._create_spreadsheet([
            self._create_gsheet(2, protected=False),
        ])

        unlocked_sheets = self.gull._get_unlocked_sheets(spreadsheet, prev_spreadsheet)

        self.assertListEqual([Sheet(self._create_gsheet(2))], unlocked_sheets)

    def _create_spreadsheet(self, gsheets):
        return Spreadsheet({'sheets': gsheets})

    def _create_gsheet(self, id, protected=False):
        gsheet = {
            'properties': {
                'sheetId': id,
                'title': "Sheet {}".format(id),
            },
        }
        if protected:
            gsheet['protectedRanges'] = True

        return gsheet
