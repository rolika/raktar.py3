from tkinter import *
from tkinter import ttk

from itemrecord import ItemRecord


SHORT_FIELD = 8
PADX = 3
PADY = 3
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
        self.packaging_var = DoubleVar()
        self.shelflife_var = IntVar()

    def _build_interface(self) -> None:
        Label(self, text="Megnevezés:", anchor=W)\
            .grid(row=0, column=0, sticky=W, padx=PADX, pady=PADY)
        name_entry = ttk.Entry(self, justify=LEFT, textvariable=self.name_var)
        name_entry.grid(row=0, column=1, sticky=E+W, padx=PADX, pady=PADY,
                        columnspan=6)
        name_entry.focus()

        Label(self, text="Gyártó:", anchor=W)\
            .grid(row=1, column=0, sticky=W, padx=PADX, pady=PADY)
        ttk.Entry(self, justify=LEFT, textvariable=self.manufacturer_var)\
            .grid(row=1, column=1, sticky=E+W, padx=PADX, pady=PADY,
                  columnspan=3)
        Label(self, text="Becenév:", anchor=E)\
            .grid(row=1, column=4, sticky=E, padx=PADX, pady=PADY)
        ttk.Entry(self, justify=LEFT, textvariable=self.nickname_var)\
            .grid(row=1, column=5, sticky=E+W, padx=PADX, pady=PADY,
                  columnspan=2)

        Label(self, text="Leírás:", anchor=W)\
            .grid(row=2, column=0, sticky=W, padx=PADX, pady=PADY)
        ttk.Entry(self, justify=LEFT, textvariable=self.description_var)\
            .grid(row=2, column=1, sticky=E+W, padx=PADX, pady=PADY,
                  columnspan=6)

        Label(self, text="Megjegyzés:", anchor=W)\
            .grid(row=3, column=0, sticky=W, padx=PADX, pady=PADY)
        ttk.Entry(self, justify=LEFT, textvariable=self.comment_var)\
            .grid(row=3, column=1, sticky=E+W, padx=PADX, pady=PADY,
                  columnspan=3)
        Label(self, text="Szín:", anchor=E)\
            .grid(row=3, column=4, sticky=E, padx=PADX, pady=PADY)
        ttk.Entry(self, justify=LEFT, textvariable=self.color_var)\
            .grid(row=3, column=5, sticky=E+W, padx=PADX, pady=PADY,
                  columnspan=2)

        Label(self, text="Kiszerelés:", anchor=W)\
            .grid(row=4, column=0, sticky=W, padx=PADX, pady=PADY)
        ttk.Entry(self, width=SHORT_FIELD, justify=RIGHT,
                  textvariable=self.packaging_var)\
            .grid(row=4, column=1, sticky=W, padx=PADX, pady=PADY)
        ttk.Entry(self, width=SHORT_FIELD, justify=LEFT,
                  textvariable=self.unit_var)\
            .grid(row=4, column=2, sticky=E, padx=PADX, pady=PADY)
        Label(self, text="egység", anchor=E)\
            .grid(row=4, column=3, sticky=E, padx=PADX, pady=PADY)
        Label(self, text="Eltartható:", anchor=E)\
            .grid(row=4, column=4, sticky=E, padx=PADX, pady=PADY)
        ttk.Entry(self, width=SHORT_FIELD, justify=RIGHT,
                  textvariable=self.shelflife_var)\
            .grid(row=4, column=5, sticky=W, padx=PADX, pady=PADY)
        Label(self, text="hónap", anchor=W)\
            .grid(row=4, column=6, sticky=W, padx=PADX, pady=PADY)
        self.shelflife_var.set(DEFAULT_SHELFLIFE)

    def _get_controll_variables(self) -> list[StringVar|DoubleVar]:
        return [getattr(self, attr) for attr in dir(self)\
                if attr.endswith("_var")]
    
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

    def set_mask(self, item:ItemRecord):
        self.name_var.set(item.name)
        self.nickname_var.set(item.nickname)
        self.manufacturer_var.set(item.manufacturer)
        self.description_var.set(item.description)
        self.color_var.set(item.color)
        self.comment_var.set(item.comment)
        self.unit_var.set(item.unit)
        self.packaging_var.set(item.packaging)
        self.shelflife_var.set(item.shelflife)


if __name__ == "__main__":
    ItemMask().mainloop()