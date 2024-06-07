import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.simpledialog import askstrin


PROGRAM = "Készlet-nyilvántartó"
WINDOWS_ICON = "data/pohlen.ico"
LINUX_ICON = "data/pohlen.gif"
MARKER_COLOR = ("green", "darkgreen")
#grid-jellemzők
LONG_FIELD = 42
MID_FIELD = 12
SHORT_FIELD = 8
BUTTON_WIDTH = 8
PADX = 2
PADY = 2


class Gui(Frame):
    def __init__(self, root=None, version="0.00"):
        super().__init__(root)
        if os.name == "posix":
            ikon = PhotoImage(file = LINUX_ICON)
            self.master.tk.call("wm", "iconphoto", self.master._w, ikon)
        else:
            self.master.iconbitmap(default = WINDOWS_ICON)
        self.master.title(PROGRAM + " v" + version)
        self.grid()
        self._control_variables()
        self._widgets()
    
    def _control_variables(self):
        # calculated / given values
        self.articlenumber = StringVar()
        self.stock = StringVar()
        self.itemvalue = StringVar()
        self.selection_value = StringVar()
        self.inventroyvalue = StringVar()
        self.value = (self.articlenumber,
                      self.stock,
                      self.stockvalue,
                      self.selection_values_erteke,
                      self.inventroyvalue)
        # values submitted by user
        self.name = StringVar()
        self.nickname = StringVar()
        self.manufacturer = StringVar()
        self.description = StringVar()
        self.color = StringVar()
        self.comment = StringVar()
        self.place = StringVar()
        self.production_date = StringVar()
        self.unit = StringVar()
        self.unitprice = StringVar()
        self.change = StringVar()
        self.packaging = StringVar()
        self.shelflife = StringVar()
        self.ariclenumbers = []  # actual selection
        self.itemlist = StringVar()  # itemlist for Listbox
        self.waybill_list = []
    
    def _widgets(self):
        pass
