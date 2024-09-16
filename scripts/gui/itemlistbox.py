from tkinter import *
from tkinter import ttk


class ItemListbox(LabelFrame):
    def __init__(self, title="Raktárkészlet") -> None:
        super().__init__(text=title)
        self._init_controll_variables()
        self._build_interface()
        self._master_list = None
        self._item_list = None

    def _init_controll_variables(self) -> None:
        self.filter_var = StringVar()
        self.list_var = StringVar()

    def _build_interface(self) -> None:
        self.filter_entry = ttk.Entry(self,
                                      textvariable=self.filter_var,
                                      validate="key")

        vertical_scroll = Scrollbar(self, orient=VERTICAL)
        self.list_box = Listbox(self,
                                cursor="hand2",
                                font=("Liberation Mono", "-12"),
                                listvariable=self.list_var,
                                selectmode=SINGLE,
                                width=60,
                                height=23,
                                yscrollcommand=vertical_scroll.set)
        vertical_scroll["command"]=self.list_box.yview

        self.list_box.bind("<Button-4>",
                           lambda _: self.list_box.yview_scroll(-1, UNITS))
        self.list_box.bind("<Button-5>",
                           lambda _: self.list_box.yview_scroll(1, UNITS))
        self.list_box.bind("<MouseWheel>",
            lambda e: self.list_box.yview_scroll(int(e.delta / 120), UNITS))

        self.filter_entry.grid(row=0, column=0, columnspan=2, sticky=E+W)
        self.list_box.grid(row=1, column=0)
        vertical_scroll.grid(row=1, column=1, sticky=N+S)

    def populate(self, item_list:list) -> None:
        for item in item_list:
            self.list_box.insert(END, str(item))
        
    def clear(self) -> None:
        self.list_box.delete(0, END)
    
    def register_filter(self, reference:str) -> None:
        self.filter_entry["validatecommand"] = (reference, "%P")


if __name__ == "__main__":
    itemlist = ItemListbox()
    itemlist.grid()
    itemlist.mainloop()