from sqlite3 import Cursor
from typing import List

from scripts.databasesession import DatabaseSession
from scripts.gui.withdraw_gui import WithdrawGui
from scripts.stockitemrecord import StockItemRecord


def _load(cursor:Cursor) -> List[StockItemRecord]:
    return [StockItemRecord(**item) for item in cursor]


class GuiDbaseMediator():
    def __init__(self) -> None:
        self.__gui = None
        self.__dbsession = None
    
    def add_gui(self, gui:WithdrawGui) -> None:
        self.__gui = gui
    
    def add_dbsession(self, dbsession:DatabaseSession) -> None:
        self.__dbsession = dbsession
    
    def populate(self):
        all_items = self.__dbsession.select_all_items()
        self.__gui.itemlistbox.populate(_load(all_items))
        self.__gui.itemlistbox.select_index(0)