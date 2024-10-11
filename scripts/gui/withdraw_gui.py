import os
from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox

from scripts.databasesession import DatabaseSession
from scripts.gui.itemlistbox import ItemListbox
from scripts.projectnumber import Projectnumber


PADX = 2
PADY = 2


class WithdrawGui(simpledialog.Dialog):
    def __init__(self, root=None, title="Kivét raktárból",
                 dbsession=DatabaseSession) -> None:
        self.__dbsession = dbsession
        self.__projectnumber = self._get_projectnumber()
        if not self.__projectnumber:
            return
        super().__init__(root, title)
    
    def body(self, root:Widget) -> None:
        """Create dialog body. Return widget that should have initial focus."""
        box = Frame(self)
        self.__itemlistbox = ItemListbox(box)
        self.__withdraw_listbox = ItemListbox(box, title="Szállítólevél")
        self.__itemlistbox.pack(side=LEFT, padx=PADX, pady=PADY)
        self.__withdraw_listbox.pack(padx=PADX, pady=PADY)
        self.__itemlistbox.populate(self.__dbsession.load_all_items())
        self.__itemlistbox.select_index(0)
        box.pack()
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
    
    def _get_projectnumber(self) -> Projectnumber:
        while True:
            projectnumber =\
                simpledialog.askstring(title="Új szállítólevél",
                                       prompt="Kérlek add meg a projektszámot:")
            if not projectnumber:
                return None
            projectnumber = Projectnumber(projectnumber)
            if projectnumber:
                return projectnumber
            else:
                messagebox.showwarning(title="Vigyázz!",
                                       message="Hibás projektszám!")