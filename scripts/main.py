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
        self._dbsession = DatabaseSession(database)
        self._gui = Gui()
        lookup_ = self._gui.itemlistbox.register(self.lookup)
        self._gui.itemlistbox.register_lookup(lookup_)
        self._gui.itemlistbox.bind_selection(self.show_selected)
        all_items = self._dbsession.select_all_items()
        self._gui.itemlistbox.populate(self.load(all_items))
        self._gui.itemlistbox.select_first()
        self._gui.mainloop()

    def lookup(self, term:str) -> bool:
        self._gui.itemlistbox.clear()
        filtered = self.load(self._dbsession.select_all_items())
        for word in re.split(r"\W+", term.lower()):
            if word:
                filtered = [item for item in filtered if item.contains(word)]
        self._gui.itemlistbox.populate(filtered)
        try:
            self._gui.itemlistbox.select_first()
        except IndexError:  # no result, empty list
            pass
        return True

    def load(self, source:Cursor) -> list[StockItemRecord]:
        return [StockItemRecord(**item) for item in source]

    def show_selected(self, _) -> None:
        item = self._gui.itemlistbox.get_record()
        if item:
            self._gui.update_mask(item)


if __name__ == "__main__":
    InventoryApp()