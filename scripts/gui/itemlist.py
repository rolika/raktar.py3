from tkinter import *
from tkinter import ttk


class ItemList(LabelFrame):
    def __init__(self, title="Raktárkészlet") -> None:
        super().__init__(text=title)
        self._init_controll_variables()
        self._build_interface()
    
    def _init_controll_variables(self) -> None:
        self.filter_var = StringVar()
        self.list_var = StringVar()
    
    def _build_interface(self) -> None:
        self.filter_entry = ttk.Entry()
        self.list_box = Listbox()