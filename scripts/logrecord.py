import locale
locale.setlocale(locale.LC_ALL, "")

from scripts.record import Record


TRANSLATE_ATTRIBUTES = {
    "azonosito": "primary_key",
    "megnevezes": "name",
    "egysegar": "unitprice",
    "egyseg": "unit",
    "valtozas": "change",
    "datum": "date",
    "projektszam": "projectnumber"
}


class LogRecord(Record):
    """Handles a single record in the logbook."""
    def __init__(self, **kwargs) -> None:
        super().__init__(translate_attributes=TRANSLATE_ATTRIBUTES, **kwargs)

    def __str__(self) -> str:
        return "{:<41} {:>10} {:<7}".format(
                (self.name)[0:41],
                locale.format_string(f="%+.2f", val=self.change, grouping=True),
                self.unit)