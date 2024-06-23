from tkinter import *
from tkinter import ttk


MID_FIELD = 16
PADX = 3
PADY = 3

ALL_SELECTED = "teljes raktár"


class DisplayMask(LabelFrame):
    def __init__(self):
        super().__init__(text="Számított adatok")
        self._init_controll_variables()
        self._build_interface()

    def _init_controll_variables(self) -> None:
        self.articlenumber_var = StringVar()
        self.selectiontext_var = StringVar()
        self.selectionvalue_var = StringVar()

    def _build_interface(self) -> None:
        Label(self, text="Cikkszám:")\
            .grid(row=0, column=0, sticky=W, padx=PADX, pady=PADY)
        ttk.Entry(self, justify=RIGHT, width=MID_FIELD, state=DISABLED,
                  textvariable=self.articlenumber_var)\
            .grid(row=0, column=1, padx=PADX, pady=PADY)
        Label(self, text="Kiválasztva:")\
            .grid(row=1, column=0, sticky=W, padx=PADX, pady=PADY)
        ttk.Entry(self, justify=RIGHT, width=MID_FIELD, state=DISABLED,
                  textvariable=self.selectiontext_var)\
            .grid(row=1, column=1, padx=PADX, pady=PADY)
        Label(self, text="Érték:")\
            .grid(row=2, column=0, sticky=W, padx=PADX, pady=PADY)
        ttk.Entry(self, justify=RIGHT, width=MID_FIELD, state=DISABLED,
                  textvariable=self.selectionvalue_var)\
            .grid(row=2, column=1, padx=PADX, pady=PADY)
        Label(self, text="Ft")\
            .grid(row=2, column=2, sticky=W, padx=PADX, pady=PADY)
    
    def update_(self, 
                articlenumber:int, 
                selectiontext:str, 
                selectionvalue:float) -> None:
        self.articlenumber_var.set(f"{articlenumber:06}")
        if selectiontext:
            selectiontext = f"""\"{selectiontext}\""""
        else:
            selectiontext = ALL_SELECTED
        self.selectiontext_var.set(selectiontext)
        self.selectionvalue_var.set(f"{round(selectionvalue):n}")