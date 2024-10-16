import locale
locale.setlocale(locale.LC_ALL, "")

from tkinter import *
from tkinter import ttk
from tkinter import simpledialog

from scripts.gui import styles



class AskLocalFloat(simpledialog.Dialog):
    """Ask for a float number and verify it considering locale settings."""
    def __init__(self, title:str, prompt:str, root=None, initvalue:float=None,
                 minvalue:float=None, maxvalue:float=None) -> None:
        self.__prompt = prompt
        self.__minvalue = minvalue
        self.__maxvalue = maxvalue
        self.__number = None
        self.__entry_var = StringVar()
        if initvalue:
            self.__entry_var.set(initvalue)
        super().__init__(root, title=title)

    def body(self, root:Widget) -> Widget:
        is_okay = self.register(self._is_okay)
        box = Frame(self)
        ttk.Label(box, text=self.__prompt).pack()
        entry = ttk.Entry(box, justify=RIGHT, textvariable=self.__entry_var,
                          validate="all", validatecommand=(is_okay, "%P", "%W"))
        entry.select_range(0, END)
        entry.pack()
        box.pack()
        return entry

    def buttonbox(self):
        """Override standard button texts."""
        box = Frame(self)
        self.__ok_button = Button(box, text="OK", width=10,
                                  command=self.ok, default=ACTIVE)
        self.__ok_button.pack(side=LEFT, padx=5, pady=5)
        Button(box, text="Mégse", width=10, command=self.cancel)\
            .pack(side=LEFT, padx=5, pady=5)
        self.bind("<Return>", self.ok)
        self.bind("<KP_Enter>", self.ok)
        self.bind("<Escape>", self.cancel)
        box.pack()

    def apply(self) -> None:
        value = self.__entry_var.get()
        if value:
            self.__number = float(value)

    @property
    def number(self) -> float:
        return self.__number

    def _is_okay(self, text:str, name:str) -> bool:
        number = None
        try:
            number = float(text)
            styles.apply_entry_ok(self, name)
            self.__ok_button["state"] = NORMAL
        except ValueError:
            styles.apply_entry_error(self, name)
            self.__ok_button["state"] = DISABLED
        return True

if __name__ == "__main__":
    value = AskLocalFloat(title="Kivét", prompt="Mennyit veszel ki?",
                          initvalue=324.5)
    print(value.number)