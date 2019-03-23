from ocgull.constants import ProtectionStatus


class Sheet():
    """
    Data structure represents a Sheet.
    """

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
    def protection(self):
        try:
            protected_ranges = self._gsheet['protectedRanges']
            if any('unprotectedRanges' in r for r in protected_ranges):
                return ProtectionStatus.UNLOCKED
            else:
                return ProtectionStatus.LOCKED
        except KeyError:
            return ProtectionStatus.UNPROTECTED

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        return type(self) == type(other) and hash(self) == hash(other)

    def __str__(self):
        return "Sheet({}, \"{}\", protection={})".format(
                self.id, self.title, self.protection)

    def __repr__(self):
        return str(self)
