import pathlib
import sqlite3

LOG_COLUMNS = "megnevezes, egysegar, egyseg, valtozas, datum, projektszam"


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
                            SET keszlet = ?, utolso_modositas = date()
                            WHERE cikkszam = ?;""", (quantity, primary_key))

    def update_item(self,
                    primary_key:int,
                    name:str,
                    nickname:str,
                    manufacturer:str,
                    description:str,
                    color:str,
                    comment:str,
                    unit:str,
                    unitprice:float,
                    packaging:float,
                    place:str,
                    shelflife:float,
                    manufacturing_date:str) -> None:
        with self:
            self.execute("""
                UPDATE raktar
                SET megnevezes = ?,
                    becenev = ?,
                    gyarto = ?,
                    leiras = ?,
                    szin = ?,
                    megjegyzes = ?,
                    egyseg = ?,
                    egysegar = ?,
                    kiszereles = ?,
                    hely = ?,
                    lejarat = ?,
                    gyartasido = ?,
                    utolso_modositas = date()
                WHERE cikkszam = ?;
                """, (name,
                      nickname,
                      manufacturer,
                      description,
                      color,
                      comment,
                      unit,
                      unitprice,
                      packaging,
                      place,
                      shelflife,
                      manufacturing_date,
                      primary_key))

    def insert_item(self,
                    stock:float,
                    name:str,
                    nickname:str,
                    manufacturer:str,
                    description:str,
                    color:str,
                    comment:str,
                    unit:str,
                    unitprice:float,
                    packaging:float,
                    place:str,
                    shelflife:float,
                    manufacturing_date:str) -> None:
        with self:
            self.execute("""
                INSERT INTO raktar(keszlet,
                                   megnevezes,
                                   becenev,
                                   gyarto,
                                   leiras,
                                   szin,
                                   megjegyzes,
                                   egyseg,
                                   egysegar,
                                   kiszereles,
                                   hely,
                                   lejarat,
                                   gyartasido,
                                   letrehozas,
                                   utolso_modositas)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                        date(), date())
                """, (stock,
                      name,
                      nickname,
                      manufacturer,
                      description,
                      color,
                      comment,
                      unit,
                      unitprice,
                      packaging,
                      place,
                      shelflife,
                      manufacturing_date))

    def get_last_rowid(self) -> int:
        return self.execute("""SELECT last_insert_rowid();""").fetchone()[0]

    def filter_for(self, term:str) -> sqlite3.Cursor:
        return self.execute(f"""
SELECT cikkszam, megnevezes, becenev, gyarto, leiras, szin, megjegyzes, hely
FROM raktar
WHERE
lower(megnevezes || becenev || gyarto || leiras || szin || megjegyzes || hely)
LIKE "%{term.lower()}%"
ORDER BY gyarto, megnevezes;""")

    def mark_item(self, primary_key:int, color:str) -> None:
        with self:
            self.execute("""UPDATE raktar SET jeloles = ? WHERE cikkszam = ?""",
                        (color, primary_key))

    def log_change(self,
                   name:str,
                   unitprice:float,
                   unit:str,
                   change:float,
                   projectnumber:str) -> None:
        with self:
            self.execute("""
INSERT INTO
    raktar_naplo(megnevezes, egysegar, egyseg, valtozas, datum, projektszam)
VALUES (?, ?, ?, ?, date(), ?)
            """, (name, unitprice, unit, change, projectnumber))

    def query_log(self, projectnumber:str, month:str) -> sqlite3.Cursor:
        """Query items belonging to projectnumber and inserted in month.
        Both arguments should be verified for proper formatting before calling:
        projectnumber:  yy_nnn
        month:          yyyy-mm"""
        return self.execute(f"""
            SELECT {LOG_COLUMNS}
            FROM raktar_naplo
            WHERE projektszam = ?
            AND strftime('%Y-%m', datum) = ?;
        """, (projectnumber, month))

    def query_months(self) -> sqlite3.Cursor:
        """Query distinct months in descending order."""
        return self.execute("""
            SELECT DISTINCT strftime('%Y-%m', datum)
            FROM raktar_naplo
            ORDER BY datum DESC;
        """)

    def query_projects(self, month="2023-04") -> sqlite3.Cursor:
        """Query distinct projectnumbers in ascending order."""
        return self.execute("""
            SELECT DISTINCT projektszam
            FROM raktar_naplo
            WHERE strftime("%Y-%m", datum) = ?
            ORDER BY projektszam ASC;
        """, (month, ))