"""
INVENTORY APPLICATION
"""

import locale
locale.setlocale(locale.LC_ALL, "")

import re
from sqlite3 import Cursor

from scripts.databasesession import DatabaseSession
from scripts.filesession import FileSession
from scripts.gui.gui import Gui
from scripts.gui.withdraw_gui import WithdrawGui
from scripts.listboxdatabasemediator import ListboxDatabaseMediator
from scripts.projectnumber import Projectnumber
from scripts.rep import Rep
from scripts.stockitemrecord import StockItemRecord


DATABASE = "data/adatok.db"


class InventoryApp():
    def __init__(self, database:str=DATABASE) -> None:
        self.__dbsession = DatabaseSession(database)
        self.__gui = Gui()
        self._bindings()
        all_items = self.__dbsession.select_all_items()
        self.__gui.itemlistbox.populate(self._load(all_items))
        self.__gui.itemlistbox.select_index(0)
        self.__gui.mainloop()

    def _bindings(self) -> None:
        lookup_ = self.__gui.itemlistbox.register(self._lookup)
        self.__gui.itemlistbox.register_lookup(lookup_)
        self.__gui.itemlistbox.bind_selection(self._show_selected)
        self.__gui.controldevice.set_saveitem_command(self._save_item)
        self.__gui.controldevice.set_withdraw_command(self._new_waybill)
        self.__gui.bind_all("<Escape>", self._clear_selection)
        self.__gui.itemlistbox.bind_clear_selection(self._clear_selection)

    def _lookup(self, term:str) -> bool:
        self.__gui.itemlistbox.clear_listbox()
        selection = self._load(self.__dbsession.select_all_items())
        for word in re.split(r"\W+", term.lower()):
            if word:
                selection = [item for item in selection if item.contains(word)]
        self.__gui.itemlistbox.populate(selection)
        try:
            self.__gui.itemlistbox.select_index(0)
        except IndexError:  # no result, empty list
            pass
        return True

    def _load(self, source:Cursor) -> list[StockItemRecord]:
        return [StockItemRecord(**item) for item in source]

    def _show_selected(self, _) -> None:
        item = self.__gui.itemlistbox.get_record()
        if item:
            self.__gui.update_form(item)

    def _save_item(self) -> None:
        if item := self.__gui.check_item():
            self.__dbsession.write_item(item)
            if not item.articlenumber:  # this is an insert
                self.__gui.itemlistbox.clear_listbox()
                all_items = self.__dbsession.select_all_items()
                self.__gui.itemlistbox.populate(self._load(all_items))
                item.articlenumber = self.__dbsession.get_last_rowid()
            self.__gui.itemlistbox.update_item(item)

    def _clear_selection(self, _=None) -> None:
        self.__gui.itemlistbox.clear_entry()
        self._lookup("")
    
    def _new_waybill(self) -> None:
        mediator = ListboxDatabaseMediator()
        mediator.add_dbsession(self.__dbsession)
        WithdrawGui(mediator=mediator)


if __name__ == "__main__":
    InventoryApp()