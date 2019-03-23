from ocgull.spreadsheet.repo.constants import DataSource


class RepoConfig():
    _SPREADSHEET_ID_MAP = {
        DataSource.TEST: '1xevODTsSwCUP7waSZ7dykhpCedyGAHVu4-G-Obl6te4',
        DataSource.PROD: '1TmNjLpt-nI6Mvj80l2JqltdS1A4ecn-d0AT5Zitv-bw',
    }
    _SNAPSHOT_READ = {
        DataSource.TEST: 'dev-snapshot.json',
        DataSource.PROD: 'snapshot.json',
    }
    _SNAPSHOT_WRITE = {
        DataSource.TEST: 'dev-snapshot-saved.json',
        DataSource.PROD: 'snapshot.json',
    }

    def __init__(self, datasource):
        assert(datasource in (DataSource.PROD, DataSource.TEST))

        self.datasource = datasource

    def get_gspreadsheet_id(self):
        return self._SPREADSHEET_ID_MAP[self.datasource]

    def get_snapshot_read_filename(self):
        return self._SNAPSHOT_READ[self.datasource]

    def get_snapshot_write_filename(self):
        return self._SNAPSHOT_WRITE[self.datasource]

    def __eq__(self, other):
        return type(self) == type(other) and self.datasource == other.datasource

    def __hash__(self):
        return hash(self.datasource)
