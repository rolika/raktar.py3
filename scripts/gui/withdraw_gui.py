import os
from tkinter import *
from tkinter import ttk
from tkinter import simpledialog

from scripts.gui.itemlistbox import ItemListbox


PADX = 2
PADY = 2


class WithdrawGui(simpledialog.Dialog):
    def __init__(self, root=None, title="Kivét raktárból") -> None:
        super().__init__(root, title)
    
    def body(self, root) -> None:
        """Create dialog body. Return widget that should have initial focus."""
        body = Frame(self)
        self.__itemlistbox = ItemListbox(body)
        self.__withdraw_listbox = ItemListbox(body, title="Szállítólevél")
        self.__itemlistbox.pack(side=LEFT, padx=PADX, pady=PADY)
        self.__withdraw_listbox.pack(padx=PADX, pady=PADY)
        body.pack()
        return self.__itemlistbox.lookup_entry

    def buttonbox(self):
        """Override standard button texts."""
        box = Frame(self)
        w = ttk.Button(box, text="KÉSZ", width=10, command=self.ok,
                       default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = ttk.Button(box, text="Mégse", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        box.pack()