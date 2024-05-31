"""Various helper classes and functions."""


import re


PROJECTNUMBER_PATTERN = r"(?P<year>\d{2})[/ _-](?P<serial>\d{1,3})"


class Projectnumber():
    """ Class for handling projectnumbers.
    A "legal" projectnumber looks like year/serial, where year is
    represented with two digits, and serial with one to three digits.
    Example: 24/1, 24/12, 24/123. In our case there are no more than 500
    projects in a year, so three digits leave place for growing.
    The 0 serial isn't allowed, but it can be used to bypass things.
    In practice, the projectnumber can be anything, two and one to three digits
    separated by a slash, underscore, space or hyphen.
    For a filename we use the format year_serial, where year is two digits,
    serial is always three digits with leading zeroes. This is also beneficial
    for ordering."""
    def __init__(self, text:str) -> None:
        """At initialization we try tor extract a valid projectnumber."""
        self.year = None
        self.serial = None
        regex = re.compile(PROJECTNUMBER_PATTERN)
        extract = regex.fullmatch(text)
        if extract:
            self.year = extract["year"]
            self.serial = extract["serial"]
    
    def __bool__(self) -> bool:
        """Return true if this is a valid projectnumber."""
        return bool(self.year) and bool(self.serial)
    
    def __str__(self) -> str:
        """Projectnumber as a string is the filename-format."""
        assert bool(self)
        return "{}_{:0>3s}".format(self.year, self.serial)
    
    def __repr__(self) -> str:
        """This is the human readable legal form."""
        assert bool(self)
        return "{}/{}".format(self.year, self.serial)
    
    def __eq__(self, other:object) -> bool:
        """Two projectnumbers are equal if both year and serial are equal."""
        return (self.year == other.year) and (self.serial == other.serial)



def valid_projectnr(text:str) -> re.match:
    """ Test input fora valid projectnumber.
    A valid projectnumber looks like 24/123, ie. a year with two digits, a
    separator and the projects serial number between 1-999.
    The 0 serial isn't allowed, but it's used to bypass things.
    In practice, the separator can be a slash, underscore, space or hyphen."""
    projectnumber_regex = re.compile(PROJECTNUMBER_PATTERN)
    return projectnumber_regex.fullmatch(text)


def projectnr_from(text:str) -> str:
    """Convert back the 24_123 project number to the format of 24/123."""
    year, number = text.split("_")
    return "{}/{}".format(year, int(number))


def fmt_projectnr(text:str) -> str:
    """Convert a 24/1 or 24/12 or 24/123 projectnumber to a separator of _,
    and add leading zeroes to the serial: yy_sss."""
    mo = valid_projectnr(text)
    return "{}_{:0>3s}".format(mo["year"], mo["serial"])