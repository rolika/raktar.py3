from datetime import date
from tkinter import *
from tkinter import ttk

from scripts.itemrecord import ItemRecord
from scripts.stockitemrecord import StockItemRecord


SHORT_FIELD = 8
MID_FIELD = 16
PADX = 3
PADY = 3

style = ttk.Style()
style.configure("okstyle.TEntry", fieldbackground="white")
style.configure("errorstyle.TEntry", fieldbackground="red")


class StockItemMask(LabelFrame):
    def __init__(self):
        super().__init__(text="Raktári jellemzők")
        self._init_controll_variables()
        self._build_interface()
        self.grid(padx=PADX, pady=PADY)

    def _init_controll_variables(self) -> None:
        self.place_var = StringVar()
        self.unitprice_var = StringVar()
        self.unit_var = StringVar()
        self.productiondate_var = StringVar()
        self.stock_var = StringVar()

    def _build_interface(self) -> None:
        is_number = self.register(self._is_number)
        is_date = self.register(self._is_date)

        Label(self, text="Készlet:")\
            .grid(row=0, column=0, sticky=W, padx=PADX, pady=PADY)
        ttk.Entry(self, justify=RIGHT, width=MID_FIELD,
                  textvariable=self.stock_var,
                  validate="all", validatecommand=(is_number, "%P", "%W"))\
            .grid(row=0, column=1, padx=PADX, pady=PADY)
        Label(self, textvariable=self.unit_var)\
            .grid(row=0, column=2, sticky=W, padx=PADX, pady=PADY)
        Label(self, text="Egységár:")\
            .grid(row=0, column=3, sticky=W, padx=PADX, pady=PADY)
        ttk.Entry(self, justify=RIGHT, width=MID_FIELD,
                  textvariable=self.unitprice_var,
                  validate="all", validatecommand=(is_number, "%P", "%W"))\
            .grid(row=0, column=4, padx=PADX, pady=PADY)
        Label(self, text="Ft /")\
            .grid(row=0, column=5, sticky=E, padx=PADX, pady=PADY)
        Label(self, textvariable=self.unit_var)\
            .grid(row=0, column=6, sticky=W, padx=PADX, pady=PADY)

        Label(self, text="Hely/projekt:")\
            .grid(row=1, column=0, sticky=W, padx=PADX, pady=PADY)
        ttk.Entry(self, justify=LEFT, width=MID_FIELD,
                  textvariable=self.place_var)\
            .grid(row=1, column=1, padx=PADX, pady=PADY)
        Label(self, text="Gyártási idő:")\
            .grid(row=1, column=3, sticky=W, padx=PADX, pady=PADY)
        ttk.Entry(self, justify=RIGHT, width=MID_FIELD,
                  textvariable=self.productiondate_var,
                  validate="all", validatecommand=(is_date, "%P", "%W"))\
            .grid(row=1, column=4, padx=PADX, pady=PADY)
        Label(self, text="(éééé-hh-nn)")\
            .grid(row=1, column=5, sticky=W, padx=PADX, pady=PADY,
                  columnspan=2)
        self.unitprice_var.set("0")
        self.stock_var.set("0")
        self.productiondate_var.set(date.today().isoformat())

    def _is_number(self, text:str, name:str) -> bool:
        widget = self.nametowidget(name)
        try:
            number = float(text)
            if number >= 0:
                widget["style"] = "okstyle.TEntry"
        except ValueError:
            widget["style"] = "errorstyle.TEntry"
        return True

    def _is_date(self, text:str, name:str) -> bool:
        widget = self.nametowidget(name)
        try:
            date.fromisoformat(text)
            widget["style"] = "okstyle.TEntry"
        except ValueError:
            widget["style"] = "errorstyle.TEntry"
        return True

    def retrieve(self) -> StockItemRecord:
        return StockItemRecord(
            stock=self.stock_var.get(),
            unitprice=self.unitprice_var.get(),
            place=self.place_var.get(),
            productiondate=self.productiondate_var.get()
        )

    def populate(self, stockitem:StockItemRecord, item:ItemRecord) -> None:
        self.stock_var.set(stockitem.stock)
        self.unitprice_var.set(stockitem.unitprice)
        self.place_var.set(stockitem.place)
        self.productiondate_var.set(stockitem.productiondate)
        self.unit_var.set(item.unit)

    def is_valid(self) -> bool:
        return bool(self.retrieve())