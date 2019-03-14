class Sheet():
    """
    Data structure represents a Sheet.
    """

    def __init__(self, gsheet):
        """
        :param gsheet: The google sheet dictionary.
        :type gsheet: dict()
        """
        self.gsheet = gsheet

    @classmethod
    def from_dict(cls, data):
        return Sheet(**data)

    @property
    def id(self):
        return self.gsheet['properties']['sheetId']

    @property
    def title(self):
        return self.gsheet['properties']['title']

    @property
    def protected(self):
        return bool(self.gsheet.get('protectedRanges'))

    def to_dict(self):
        return self.__dict__

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return "Sheet({}, \"{}\", protected={})".format(
                self.id, self.title, self.protected)

    def __repr__(self):
        return str(self)
