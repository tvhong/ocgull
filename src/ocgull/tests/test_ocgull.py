from unittest import TestCase

from mock import Mock

from constants import ProtectionStatus
from fixture import FixtureManager
from notifier import Notifier
from ocgull import OcGull
from spreadsheet import Sheet, Spreadsheet
from spreadsheet.repo import PreviousSpreadsheetRepo, SpreadsheetRepo


class TestOcGull(TestCase):
    def setUp(self):
        self.spreadsheet_repo = Mock(spec=SpreadsheetRepo)
        self.prev_spreadsheet_repo = Mock(spec=PreviousSpreadsheetRepo)
        self.notifier = Mock(spec=Notifier)
        self.gull = OcGull(
            self.spreadsheet_repo,
            self.prev_spreadsheet_repo,
            self.notifier,
        )

    def test_pull_failedFetchingSheets_bubbleError(self):
        self.spreadsheet_repo.fetch.side_effect = ValueError()

        with self.assertRaises(ValueError):
            self.gull.pull()

    def test_pull_lockedSheetCreated_noNotification(self):
        self.prev_spreadsheet_repo.fetch.return_value = self._create_stub_spreadsheet([])
        self.spreadsheet_repo.fetch.return_value = self._create_stub_spreadsheet([
            (1, ProtectionStatus.LOCKED),
        ])

        self.gull.pull()

        self.notifier.send_notification.assert_not_called()

    def test_pull_unprotectedSheetCreated_noNotification(self):
        self.prev_spreadsheet_repo.fetch.return_value = self._create_stub_spreadsheet([])
        self.spreadsheet_repo.fetch.return_value = self._create_stub_spreadsheet([
            (1, ProtectionStatus.UNPROTECTED),
        ])

        self.gull.pull()

        self.notifier.send_notification.assert_not_called()

    def test_pull_unlockedSheetCreated_sendNotificationForSheet(self):
        self.prev_spreadsheet_repo.fetch.return_value = self._create_stub_spreadsheet([])
        self.spreadsheet_repo.fetch.return_value = self._create_stub_spreadsheet([
            (1, ProtectionStatus.UNLOCKED),
        ])

        self.gull.pull()

        self.notifier.send_notification.assert_called_once_with([
            self._create_sheet(1, ProtectionStatus.UNLOCKED),
        ])

    def test_pull_oneSheetUnlocked_sendNotificationForSheet(self):
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

        self.gull.pull()

        self.notifier.send_notification.assert_called_once_with([
            self._create_sheet(2, ProtectionStatus.UNLOCKED),
        ])

    def test_pull_multipleSheetsUnlocked_sendNotificationForSheets(self):
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

        self.gull.pull()

        self.notifier.send_notification.assert_called_once_with([
            self._create_sheet(2, ProtectionStatus.UNLOCKED),
            self._create_sheet(3, ProtectionStatus.UNLOCKED),
        ])

    def test_pull_noSheetsUnlocked_noNotification(self):
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

        self.gull.pull()

        self.notifier.send_notification.assert_not_called()

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
