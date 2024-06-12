from collections import namedtuple


from scripts.projectnumber import Projectnumber


class LogRecord():
    """Handles a single row in the logbook."""
    def __init__(self, record:namedtuple) -> None:
        self._name = record.megnevezes[:28]
        self._unitprice = round(float(record.egysegar))
        self._unit = record.egyseg[:4]
        self._change = round(float(record.valtozas))
        self._projectnumber = Projectnumber(record.projektszam)
        self._value = self._unitprice * self._change


    def __str__(self) -> str:
        return "{name:<28} {change:>6} {unit:<4} x {up:>7} = {value:>13} Ft".\
                format(name=self._name,
                       change=self._change,
                       unit=self._unit,
                       up=self._unitprice,
                       value=self._value)

    @property
    def value(self) -> int:
        return self._value

    @property
    def quantity(self) -> int:
        return abs(self._change)

    @property
    def projectnumber(self) -> Projectnumber:
        return self._projectnumber