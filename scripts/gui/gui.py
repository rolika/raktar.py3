import os
from tkinter import *

from scripts.gui.displaymask import DisplayMask
from scripts.gui.itemmask import ItemMask
from scripts.gui.stockitemmask import StockItemMask


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
            ikon = PhotoImage(file = LINUX_ICON)
            self.master.tk.call("wm", "iconphoto", self.master._w, ikon)
        else:
            self.master.iconbitmap(default = WINDOWS_ICON)
        self.master.title(PROGRAM + " v" + version)
        self.grid(padx=PADX, pady=PADY)
        self._build_interface()
        self.bind_all("<KeyPress>", self._update_labels)

    def _build_interface(self):
        self.itemmask = ItemMask()
        self.stockitemmask = StockItemMask()
        self.displaymask = DisplayMask()
        self.displaymask.update_(1, "", 8912234.35)

    def _update_labels(self, _:Event):
        self.stockitemmask.unit_var.set(self.itemmask.unit_var.get())
        self.stockitemmask.value_var.set(self.stockitemmask.retrieve().value_fmt)
        self.displaymask.update_(1, "valami", 8912234.35)


if __name__ == "__main__":
    import locale
    locale.setlocale(locale.LC_ALL, "")
    gui = Gui()
    gui.mainloop()
