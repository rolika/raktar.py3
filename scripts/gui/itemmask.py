from tkinter import *
from tkinter import ttk


LONG_FIELD = 42
MID_FIELD = 16
SHORT_FIELD = 8
TINY_FIELD = 3
BUTTON_WIDTH = 8
PADX = 3
PADY = 3


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
        self.place_var = StringVar()
        self.unit_var = StringVar()
        self.unitprice_var = DoubleVar()
        self.packaging_var = DoubleVar()
        self.productiondate_var = StringVar()
        self.shelflife_var = IntVar()

    def _build_interface(self) -> None:
        Label(self, text="Megnevezés:", anchor=W)\
            .grid(row=0, column=0, sticky=W, padx=PADX, pady=PADY)
        ttk.Entry(self, justify=LEFT, textvariable=self.name_var)\
            .grid(row=0, column=1, sticky=E+W, padx=PADX, pady=PADY,
                  columnspan=7)

        Label(self, text="Gyártó:", anchor=W)\
            .grid(row=1, column=0, sticky=W, padx=PADX, pady=PADY)
        ttk.Entry(self, justify=LEFT, textvariable=self.manufacturer_var)\
            .grid(row=1, column=1, sticky=E+W, padx=PADX, pady=PADY,
                  columnspan=4)
        Label(self, text="Becenév:", anchor=E)\
            .grid(row=1, column=5, sticky=E, padx=PADX, pady=PADY)
        ttk.Entry(self, justify=LEFT, textvariable=self.nickname_var)\
            .grid(row=1, column=6, sticky=E+W, padx=PADX, pady=PADY, 
                  columnspan=2)

        Label(self, text="Leírás:", anchor=W)\
            .grid(row=2, column=0, sticky=W, padx=PADX, pady=PADY)
        ttk.Entry(self, justify=LEFT, textvariable=self.description_var)\
            .grid(row=2, column=1, sticky=E+W, padx=PADX, pady=PADY,
                  columnspan=7)

        Label(self, text="Megjegyzés:", anchor=W)\
            .grid(row=3, column=0, sticky=W, padx=PADX, pady=PADY)
        ttk.Entry(self, justify=LEFT, textvariable=self.comment_var)\
            .grid(row=3, column=1, sticky=E+W, padx=PADX, pady=PADY, 
                  columnspan=4)
        Label(self, text="Szín:", anchor=E)\
            .grid(row=3, column=5, sticky=E, padx=PADX, pady=PADY)
        ttk.Entry(self, justify=LEFT, textvariable=self.color_var)\
            .grid(row=3, column=6, sticky=E+W, padx=PADX, pady=PADY, 
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


if __name__ == "__main__":
    ItemMask().mainloop()