class Sheet():
    """
    Data structure represents a Sheet.
    """

    @classmethod
    def from_dict(cls, data):
        return Sheet(**data)

    def __init__(self, gsheet):
        """
        :param gsheet: The google sheet dictionary.
        :type gsheet: dict()
        """
        self._gsheet = gsheet

    @property
    def gsheet(self):
        return self._gsheet

    @property
    def id(self):
        return self._gsheet['properties']['sheetId']

    @property
    def title(self):
        return self._gsheet['properties']['title']

    @property
    def protected(self):
        return bool(self._gsheet.get('protectedRanges'))

    def to_dict(self):
        return self.__dict__

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        return type(self) == type(other) and hash(self) == hash(other)

    def __str__(self):
        return "Sheet({}, \"{}\", protected={})".format(
                self.id, self.title, self.protected)

    def __repr__(self):
        return str(self)
