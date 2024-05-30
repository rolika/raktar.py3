"""Various helper functions."""


import re


PROJECTNUMBER_PATTERN = r"(?P<ev>\d{2})[/ _-](?P<szam>\d{1,3})"


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
    and add leading zeroes to the serial."""
    mo = valid_projectnr(text)
    return "{}_{:0>3s}".format(mo["ev"], mo["szam"])