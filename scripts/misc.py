"""Various helper functions."""


import re


def projectnr_from(projectnr:str) -> str:
    """Convert back the original project number."""
    year, number = projectnr.split("_")
    return "{}/{}".format(year, int(number))


def valid_projectnr(projektszam:str) -> re.match:
    """A projektszám éé/s vagy éé/ss vagy éé/sss alakban elfogadható."""
    pattern = r"(?P<ev>\d{2})\/(?P<szam>\d{1,3})"
    projektszam_regex = re.compile(pattern)
    return projektszam_regex.fullmatch(projektszam)


def fmt_projectnr(projektszam:str) -> str:
    """Az éé/s vagy éé/ss vagy éé/sss alakban érkező projektszámot éé_sss
    alakra formázza, ahol az sss-ben vezető nullákkal tölti ki a szám előtti
    helyet. Ide már valid projektszám érkezik."""
    mo = valid_projectnr(projektszam)
    return "{}_{:0>3s}".format(mo["ev"], mo["szam"])