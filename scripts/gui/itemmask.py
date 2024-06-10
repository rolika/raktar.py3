from tkinter import *
from tkinter import ttk

from itemrecord import ItemRecord


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
        self.grid(padx=PADX, pady=PADY)

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
        is_packaging = self.register(self._is_packaging)
        is_month = self.register(self._is_month)
        Label(self, text="Megnevezés:")\
            .grid(row=0, column=0, sticky=W, padx=PADX, pady=PADY)
        name_entry = ttk.Entry(self, justify=LEFT, textvariable=self.name_var)
        name_entry.grid(row=0, column=1, sticky=E+W, padx=PADX, pady=PADY,
                        columnspan=6)
        name_entry.focus()

        Label(self, text="Gyártó:")\
            .grid(row=1, column=0, sticky=W, padx=PADX, pady=PADY)
        ttk.Entry(self, justify=LEFT, textvariable=self.manufacturer_var)\
            .grid(row=1, column=1, sticky=E+W, padx=PADX, pady=PADY,
                  columnspan=3)
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
        self.packaging_entry = ttk.Entry(self, width=SHORT_FIELD, justify=RIGHT,
                  textvariable=self.packaging_var,
                  validate="all", validatecommand=(is_packaging))
        self.packaging_entry.grid(row=4, column=1, sticky=W, padx=PADX, pady=PADY)
        ttk.Entry(self, width=SHORT_FIELD, justify=LEFT,
                  textvariable=self.unit_var)\
            .grid(row=4, column=2, sticky=E, padx=PADX, pady=PADY)
        Label(self, text="egység")\
            .grid(row=4, column=3, sticky=E, padx=PADX, pady=PADY)
        Label(self, text="Eltartható:")\
            .grid(row=4, column=4, sticky=E, padx=PADX, pady=PADY)
        ttk.Entry(self, width=MID_FIELD, justify=RIGHT,
                  textvariable=self.shelflife_var,
                  validate="all", validatecommand=(is_month))\
            .grid(row=4, column=5, sticky=W, padx=PADX, pady=PADY)
        Label(self, text="hónap")\
            .grid(row=4, column=6, padx=PADX, pady=PADY)
        self.packaging_var.set(DEFAULT_PACKAGING)
        self.shelflife_var.set(DEFAULT_SHELFLIFE)

    def get_mask(self) -> ItemRecord:
        return ItemRecord(
            name=self.name_var.get(),
            nickname=self.nickname_var.get(),
            manufactuere=self.manufacturer_var.get(),
            descriptioin=self.description_var.get(),
            color=self.color_var.get(),
            comment=self.comment_var.get(),
            unit=self.unit_var.get(),
            packaging=self.packaging_var.get(),
            shelflife=self.shelflife_var.get()
        )

    def set_mask(self, item:ItemRecord) -> None:
        self.name_var.set(item.name)
        self.nickname_var.set(item.nickname)
        self.manufacturer_var.set(item.manufacturer)
        self.description_var.set(item.description)
        self.color_var.set(item.color)
        self.comment_var.set(item.comment)
        self.unit_var.set(item.unit)
        self.packaging_var.set(item.packaging)
        self.shelflife_var.set(item.shelflife)

    def disable(self) -> None:
        for child in self.winfo_children():
            if type(child) is ttk.Entry:
                child["state"] = DISABLED

    def enable(self) -> None:
        for child in self.winfo_children():
            if type(child) is ttk.Entry:
                child["state"] = NORMAL
    
    def _is_packaging(self) -> bool:
        style = ttk.Style()
        style.configure("okstyle.TEntry", fieldbackground="white")
        style.configure("errorstyle.TEntry", fieldbackground="red")
        try:
            number = float(self.packaging_var.get())
            if number >= 0:
                self.packaging_entry["style"] = "okstyle.TEntry"
        except ValueError:            
            self.packaging_entry["style"] = "errorstyle.TEntry"
        return True
    
    def _is_month(self) -> bool:
        return True


if __name__ == "__main__":
    mask = ItemMask()
    mask.disable()
    mask.enable()
    mask.mainloop()
