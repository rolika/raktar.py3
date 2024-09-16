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
        self.dbsession = DatabaseSession(database)
        self.gui = Gui()
        lookup_ = self.gui.itemlistbox.register(self.lookup)
        self.gui.itemlistbox.register_filter(lookup_)
        all_items = self.dbsession.select_all_items()
        self.gui.itemlistbox.populate(self.load(all_items))
        self.gui.mainloop()
    
    def lookup(self, text:str) -> bool:
        self.gui.itemlistbox.clear()
        if filtered := self.dbsession.filter_for(text):
            self.gui.itemlistbox.populate(self.load(filtered))
        return True
    
    def load(self, source:iter) -> list[StockItemRecord]:
        return [StockItemRecord(**item) for item in source.fetchall()]


if __name__ == "__main__":
    InventoryApp()