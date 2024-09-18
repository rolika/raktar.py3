from tkinter import *
from tkinter import ttk

from scripts.gui import styles
from scripts.itemrecord import ItemRecord


SHORT_FIELD = 8
MID_FIELD = 16
PADX = 3
PADY = 3
DEFAULT_PACKAGING = 0
DEFAULT_SHELFLIFE = 12


class ItemMask(LabelFrame):
    def __init__(self):
        super().__init__(text="Anyag")
        self._init_controll_variables()
        self._build_interface()

    def _init_controll_variables(self) -> None:
        self.name_var = StringVar()
        self.nickname_var = StringVar()
        self.manufacturer_var = StringVar()
        self.description_var = StringVar()
        self.color_var = StringVar()
        self.comment_var = StringVar()
        self.unit_var = StringVar()
        self.packaging_var = StringVar()
        self.shelflife_var = StringVar()

    def _build_interface(self) -> None:
        is_number = self.register(self._is_number)
        is_empty = self.register(self._is_empty)
        Label(self, text="Megnevezés:")\
            .grid(row=0, column=0, sticky=W, padx=PADX, pady=PADY)
        self._name_entry = ttk.Entry(self, justify=LEFT,
                                     textvariable=self.name_var,
                                     name="name", validate="key",
                                     validatecommand=(is_empty, "%P", "%W"))
        self._name_entry.grid(row=0, column=1, sticky=E+W, padx=PADX, pady=PADY,
                              columnspan=6)
        self._name_entry.focus()

        Label(self, text="Gyártó:")\
            .grid(row=1, column=0, sticky=W, padx=PADX, pady=PADY)
        self._manufacturer_entry =\
            ttk.Entry(self, justify=LEFT, textvariable=self.manufacturer_var,
                      name="manufacturer", validate="key",
                      validatecommand=(is_empty, "%P", "%W"))
        self._manufacturer_entry.grid(row=1, column=1, sticky=E+W, padx=PADX,
                                      pady=PADY, columnspan=3)
        Label(self, text="Becenév:")\
            .grid(row=1, column=4, sticky=E, padx=PADX, pady=PADY)
        ttk.Entry(self, justify=LEFT, textvariable=self.nickname_var)\
            .grid(row=1, column=5, sticky=E+W, padx=PADX, pady=PADY,
                  columnspan=2)

        Label(self, text="Leírás:")\
            .grid(row=2, column=0, sticky=W, padx=PADX, pady=PADY)
        ttk.Entry(self, justify=LEFT, textvariable=self.description_var)\
            .grid(row=2, column=1, sticky=E+W, padx=PADX, pady=PADY,
                  columnspan=6)

        Label(self, text="Megjegyzés:")\
            .grid(row=3, column=0, sticky=W, padx=PADX, pady=PADY)
        ttk.Entry(self, justify=LEFT, textvariable=self.comment_var)\
            .grid(row=3, column=1, sticky=E+W, padx=PADX, pady=PADY,
                  columnspan=3)
        Label(self, text="Szín:")\
            .grid(row=3, column=4, sticky=E, padx=PADX, pady=PADY)
        ttk.Entry(self, justify=LEFT, textvariable=self.color_var)\
            .grid(row=3, column=5, sticky=E+W, padx=PADX, pady=PADY,
                  columnspan=2)

        Label(self, text="Kiszerelés:")\
            .grid(row=4, column=0, sticky=W, padx=PADX, pady=PADY)
        ttk.Entry(self, width=SHORT_FIELD, justify=RIGHT,
                  textvariable=self.packaging_var, name="packaging",
                  validate="key", validatecommand=(is_number, "%P", "%W"))\
                    .grid(row=4, column=1, sticky=W, padx=PADX, pady=PADY)
        self._unit_entry =\
            ttk.Entry(self, width=SHORT_FIELD, justify=LEFT,
                      textvariable=self.unit_var, name="unit", validate="all",
                      validatecommand=(is_empty, "%P", "%W"))
        self._unit_entry.grid(row=4, column=2, sticky=E, padx=PADX, pady=PADY)
        Label(self, text="egység")\
            .grid(row=4, column=3, sticky=E, padx=PADX, pady=PADY)
        Label(self, text="Eltartható:")\
            .grid(row=4, column=4, sticky=E, padx=PADX, pady=PADY)
        self._shelflife_entry =\
            ttk.Entry(self, width=MID_FIELD, justify=RIGHT,
                      textvariable=self.shelflife_var, name="shelflife",
                      validate="key", validatecommand=(is_number, "%P", "%W"))
        self._shelflife_entry.grid(row=4, column=5, sticky=W,
                                   padx=PADX, pady=PADY)
        Label(self, text="hónap")\
            .grid(row=4, column=6, padx=PADX, pady=PADY)
        self.packaging_var.set(DEFAULT_PACKAGING)
        self.shelflife_var.set(DEFAULT_SHELFLIFE)

    def retrieve(self) -> ItemRecord:
        return ItemRecord(
            name=self.name_var.get(),
            nickname=self.nickname_var.get(),
            manufacturer=self.manufacturer_var.get(),
            description=self.description_var.get(),
            color=self.color_var.get(),
            comment=self.comment_var.get(),
            unit=self.unit_var.get(),
            packaging=self.packaging_var.get(),
            shelflife=self.shelflife_var.get()
        )

    def populate(self, item:ItemRecord) -> None:
        self.name_var.set(item.name)
        self.nickname_var.set(item.nickname)
        self.manufacturer_var.set(item.manufacturer)
        self.description_var.set(item.description)
        self.color_var.set(item.color)
        self.comment_var.set(item.comment)
        self.unit_var.set(item.unit)
        self.packaging_var.set(item.packaging)
        self.shelflife_var.set(item.shelflife)
        self._name_entry["style"] = "okstyle.TEntry"
        self._manufacturer_entry["style"] = "okstyle.TEntry"
        self._unit_entry["style"] = "okstyle.TEntry"
        self._shelflife_entry["style"] = "okstyle.TEntry"

    def disable(self) -> None:
        for child in self.winfo_children():
            if type(child) is ttk.Entry:
                child["state"] = DISABLED

    def enable(self) -> None:
        for child in self.winfo_children():
            if type(child) is ttk.Entry:
                child["state"] = NORMAL

    def is_valid(self) -> bool:
        return styles.is_entry_ok(self)

    def _is_number(self, text:str, name:str) -> bool:
        try:
            number = float(text)
            if number >= 0:
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


if __name__ == "__main__":
    mask = ItemMask()
    mask.disable()
    mask.enable()
    mask.mainloop()
