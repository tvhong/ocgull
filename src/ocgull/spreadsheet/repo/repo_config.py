from ocgull.spreadsheet.repo.constants import DataSource


class RepoConfig():
    _SPREADSHEET_ID_MAP = {
        DataSource.DEV: '1xevODTsSwCUP7waSZ7dykhpCedyGAHVu4-G-Obl6te4',
        DataSource.PROD: '1TmNjLpt-nI6Mvj80l2JqltdS1A4ecn-d0AT5Zitv-bw',
    }
    _SNAPSHOT_READ = {
        DataSource.DEV: 'dev-snapshot.json',
        DataSource.PROD: 'snapshot.json',
    }
    _SNAPSHOT_WRITE = {
        DataSource.DEV: 'dev-snapshot-saved.json',
        DataSource.PROD: 'snapshot.json',
    }

    def __init__(self, env):
        assert(env in (DataSource.PROD, DataSource.DEV))

        self.env = env

    def get_gspreadsheet_id(self):
        return self._SPREADSHEET_ID_MAP[self.env]

    def get_snapshot_read_filename(self):
        return self._SNAPSHOT_READ[self.env]

    def get_snapshot_write_filename(self):
        return self._SNAPSHOT_WRITE[self.env]
