import re
from tkinter import *
from tkinter import ttk

from scripts.databasesession import DatabaseSession
from scripts.stockitemrecord import StockItemRecord


class ItemListbox(LabelFrame):
    def __init__(self, root=None, title="Raktárkészlet",
                 dbsession:DatabaseSession=None) -> None:
        super().__init__(root, text=title)
        self.__selected_item = None
        self.__item_list = None
        self.__dbsession = dbsession
        self._init_controll_variables()
        self._build_interface()
        self._bindings()

    def _init_controll_variables(self) -> None:
        self.__lookup_var = StringVar()
        self.__list_var = StringVar()

    def _build_interface(self) -> None:
        self.__lookup_entry = ttk.Entry(self, textvariable=self.__lookup_var,
                                        validate="key")
        self.__clear_button = Button(self, bitmap="questhead")
        self.__clear_button.grid(row=0, column=1)
        self.__lookup_entry.focus()

        vertical_scroll = Scrollbar(self, orient=VERTICAL)
        self.__listbox = Listbox(self,
                                 cursor="hand2",
                                 font=("Liberation Mono", "-12"),
                                 listvariable=self.__list_var,
                                 selectmode=SINGLE,
                                 width=60,
                                 height=23,
                                 yscrollcommand=vertical_scroll.set)
        vertical_scroll["command"]=self.__listbox.yview

        self.__listbox.bind("<Button-4>",
                            lambda _: self.__listbox.yview_scroll(-1, UNITS))
        self.__listbox.bind("<Button-5>",
                            lambda _: self.__listbox.yview_scroll(1, UNITS))
        self.__listbox.bind("<MouseWheel>",
            lambda e: self.__listbox.yview_scroll(int(e.delta / 120), UNITS))

        self.__lookup_entry.grid(row=0, column=0, sticky=E+W)
        self.__listbox.grid(row=1, column=0)
        vertical_scroll.grid(row=1, column=1, sticky=N+S)
    
    def _bindings(self) -> None:
        lookup_ = self.__listbox.register(self.lookup)
        self.__lookup_entry["validatecommand"] = (lookup_, "%P")

    def populate(self, item_list:list) -> None:
        self.__item_list = item_list
        for item in item_list:
            self.__listbox.insert(END, str(item))

    def clear_listbox(self) -> None:
        self.__listbox.delete(0, END)

    def clear_entry(self) -> None:
        self.__lookup_var.set("")

    def register_lookup(self, reference:str) -> None:
        self.__lookup_entry["validatecommand"] = (reference, "%P")

    def bind_selection(self, method:callable) -> None:
        self.__listbox.bind("<<ListboxSelect>>", method)

    def bind_clear_selection(self, method:callable) -> None:
        self.__clear_button["command"] = method

    def get_record(self) -> StockItemRecord:
        try:
            self.__selected_item =\
                self.__item_list[self.__listbox.curselection()[0]]
            return self.__selected_item
        except IndexError:  # empty list
            return None

    def select_index(self, idx:int) -> None:
        self.__listbox.selection_set(idx)
        self.__listbox.event_generate("<<ListboxSelect>>")

    def update_item(self, item:StockItemRecord) -> None:
        for idx, stockitem in enumerate(self.__item_list):
            if stockitem.articlenumber == item.articlenumber:
                break
        self.__item_list[idx] = item
        self.__listbox.delete(idx)
        self.__listbox.insert(idx, str(item))
        self.select_index(idx)
        self.__listbox.see(idx)

    def lookup(self, term:str) -> bool:
        assert self.__dbsession
        self.clear_listbox()
        selection = self.__dbsession.load_all_items()
        for word in re.split(r"\W+", term.lower()):
            if word:
                selection = [item for item in selection if item.contains(word)]
        self.populate(selection)
        try:
            self.select_index(0)
        except IndexError:  # no result, empty list
            pass
        return True

    @property
    def selected_item(self) -> StockItemRecord:
        return self.__selected_item
    
    @property
    def lookup_entry(self) -> ttk.Entry:
        return self.__lookup_entry


if __name__ == "__main__":
    itemlist = ItemListbox()
    itemlist.grid()
    itemlist.mainloop()