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
        self.grid(padx=PADX, pady=PADY)

    def _build_interface(self):
        self.stockitemform = StockItemForm()
        self.itemlistbox = ItemListbox()
        self.stockitemform.grid(row=0, column=0, padx=PADX, pady=PADY,
                                sticky=N+E+W)
        self.itemlistbox.grid(row=0, column=1, padx=PADX, pady=PADY,
                              sticky=N+S)

    def update_form(self, item:StockItemRecord) -> None:
        self.stockitemform.populate(item)


if __name__ == "__main__":
    import locale
    locale.setlocale(locale.LC_ALL, "")
    gui = Gui()
    test_list = [str(i) for i in range(50)]
    gui.itemlistbox.populate(test_list)
    gui.mainloop()
