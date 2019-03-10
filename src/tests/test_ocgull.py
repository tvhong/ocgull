from unittest import TestCase

from mock import Mock

from ocgull import OcGull, Sheet


class TestOcGull(TestCase):
    def setUp(self):
        self.sheets_repo = Mock()
        self.prev_sheets_repo = Mock()
        self.gull = OcGull(self.sheets_repo, self.prev_sheets_repo)

    def test_getUnlockedSheets_oneSheetUnlocked_returnSheet(self):
        self.prev_sheets_repo.fetch_protected_sheets.return_value = [
            Sheet(1, "Sheet 1", protected=True),
            Sheet(2, "Sheet 2", protected=True),
        ]
        self.sheets_repo.fetch.return_value = [
            Sheet(1, "Sheet 1", protected=False),
            Sheet(2, "Sheet 2", protected=True),
        ]

        unlocked_sheets = self.gull._get_unlocked_sheets()

        self.assertListEqual([Sheet(1, "Sheet 1")], unlocked_sheets)

    def test_getUnlockedSheets_multipleSheetsUnlocked_returnSheets(self):
        self.prev_sheets_repo.fetch_protected_sheets.return_value = [
            Sheet(1, "Sheet 1", protected=True),
            Sheet(2, "Sheet 2", protected=True),
            Sheet(3, "Sheet 3", protected=True),
        ]
        self.sheets_repo.fetch.return_value = [
            Sheet(1, "Sheet 1", protected=False),
            Sheet(2, "Sheet 2", protected=False),
            Sheet(3, "Sheet 3", protected=True),
        ]

        unlocked_sheets = self.gull._get_unlocked_sheets()

        self.assertListEqual(
                [Sheet(1, "Sheet 1"), Sheet(2, "Sheet 2")],
                unlocked_sheets)

    def test_getUnlockedSheets_noSheetsUnlocked_returnEmptyList(self):
        self.prev_sheets_repo.fetch_protected_sheets.return_value = [
            Sheet(1, "Sheet 1", protected=True),
            Sheet(2, "Sheet 2", protected=True),
        ]
        self.sheets_repo.fetch.return_value = [
            Sheet(1, "Sheet 1", protected=True),
            Sheet(2, "Sheet 2", protected=True),
        ]

        unlocked_sheets = self.gull._get_unlocked_sheets()

        self.assertListEqual([], unlocked_sheets)

    def test_getUnlockedSheets_noPrevProtectedSheets_returnEmptyList(self):
        self.prev_sheets_repo.fetch_protected_sheets.return_value = []
        self.sheets_repo.fetch.return_value = [
            Sheet(1, "Sheet 1", protected=True),
            Sheet(2, "Sheet 2", protected=True),
        ]

        unlocked_sheets = self.gull._get_unlocked_sheets()

        self.assertListEqual([], unlocked_sheets)

    def test_getUnlockedSheets_noNewProtectedSheets_returnAllPrevSheets(self):
        self.prev_sheets_repo.fetch_protected_sheets.return_value = [
            Sheet(1, "Sheet 1", protected=True),
            Sheet(2, "Sheet 2", protected=True),
        ]
        self.sheets_repo.fetch.return_value = [
            Sheet(1, "Sheet 1", protected=False),
            Sheet(2, "Sheet 2", protected=False),
            Sheet(3, "Sheet 3", protected=False),
        ]

        unlocked_sheets = self.gull._get_unlocked_sheets()

        self.assertListEqual(
                [Sheet(1, "Sheet 1"), Sheet(2, "Sheet 2")],
                unlocked_sheets)

    def test_getUnlockedSheets_prevSheetsNotThereAnyMore_ignoreSheet(self):
        self.prev_sheets_repo.fetch_protected_sheets.return_value = [
            Sheet(1, "Sheet 1", protected=True),
            Sheet(2, "Sheet 2", protected=True),
        ]
        self.sheets_repo.fetch.return_value = [
            Sheet(2, "Sheet 2", protected=False),
        ]

        unlocked_sheets = self.gull._get_unlocked_sheets()

        self.assertListEqual([Sheet(2, "Sheet 2")], unlocked_sheets)

    def test_getUnlockedSheets_failedFetchingSheets_bubbleError(self):
        self.prev_sheets_repo.fetch_protected_sheets.return_value = [
            Sheet(1, "Sheet 1", protected=True),
            Sheet(2, "Sheet 2", protected=True),
        ]
        self.sheets_repo.fetch.side_effect = ValueError()

        with self.assertRaises(ValueError):
            self.gull._get_unlocked_sheets()
