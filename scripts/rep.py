import sqlite3
from typing import Iterable

from szam_megjelenites import *


class Rep:
    """A reprezentációs osztály a terminálon kijelzésekhez és a fileexportokhoz
    biztosít vonalat, címsort, fejlécet."""

    def vonal(karakter:str="_", hossz:int=80) -> str:
        """Megadott hosszúságú vonal rajzolása."""
        return "".join(karakter for _ in range(hossz)) + "\n"

    def cimsor(szoveg:str) -> str:
        """A címsor csupa nagybetű, a betű között szóközzel, középre igazított,
        alul-felül átmenő vonallal."""
        cim = " ".join(betu.upper() for betu in szoveg)
        return "{}{:^80}{}{}".format(Rep.vonal(), cim, "\n", Rep.vonal())

    def fejlec(karakter:str="", **kwargs:dict[str,int]) -> str:
        """A fejléc csupa balra igazított, nagybetűvel kezdődő szavakból áll,
        melyek egymástól meghatározott távolságra vannak és karakter köti össze
        őket, aláhúzva egy folytonos vonallal."""
        formatspec = ("{:" + karakter + "<" + str(kwargs[szo]) + "}" \
                      for szo in kwargs)
        fejlec = "".join(formatspec)\
            .format(*(szo.capitalize() for szo in kwargs.keys()))
        return fejlec + "\n" + Rep.vonal()

    def stock2str(cursor:sqlite3.Cursor, articles:Iterable[int]) -> str:
        """Build a string of the presented articles to show the stock."""
        result = ""
        for i, article in enumerate(articles):
            cursor.execute("""
            SELECT megnevezes, keszlet, egyseg, egysegar
            FROM raktar
            WHERE cikkszam = {};
            """.format(article))
            record = cursor.fetchone()
            if record["keszlet"]:
                result += "{:>6}  {:<28} {:>8} {:<3} {:>9} Ft/{:<4}{:>10} Ft\n"\
                        .format(format(i + 1, "0=5"),
                            record["megnevezes"][0:28],
                            ezresv(format(float(record["keszlet"]), ".0f")),
                            record["egyseg"][:3],
                            ezresv(record["egysegar"]),
                            record["egyseg"][:3],
                            ezresv(int(float(record["keszlet"]) * float(record["egysegar"]))))
        return result

    def waybill2str(articles:dict) -> str:
        """Build a string of the presented articles to show the waybill."""
        result = ""
        for i, article in enumerate(articles):
            result += "{:>6}   {:<50} {:>12} {}\n"\
                        .format(format(i + 1, "0=5"),
                                       article["megnevezes"][0:49],
                                       ezresv(format(abs(article["valtozas"]),\
                                                     ".2f")),
                                       article["egyseg"])
        return result