import locale
locale.setlocale(locale.LC_ALL, "")

from datetime import date


TRANSLATE_ATTRIBUTES = {
    "cikkszam": "articlenumber",
    "keszlet": "stock",
    "megnevezes": "name",
    "becenev": "nickname",
    "gyarto": "manufacturer",
    "leiras": "description",
    "megjegyzes": "comment",
    "egyseg": "unit",
    "egysegar": "unitprice",
    "kiszereles": "packaging",
    "hely": "place",
    "lejarat": "shelflife",
    "gyartasido": "productiondate",
    "szin": "color",
    "jeloles": "notation",
    "letrehozas": "created",
    "utolso_modositas": "modified"
}


class StockItemRecord():
    """Handles a single item in the stock."""

    def __init__(self, **kwargs) -> None:
        for arg, value in kwargs.items():
            setattr(self, TRANSLATE_ATTRIBUTES.get(arg, arg), value)

    def __str__(self) -> str:
        space = " " if self.manufacturer else ""
        return "{:<41} {:>10} {:<7}".format(
                (self.manufacturer + space + self.name)[0:41],
                locale.format_string(f="%.2f", val=self.stock, grouping=True),
                self.unit)

    def __bool__(self) -> bool:
        try:
            bool(self.name) and\
            bool(self.unit) #and\
            #bool(self.manufacturer)
            stock = float(self.stock)
            unitprice = float(self.unitprice)
            #date.fromisoformat(self.productiondate)
            return (stock >= 0) and (unitprice >= 0)
        except (AttributeError, ValueError):
            return False

    @property
    def value(self) -> float:
        return float(self.stock) * float(self.unitprice) if bool(self) else 0

    def contains(self, term:str) -> bool:
        for attribute in TRANSLATE_ATTRIBUTES.values():
            if term in str(getattr(self, attribute, None)).lower():
                return True
        return False