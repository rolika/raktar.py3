"""
INVENTORY APPLICATION
"""

import locale
locale.setlocale(locale.LC_ALL, "")

from scripts.gui.askprojectnumber import AskProjectNumber
from scripts.databasesession import DatabaseSession
from scripts.gui.title_ui import TitleUI
from scripts.gui.withdrawdialog import WithdrawDialog


DATABASE = "data/adatok.db"


class InventoryApplication():
    def __init__(self, database:str=DATABASE) -> None:
        self.__dbsession = DatabaseSession(database)
        self.__projectnumber = None
        self.__ui = TitleUI(self)
        self._bindings()
        self.__ui.pack()
        self.__ui.mainloop()

    def _bindings(self) -> None:
        self.__ui.withdraw_button= self._withdraw
    
    def _withdraw(self) -> None:
        project = AskProjectNumber(self.__ui)
        self.__projectnumber = project.projectnumber
        if not self.__projectnumber:
            return
        withdraw_dialog = WithdrawDialog(self.__ui, self.__dbsession,
                                         self.__projectnumber)
        self.__dbsession.log_stock_change(withdraw_dialog.withdrawed_items)
                


if __name__ == "__main__":
    InventoryApplication()