from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
from typing import List

from scripts.gui.asklocalfloat import ask_localfloat
from scripts.gui.itemlistbox import ItemListbox
from scripts.projectnumber import Projectnumber
from scripts.stockitemrecord import StockItemRecord


PADX = 2
PADY = 2


class WithdrawDialog(simpledialog.Dialog):
    def __init__(self, root:Widget, master_list:List[StockItemRecord],
                 projectnumber:Projectnumber) -> None:
        self.__master_list = master_list
        self.__withdrawed_items = []
        self.__temp_withdraw = []
        super().__init__(root,
                         title=f"{projectnumber.legal}: Kivét raktárból")

    def body(self, root:Widget) -> None:
        """Create dialog body. Return widget that should have initial focus."""
        box = Frame(self)
        self.__itemlistbox = ItemListbox(box, master_list=self.__master_list)
        self.__itemlistbox.pack(side=LEFT, padx=PADX, pady=PADY)
        self.__itemlistbox.bind_selection(self._withdraw)
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
        box.pack()

    def apply(self) -> None:
        self.__withdrawed_items = self.__temp_withdraw

    def _withdraw(self, _:Event) -> float:
        item = self.__itemlistbox.get_record()
        change = ask_localfloat(title="Kivét", prompt=item.name, root=self,
                                initvalue=item.stock, minvalue=0,
                                maxvalue=item.stock, unit=item.unit)
        if change:
            setattr(item, "change", -change)
            self.__temp_withdraw.append(item)
            for item in self.__temp_withdraw:
                print(item.withdraw_view)
            print("---")

    @property
    def withdrawed_items(self) -> List[StockItemRecord]|None:
        return self.__withdrawed_items