from sqlite3 import Cursor
from typing import List

from scripts.databasesession import DatabaseSession
from scripts.gui.itemlistbox import ItemListbox
from scripts.stockitemrecord import StockItemRecord


def _load(cursor:Cursor) -> List[StockItemRecord]:
    return [StockItemRecord(**item) for item in cursor]


class ListboxDatabaseMediator():
    def __init__(self) -> None:
        self.__itemlistbox = None
        self.__dbsession = None
    
    def add_itemlistbox(self, itemlistbox:ItemListbox) -> None:
        self.__itemlistbox = itemlistbox
    
    def add_dbsession(self, dbsession:DatabaseSession) -> None:
        self.__dbsession = dbsession
    
    def populate(self):
        all_items = self.__dbsession.select_all_items()
        self.__itemlistbox.populate(_load(all_items))
        self.__itemlistbox.select_index(0)