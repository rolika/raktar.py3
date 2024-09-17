"""
INVENTORY APPLICATION
"""


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
        self._gui.itemlistbox.register_filter(lookup_)
        all_items = self._dbsession.select_all_items()
        self._gui.itemlistbox.populate(self.load(all_items))
        self._gui.mainloop()

    def lookup(self, text:str) -> bool:
        self._gui.itemlistbox.clear()
        if filtered := self._dbsession.filter_for(text):
            self._gui.itemlistbox.populate(self.load(filtered))
        return True

    def load(self, source:iter) -> list[StockItemRecord]:
        return [StockItemRecord(**item) for item in source.fetchall()]


if __name__ == "__main__":
    InventoryApp()