"""
INVENTORY APPLICATION
"""


import locale
locale.setlocale(locale.LC_ALL, "")

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
        self.all_items = [StockItemRecord(**item) for item in\
                          self.dbsession.select_all_items().fetchall()]
        self.gui = Gui()
        self.gui.itemlist.populate(self.all_items)
        self.gui.mainloop()


if __name__ == "__main__":
    InventoryApp()