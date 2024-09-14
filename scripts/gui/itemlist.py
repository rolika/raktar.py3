from tkinter import *
from tkinter import ttk


class ItemList(LabelFrame):
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
        filter_for = self.register(self._filter_for)
        self.filter_entry = ttk.Entry(self,
                                      textvariable=self.filter_var,
                                      validate="all",
                                      validatecommand=(filter_for, "%P"))

        vertical_scroll = Scrollbar(self, orient=VERTICAL)
        self.list_box = Listbox(self,
                                cursor="hand2",
                                listvariable=self.list_var,
                                selectmode=SINGLE,
                                width=60,
                                height=18,
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
        self._master_list = list(item_list)
        for i, item in enumerate(item_list):
            self.list_box.insert(i, str(item))

    def _filter_for(self, text:str) -> bool:
        self.list_box.delete(0, END)
        for i, item in enumerate(self._master_list):
            if text in str(item):
                self.list_box.insert(i, str(item))
        return True


if __name__ == "__main__":
    itemlist = ItemList()
    itemlist.grid()
    itemlist.mainloop()