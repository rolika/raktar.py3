from pathlib import Path
from sqlite3 import Connection, Cursor


class DBSession(Connection):
    """This class handles all database-related stuff."""

    LOG_COLUMNS = "megnevezes, egysegar, egyseg, valtozas, datum, projektszam"

    def __init__(self, filename:str) -> None:
        """Initialize an sqlite database connection.
        It is an error if the file doesn't exist."""
        dbfile = Path(filename)
        if not dbfile.is_file():
            raise FileNotFoundError(f"{filename} doesn't exist.")
        super().__init__(dbfile)

    def query(self, projectnumber:str, month:str) -> Cursor:
        """Query items belonging to projectnumber and inserted in month.
        Both arguments should be verified for proper formatting before calling:
        projectnumber:  yy_nnn
        month:          yyyy-mm"""
        cursor = self.cursor()
        cursor.execute(f"""
        SELECT {DBSession.LOG_COLUMNS}
        FROM raktar_naplo
        WHERE projektszam = ?
        AND strftime('%Y-%m', datum) = ?;
        """, (projectnumber, month))
        return cursor

    def query_months(self) -> Cursor:
        """Query distinct months in descending order."""
        cursor = self.cursor()
        cursor.execute("""
        SELECT DISTINCT strftime('%Y-%m', datum)
        FROM raktar_naplo
        ORDER BY datum DESC;
        """)
        return cursor

    def query_projects(self, month="2023-04") -> Cursor:
        """Query distinct projectnumbers in ascending order."""
        cursor = self.cursor()
        cursor.execute("""
        SELECT DISTINCT projektszam
        FROM raktar_naplo
        WHERE strftime("%Y-%m", datum) = ?
        ORDER BY projektszam ASC;
        """, (month, ))
        return cursor
