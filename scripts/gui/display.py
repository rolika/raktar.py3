from tkinter import *


PADX = 3
PADY = 3


class Display(LabelFrame):
    def __init__(self):
        super().__init__(text="Számított adatok")
        self._init_controll_variables()
        self._build_interface()
        self.grid(padx=PADX, pady=PADY)
    
    def _init_controll_variables(self) -> None:
        pass

    def _build_interface(self) -> None:
        pass

    def update_(self) -> None:
        pass