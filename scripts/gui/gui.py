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
        self._build_interface()
        self.bind_all("<KeyPress>", self._update_labels)
        self.grid(padx=PADX, pady=PADY)

    def _build_interface(self):
        self.displaymask = DisplayMask()
        self.stockitemmask = StockItemMask()
        self.itemmask = ItemMask()
        self.displaymask.update_(1, "", 8912234.35)
        self.displaymask.grid(padx=PADX, pady=PADY, sticky=E+W)
        self.itemmask.grid(padx=PADX, pady=PADY, sticky=E+W)
        self.stockitemmask.grid(padx=PADX, pady=PADY, sticky=E+W)

    def _update_labels(self, _:Event):
        self.stockitemmask.unit_var.set(self.itemmask.unit_var.get())
        self.stockitemmask.value_var.set(self.stockitemmask.retrieve().value_fmt)
        self.displaymask.update_(1, "valami", 8912234.35)


if __name__ == "__main__":
    import locale
    locale.setlocale(locale.LC_ALL, "")
    gui = Gui()
    gui.mainloop()
