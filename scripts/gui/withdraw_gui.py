import os
from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
from typing import List

from scripts.gui.itemlistbox import ItemListbox
# from scripts.guidbasemediator import GuiDbaseMediator


PADX = 2
PADY = 2


class WithdrawGui(simpledialog.Dialog):
    def __init__(self, root=None, title="Kivét raktárból",
                 mediator=None) -> None:
        self.__mediator = mediator
        super().__init__(root, title)
    
    def _populate(func:callable) -> callable:
        """Decorator for populating the itemlistbox."""
        def wrapper(self, root):
            func(self, root)
            self.__mediator.add_gui(self)
            self.__mediator.populate()
            return self.__itemlistbox.lookup_entry  # setting the focus
        return wrapper
    
    @_populate
    def body(self, root:Widget) -> None:
        """Create dialog body. Return widget that should have initial focus."""
        box = Frame(self)
        self.__itemlistbox = ItemListbox(box)
        self.__withdraw_listbox = ItemListbox(box, title="Szállítólevél")
        self.__itemlistbox.pack(side=LEFT, padx=PADX, pady=PADY)
        self.__withdraw_listbox.pack(padx=PADX, pady=PADY)
        box.pack()

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
    
    @property
    def itemlistbox(self) -> ItemListbox:
        return self.__itemlistbox