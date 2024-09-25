import locale
locale.setlocale(locale.LC_ALL, "")

from datetime import date
from tkinter import *
from tkinter import ttk

from scripts.gui import styles
from scripts.stockitemrecord import StockItemRecord


SHORT_FIELD = 9
MID_FIELD = 16
PADX = 3
PADY = 3


class StockItemForm(LabelFrame):
    def __init__(self):
        super().__init__(text="Raktári tétel")
        self._init_controll_variables()
        self._build_interface()

    def _init_controll_variables(self) -> None:
        self.__name_var = StringVar()
        self.__nickname_var = StringVar()
        self.__manufacturer_var = StringVar()
        self.__description_var = StringVar()
        self.__color_var = StringVar()
        self.__comment_var = StringVar()
        self.__unit_var = StringVar()
        self.__packaging_var = StringVar()
        self.__shelflife_var = StringVar()
        self.__place_var = StringVar()
        self.__unitprice_var = StringVar()
        self.__productiondate_var = StringVar()
        self.__stock_var = StringVar()

    def _build_interface(self) -> None:
        is_number = self.register(self._is_number)
        is_date = self.register(self._is_date)
        is_empty = self.register(self._is_empty)

        Label(self, text="Megnevezés:")\
            .grid(row=0, column=0, sticky=W, padx=PADX, pady=PADY)
        self.__name_entry =\
            ttk.Entry(self, justify=LEFT, textvariable=self.__name_var,
                      name="name", validate="all",
                      validatecommand=(is_empty, "%P", "%W"))
        self.__name_entry.grid(row=0, column=1, sticky=E+W, padx=PADX,
                               pady=PADY, columnspan=7)

        Label(self, text="Gyártó:")\
            .grid(row=1, column=0, sticky=W, padx=PADX, pady=PADY)
        self.__manufacturer_entry =\
            ttk.Entry(self, justify=LEFT, textvariable=self.__manufacturer_var,
                      name="manufacturer", validate="all",
                      validatecommand=(is_empty, "%P", "%W"))
        self.__manufacturer_entry.grid(row=1, column=1, sticky=E+W, padx=PADX,
                                      pady=PADY, columnspan=3)
        Label(self, text="Becenév:")\
            .grid(row=1, column=4, sticky=E, padx=PADX, pady=PADY)
        ttk.Entry(self, justify=LEFT, textvariable=self.__nickname_var)\
            .grid(row=1, column=5, sticky=E+W, padx=PADX, pady=PADY,
                  columnspan=3)

        Label(self, text="Leírás:")\
            .grid(row=2, column=0, sticky=W, padx=PADX, pady=PADY)
        ttk.Entry(self, justify=LEFT, textvariable=self.__description_var)\
            .grid(row=2, column=1, sticky=E+W, padx=PADX, pady=PADY,
                  columnspan=7)

        Label(self, text="Megjegyzés:")\
            .grid(row=3, column=0, sticky=W, padx=PADX, pady=PADY)
        ttk.Entry(self, justify=LEFT, textvariable=self.__comment_var)\
            .grid(row=3, column=1, sticky=E+W, padx=PADX, pady=PADY,
                  columnspan=3)
        Label(self, text="Szín:")\
            .grid(row=3, column=4, sticky=E, padx=PADX, pady=PADY)
        ttk.Entry(self, justify=LEFT, textvariable=self.__color_var)\
            .grid(row=3, column=5, sticky=E+W, padx=PADX, pady=PADY,
                  columnspan=3)

        Label(self, text="Kiszerelés:")\
            .grid(row=4, column=0, sticky=W, padx=PADX, pady=PADY)
        ttk.Entry(self, width=SHORT_FIELD, justify=RIGHT,
                  textvariable=self.__packaging_var, name="packaging",
                  validate="all", validatecommand=(is_number, "%P", "%W"))\
                    .grid(row=4, column=1, sticky=W, padx=PADX, pady=PADY)
        self.__unit_entry =\
            ttk.Entry(self, width=SHORT_FIELD, justify=LEFT,
                      textvariable=self.__unit_var, name="unit", validate="all",
                      validatecommand=(is_empty, "%P", "%W"))
        self.__unit_entry.grid(row=4, column=2, sticky=E, padx=PADX, pady=PADY)
        Label(self, text="egység", anchor=W)\
            .grid(row=4, column=3, sticky=E+W, padx=PADX, pady=PADY)
        Label(self, text="Eltartható:")\
            .grid(row=4, column=4, sticky=E, padx=PADX, pady=PADY)
        self.__shelflife_entry =\
            ttk.Entry(self, width=SHORT_FIELD, justify=RIGHT,
                      textvariable=self.__shelflife_var, name="shelflife",
                      validate="all", validatecommand=(is_number, "%P", "%W"))
        self.__shelflife_entry.grid(row=4, column=5, sticky=W,
                                   padx=PADX, pady=PADY)
        Label(self, text="hónap", anchor=W)\
            .grid(row=4, column=6, padx=PADX, pady=PADY, sticky=E+W,
                  columnspan=2)

        Label(self, text="Készlet:")\
            .grid(row=5, column=0, sticky=W, padx=PADX, pady=PADY)
        self.__stock_entry =\
            ttk.Entry(self, justify=RIGHT, width=MID_FIELD,
                      textvariable=self.__stock_var, validate="all",
                      validatecommand=(is_number, "%P", "%W"))
        self.__stock_entry.grid(row=5, column=1, padx=PADX, pady=PADY,
                                columnspan=2, sticky=E+W)
        Label(self, textvariable=self.__unit_var, width=7, anchor=W)\
            .grid(row=5, column=3, sticky=E+W, padx=PADX, pady=PADY)
        Label(self, text="Egységár:")\
            .grid(row=5, column=4, sticky=W, padx=PADX, pady=PADY)
        self.__unitprice_entry =\
            ttk.Entry(self, justify=RIGHT, width=SHORT_FIELD,
                      textvariable=self.__unitprice_var, validate="all",
                      validatecommand=(is_number, "%P", "%W"))
        self.__unitprice_entry.grid(row=5, column=5, padx=PADX, pady=PADY)
        Label(self, text="Ft  /", anchor=W)\
            .grid(row=5, column=6, sticky=E+W, padx=PADX, pady=PADY)
        Label(self, textvariable=self.__unit_var, width=7, anchor=W)\
            .grid(row=5, column=7, sticky=E+W, padx=PADX, pady=PADY)

        Label(self, text="Hely/projekt:")\
            .grid(row=6, column=0, sticky=W, padx=PADX, pady=PADY)
        ttk.Entry(self, justify=LEFT, width=MID_FIELD,
                  textvariable=self.__place_var)\
            .grid(row=6, column=1, padx=PADX, pady=PADY, columnspan=2,
                  sticky=E+W)
        Label(self, text="Gyártási idő:")\
            .grid(row=6, column=4, sticky=W, padx=PADX, pady=PADY)
        self.__productiondate_entry =\
            ttk.Entry(self, justify=RIGHT, width=SHORT_FIELD,
                      textvariable=self.__productiondate_var, validate="all",
                      validatecommand=(is_date, "%P", "%W"))
        self.__productiondate_entry.grid(row=6, column=5, padx=PADX, pady=PADY)
        Label(self, text="(éééé-hh-nn)", anchor=W)\
            .grid(row=6, column=6, sticky=E+W, padx=PADX, pady=PADY,
                  columnspan=2)

        self.__packaging_var.set("0")
        self.__shelflife_var.set("12")
        self.__unitprice_var.set("0")
        self.__stock_var.set("0")
        self.__productiondate_var.set(date.today().isoformat())

    def _is_number(self, text:str, name:str) -> bool:
        try:
            number = locale.atof(text)
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

    def _is_empty(self, text:str, name:str) -> bool:
        if text:
            styles.apply_entry_ok(self, name)
        else:
            styles.apply_entry_error(self, name)
        return True

    def retrieve(self) -> StockItemRecord:
        return StockItemRecord(
            name=self.__name_var.get(),
            nickname=self.__nickname_var.get(),
            manufacturer=self.__manufacturer_var.get(),
            description=self.__description_var.get(),
            color=self.__color_var.get(),
            comment=self.__comment_var.get(),
            unit=self.__unit_var.get(),
            packaging=self.__packaging_var.get(),
            shelflife=self.__shelflife_var.get(),
            stock=locale.atof(self.__stock_var.get()),
            unitprice=locale.atof(self.__unitprice_var.get()),
            place=self.__place_var.get(),
            productiondate=self.__productiondate_var.get()
        )

    def populate(self, stockitem:StockItemRecord) -> None:
        self.__name_var.set(stockitem.name)
        self.__nickname_var.set(stockitem.nickname)
        self.__manufacturer_var.set(stockitem.manufacturer)
        self.__description_var.set(stockitem.description)
        self.__color_var.set(stockitem.color)
        self.__comment_var.set(stockitem.comment)
        self.__unit_var.set(stockitem.unit)
        packaging = locale.format_string(f="%.2f", val=stockitem.packaging,
                                         grouping=True)
        self.__packaging_var.set(packaging)
        self.__shelflife_var.set(stockitem.shelflife)
        stock = locale.format_string(f="%.2f", val=stockitem.stock,
                                     grouping=True)
        self.__stock_var.set(stock)
        unitprice = locale.format_string(f="%.2f", val=stockitem.unitprice,
                                         grouping=True)
        self.__unitprice_var.set(unitprice)
        self.__place_var.set(stockitem.place)
        self.__productiondate_var.set(stockitem.productiondate)
        self.__name_entry["style"] = "okstyle.TEntry"
        self.__manufacturer_entry["style"] = "okstyle.TEntry"
        self.__unit_entry["style"] = "okstyle.TEntry"
        self.__shelflife_entry["style"] = "okstyle.TEntry"
        self.__stock_entry["style"] = "okstlye.TEntry"
        self.__unitprice_entry["style"] = "okstlye.TEntry"
        self.__productiondate_entry["style"] = "okstlye.TEntry"

    def is_valid(self) -> bool:
        return styles.is_entry_ok(self)