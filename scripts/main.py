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
from scripts.projectnumber import Projectnumber
from scripts.rep import Rep
from scripts.stockitemrecord import StockItemRecord


DATABASE = "data/adatok.db"


class InventoryApp():
    def __init__(self, database:str=DATABASE) -> None:
        self.__dbsession = DatabaseSession(database)
        self.__gui = Gui()
        lookup_ = self.__gui.itemlistbox.register(self._lookup)
        self.__gui.itemlistbox.register_lookup(lookup_)
        self.__gui.itemlistbox.bind_selection(self._show_selected)
        self.__gui.controldevice.set_saveitem_command(self._saveitem)
        all_items = self.__dbsession.select_all_items()
        self.__gui.itemlistbox.populate(self._load(all_items))
        self.__gui.itemlistbox.select_first()
        self.__gui.mainloop()

    def _lookup(self, term:str) -> bool:
        self.__gui.itemlistbox.clear()
        selection = self._load(self.__dbsession.select_all_items())
        for word in re.split(r"\W+", term.lower()):
            if word:
                selection = [item for item in selection if item.contains(word)]
        self.__gui.itemlistbox.populate(selection)
        try:
            self.__gui.itemlistbox.select_first()
        except IndexError:  # no result, empty list
            pass
        return True

    def _load(self, source:Cursor) -> list[StockItemRecord]:
        return [StockItemRecord(**item) for item in source]

    def _show_selected(self, _) -> None:
        item = self.__gui.itemlistbox.get_record()
        if item:
            self.__gui.update_form(item)
    
    def _saveitem(self) -> None:
        if self.__gui.stockitemform.is_valid():
            item = self.__gui.stockitemform.retrieve()
            self.__dbsession.write_item(item)
        else:
            self.__gui.showwarning(title="Vigyázz!",
                                   message="A piros mezőket töltsd ki!")


if __name__ == "__main__":
    InventoryApp()