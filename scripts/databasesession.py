import pathlib
import sqlite3


class DatabaseSession(sqlite3.Connection):
    """This class handles all database-related stuff."""

    def __init__(self, filepath:str) -> None:
        """Initialize an sqlite database connection."""
        super().__init__(pathlib.Path(filepath))
        self.row_factory = sqlite3.Row  # access results with column-names
        self._create_tables()

    def _create_tables(self):
        with self:
            self.execute("""
                CREATE TABLE IF NOT EXISTS raktar(
                    cikkszam INTEGER PRIMARY KEY ASC,
                    keszlet,
                    megnevezes,
                    becenev,
                    gyarto,
                    leiras,
                    megjegyzes,
                    egyseg,
                    egysegar,
                    kiszereles,
                    hely,
                    lejarat,
                    gyartasido,
                    szin,
                    letrehozas,
                    utolso_modositas);
                """)
            self.execute("""
                CREATE TABLE IF NOT EXISTS raktar_naplo(
                    azonosito INTEGER PRIMARY KEY ASC,
                    megnevezes,
                    egysegar,
                    egyseg,
                    valtozas,
                    datum,
                    projektszam);
                """)

    def select_all_items(self) -> sqlite3.Cursor:
        return self.execute("""SELECT * FROM raktar ORDER BY gyarto, megnevezes;
               """)

    def select_item(self, primary_key:int) -> sqlite3.Cursor:
        return self.execute("""SELECT * FROM raktar WHERE cikkszam = ?;""",
                            (primary_key, ))

    def set_stock_quantity(self, primary_key:int, quantity:float) -> None:
        with self:
            self.execute("""UPDATE raktar
                            SET keszlet = ?, utolso_modositas = (SELECT date())
                            WHERE cikkszam = ?;""", (quantity, primary_key))