import os
from tkinter import *

from scripts.gui.display import Display
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
    
    def _build_interface(self):
        self.itemmask = ItemMask()
        self.itemmask.bind_all("<KeyPress>", self._update_labels)
        self.stockitemmask = StockItemMask()
        self.display = Display()
    
    def _update_labels(self, _:Event):
        self.stockitemmask.unit_var.set(self.itemmask.unit_var.get())


if __name__ == "__main__":
   gui = Gui()
   gui.mainloop()
