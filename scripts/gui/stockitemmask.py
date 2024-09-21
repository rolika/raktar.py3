from datetime import date
import locale
from tkinter import *
from tkinter import ttk

from scripts.gui import styles
from scripts.itemrecord import ItemRecord
from scripts.stockitemrecord import StockItemRecord


SHORT_FIELD = 8
MID_FIELD = 16
PADX = 3
PADY = 3


class StockItemMask(LabelFrame):
    def __init__(self):
        super().__init__(text="Raktári jellemzők")
        self._init_controll_variables()
        self._build_interface()

    def _init_controll_variables(self) -> None:
        self.__place_var = StringVar()
        self.__unitprice_var = StringVar()
        self.__unit_var = StringVar()
        self.__productiondate_var = StringVar()
        self.__stock_var = StringVar()
        self.__value_var = StringVar()

    def _build_interface(self) -> None:
        is_number = self.register(self._is_number)
        is_date = self.register(self._is_date)

        Label(self, text="Készlet:")\
            .grid(row=0, column=0, sticky=W, padx=PADX, pady=PADY)
        self.__stock_entry =\
            ttk.Entry(self, justify=RIGHT, width=MID_FIELD,
                      textvariable=self.__stock_var, validate="all",
                      validatecommand=(is_number, "%P", "%W"))
        self.__stock_entry.grid(row=0, column=1, padx=PADX, pady=PADY)
        Label(self, textvariable=self.__unit_var)\
            .grid(row=0, column=2, sticky=W, padx=PADX, pady=PADY)
        Label(self, text="Egységár:")\
            .grid(row=0, column=3, sticky=W, padx=PADX, pady=PADY)
        self.__unitprice_entry =\
            ttk.Entry(self, justify=RIGHT, width=MID_FIELD,
                      textvariable=self.__unitprice_var, validate="all",
                      validatecommand=(is_number, "%P", "%W"))
        self.__unitprice_entry.grid(row=0, column=4, padx=PADX, pady=PADY)
        Label(self, text="Ft /")\
            .grid(row=0, column=5, sticky=E, padx=PADX, pady=PADY)
        Label(self, textvariable=self.__unit_var)\
            .grid(row=0, column=6, sticky=W, padx=PADX, pady=PADY)

        Label(self, text="Hely/projekt:")\
            .grid(row=1, column=0, sticky=W, padx=PADX, pady=PADY)
        ttk.Entry(self, justify=LEFT, width=MID_FIELD,
                  textvariable=self.__place_var)\
            .grid(row=1, column=1, padx=PADX, pady=PADY)
        Label(self, text="Gyártási idő:")\
            .grid(row=1, column=3, sticky=W, padx=PADX, pady=PADY)
        self.__productiondate_entry =\
            ttk.Entry(self, justify=RIGHT, width=MID_FIELD,
                      textvariable=self.__productiondate_var, validate="all",
                      validatecommand=(is_date, "%P", "%W"))
        self.__productiondate_entry.grid(row=1, column=4, padx=PADX, pady=PADY)
        Label(self, text="(éééé-hh-nn)")\
            .grid(row=1, column=5, sticky=W, padx=PADX, pady=PADY,
                  columnspan=2)

        Label(self, text="Érték:")\
            .grid(row=2, column=0, sticky=W, padx=PADX, pady=PADY)
        Label(self, textvariable=self.__value_var)\
            .grid(row=2, column=1, sticky=E, padx=PADX, pady=PADY)

        self.__unitprice_var.set("0")
        self.__stock_var.set("0")
        self.__value_var.set("0")
        self.__productiondate_var.set(date.today().isoformat())

    def _is_number(self, text:str, name:str) -> bool:
        try:
            number = float(text)
            if number >= 0:
                styles.apply_entry_ok(self, name)
        except ValueError:
            styles.apply_entry_error(self, name)
        return True

    def _is_date(self, text:str, name:str) -> bool:
        try:
            date.fromisoformat(text)
            styles.apply_entry_ok(self, name)
        except ValueError:
            styles.apply_entry_error(self, name)
        return True

    def retrieve(self) -> StockItemRecord:
        return StockItemRecord(
            stock=self.__stock_var.get(),
            unitprice=self.__unitprice_var.get(),
            place=self.__place_var.get(),
            productiondate=self.__productiondate_var.get()
        )

    def populate(self, stockitem:StockItemRecord, item:ItemRecord) -> None:
        self.__stock_var.set(stockitem.stock)
        self.__unitprice_var.set(stockitem.unitprice)
        self.__place_var.set(stockitem.place)
        self.__productiondate_var.set(stockitem.productiondate)
        self.__stock_entry["style"] = "okstlye.TEntry"
        self.__unitprice_entry["style"] = "okstlye.TEntry"
        self.__productiondate_entry["style"] = "okstlye.TEntry"

    def is_valid(self) -> bool:
        return styles.is_entry_ok(self)

    @property
    def unit(self) -> str:
        return self.__unit_var.get()

    @unit.setter
    def unit(self, value:str) -> None:
        self.__unit_var.set(value)

    @property
    def value(self) -> str:
        return self.__value_var.get()

    @value.setter
    def value(self, value_:float) -> None:
        self.__value_var.set(f"{locale.currency(val=value_, grouping=True)}")