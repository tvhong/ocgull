from unittest import TestCase

from mock import Mock

from ocgull.constants import ProtectionStatus
from ocgull.fixture import FixtureManager
from ocgull.fixture.constants import Fixture
from ocgull.notifier import Notifier
from ocgull.ocgull import Ocgull
from ocgull.spreadsheet import Sheet, Spreadsheet
from ocgull.spreadsheet.repo import PreviousSpreadsheetRepo, SpreadsheetRepo


class TestOcGull(TestCase):
    def setUp(self):
        self.spreadsheet_repo = Mock(spec=SpreadsheetRepo)
        self.prev_spreadsheet_repo = Mock(spec=PreviousSpreadsheetRepo)
        self.notifier = Mock(spec=Notifier)
        self.gull = Ocgull(
            self.spreadsheet_repo,
            self.prev_spreadsheet_repo,
            self.notifier,
        )

    def test_patrol_failedFetchingSheets_bubbleError(self):
        self.spreadsheet_repo.fetch.side_effect = ValueError()

        with self.assertRaises(ValueError):
            self.gull.patrol()

    def test_patrol_lockedSheetCreated_noNotification(self):
        self.prev_spreadsheet_repo.fetch.return_value = self._create_stub_spreadsheet([])
        self.spreadsheet_repo.fetch.return_value = self._create_stub_spreadsheet([
            (1, ProtectionStatus.LOCKED),
        ])

        self.gull.patrol()

        self.notifier.send_notification.assert_not_called()

    def test_patrol_unprotectedSheetCreated_noNotification(self):
        self.prev_spreadsheet_repo.fetch.return_value = self._create_stub_spreadsheet([])
        self.spreadsheet_repo.fetch.return_value = self._create_stub_spreadsheet([
            (1, ProtectionStatus.UNPROTECTED),
        ])

        self.gull.patrol()

        self.notifier.send_notification.assert_not_called()

    def test_patrol_unlockedSheetCreated_sendNotificationForSheet(self):
        self.prev_spreadsheet_repo.fetch.return_value = self._create_stub_spreadsheet([])
        self.spreadsheet_repo.fetch.return_value = self._create_stub_spreadsheet([
            (1, ProtectionStatus.UNLOCKED),
        ])

        self.gull.patrol()

        self.notifier.send_notification.assert_called_once_with([
            self._create_sheet(1, ProtectionStatus.UNLOCKED),
        ])

    def test_patrol_oneSheetUnlocked_sendNotificationForSheet(self):
        self.prev_spreadsheet_repo.fetch.return_value = self._create_stub_spreadsheet([
            (1, ProtectionStatus.UNPROTECTED),
            (2, ProtectionStatus.LOCKED),
            (3, ProtectionStatus.LOCKED),
        ])
        self.spreadsheet_repo.fetch.return_value = self._create_stub_spreadsheet([
            (1, ProtectionStatus.UNPROTECTED),
            (2, ProtectionStatus.UNLOCKED),
            (3, ProtectionStatus.LOCKED),
        ])

        self.gull.patrol()

        self.notifier.send_notification.assert_called_once_with([
            self._create_sheet(2, ProtectionStatus.UNLOCKED),
        ])

    def test_patrol_multipleSheetsUnlocked_sendNotificationForSheets(self):
        self.prev_spreadsheet_repo.fetch.return_value = self._create_stub_spreadsheet([
            (1, ProtectionStatus.UNPROTECTED),
            (2, ProtectionStatus.LOCKED),
            (3, ProtectionStatus.LOCKED),
        ])
        self.spreadsheet_repo.fetch.return_value = self._create_stub_spreadsheet([
            (1, ProtectionStatus.UNPROTECTED),
            (2, ProtectionStatus.UNLOCKED),
            (3, ProtectionStatus.UNLOCKED),
        ])

        self.gull.patrol()

        self.notifier.send_notification.assert_called_once_with([
            self._create_sheet(2, ProtectionStatus.UNLOCKED),
            self._create_sheet(3, ProtectionStatus.UNLOCKED),
        ])

    def test_patrol_noSheetsUnlocked_noNotification(self):
        self.prev_spreadsheet_repo.fetch.return_value = self._create_stub_spreadsheet([
            (1, ProtectionStatus.UNPROTECTED),
            (2, ProtectionStatus.LOCKED),
            (3, ProtectionStatus.LOCKED),
        ])
        self.spreadsheet_repo.fetch.return_value = self._create_stub_spreadsheet([
            (1, ProtectionStatus.UNPROTECTED),
            (2, ProtectionStatus.LOCKED),
            (3, ProtectionStatus.LOCKED),
        ])

        self.gull.patrol()

        self.notifier.send_notification.assert_not_called()

    def test_patrol_noSheetsUnlocked_dontSaveSnapshot(self):
        self.prev_spreadsheet_repo.fetch.return_value = self._create_stub_spreadsheet([
            (1, ProtectionStatus.UNPROTECTED),
            (2, ProtectionStatus.LOCKED),
            (3, ProtectionStatus.LOCKED),
        ])
        self.spreadsheet_repo.fetch.return_value = self._create_stub_spreadsheet([
            (1, ProtectionStatus.UNPROTECTED),
            (2, ProtectionStatus.LOCKED),
            (3, ProtectionStatus.LOCKED),
        ])

        self.gull.patrol()

        self.prev_spreadsheet_repo.save_snapshot.assert_not_called()

    def test_patrol_sheetUnlockedInFixture_sendNotificationForSheet(self):
        self.prev_spreadsheet_repo.fetch.return_value = Spreadsheet(FixtureManager.load_spreadsheet(Fixture.BEFORE))
        self.spreadsheet_repo.fetch.return_value = Spreadsheet(FixtureManager.load_spreadsheet(Fixture.AFTER))

        self.gull.patrol()

        expected_sheets = list(map(Sheet, FixtureManager.load_recently_unlocked_sheets()))
        self.notifier.send_notification.assert_called_once_with(expected_sheets)

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
