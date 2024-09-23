import os
from tkinter import *

from scripts.gui.selectiondisplay import SelectionDisplay
from scripts.gui.itemlistbox import ItemListbox
from scripts.gui.stockitemform import StockItemForm
from scripts.stockitemrecord import StockItemRecord


PROGRAM = "Készlet-nyilvántartó"
WINDOWS_ICON = "data/pohlen.ico"
LINUX_ICON = "data/pohlen.gif"
MARKER_COLOR = ("green", "darkgreen")

PADX = 2
PADY = 2


class Gui(Frame):
    def __init__(self, root=None, version="0.0.0"):
        super().__init__(root)
        if os.name == "posix":
            icon = PhotoImage(file = LINUX_ICON)
            self.master.tk.call("wm", "iconphoto", self.master._w, icon)
        else:
            self.master.iconbitmap(default = WINDOWS_ICON)
        self.master.title(PROGRAM + " v" + version)
        self._build_interface()
        self.bind_all("<KeyPress>", self._update_labels)
        self.grid(padx=PADX, pady=PADY)

    def _build_interface(self):
        self.displaymask = SelectionDisplay()
        self.stockitemmask = StockItemForm()
        self.itemlistbox = ItemListbox()
        self.displaymask.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=E+W)
        self.stockitemmask.grid(row=1, column=0, padx=PADX, pady=PADY,
                                sticky=E+W)
        self.itemlistbox.grid(row=0, column=1, rowspan=2, padx=PADX, pady=PADY,
                           sticky=N+S)

    def _update_labels(self, _):
        self.stockitemmask.value = self.stockitemmask.retrieve().value
        self.displaymask.lookup = self.itemlistbox.lookup
    
    def update_mask(self, item:StockItemRecord) -> None:
        self.stockitemmask.populate(item)
        self._update_labels(1)


if __name__ == "__main__":
    import locale
    locale.setlocale(locale.LC_ALL, "")
    gui = Gui()
    gui.displaymask.update_(1, "valami", 8912234.35)
    test_list = [str(i) for i in range(50)]
    gui.itemlistbox.populate(test_list)
    gui.mainloop()
