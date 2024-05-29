###################################
#                                 #
#   Készletnyilvántartó program   #
#                                 #
###################################

# Copyright (c) 2015 Weisz Roland weisz.roland@wevik.hu
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.


from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.simpledialog import askstring
from time import strftime  # időbélyeghez
import sqlite3
import os
import re

from filesession import FileSession, EXPORTFOLDER
from misc import projectnr_from, valid_projectnr, fmt_projectnr
from rep import Rep
from szam_megjelenites import *


__version__ = "0.52"


PROGRAM = "Készlet-nyilvántartó"
WINDOWS_IKON = "data/pohlen.ico"
LINUX_IKON = "data/pohlen.gif"
ADATBAZIS = "data/adatok.db"
SZERVEZET = ["Pohlen-Dach Hungária Bt.", "8440-Herend", "Dózsa utca 49."]
VEVO = ["", "", ""]
JELOLOSZIN = ("green", "darkgreen")
#grid-jellemzők
HOSSZU_MEZO = 42
KOZEP_MEZO = 12
ROVID_MEZO = 8
GOMB_SZELES = 8
PADX = 2
PADY = 2


class RaktarKeszlet(Frame):
    def __init__(self, root = None):
        super().__init__(root)
        if os.name == "posix":
            ikon = PhotoImage(file = LINUX_IKON)
            self.master.tk.call("wm", "iconphoto", self.master._w, ikon)
        else:
            self.master.iconbitmap(default = WINDOWS_IKON)
        self.master.title(PROGRAM + " v" + __version__)
        self.grid()
        self.vezerloValtozok()
        self.widgetekElhelyezese()
        self.adatbazisInicializalasa()
        self._filesession = FileSession()
        # esc-re törli a kiválasztást
        self.bind_all("<Escape>", self.kilepesKivalasztasbol)
        self.bind_all("<Control-s>", self.tetelMentese)
        # első indításkor üres az adatbázis
        if len(self.cikkszamok) > 0:
            # egyébként az első tételt írja ki
            self.tetelKijelzese(self.cikkszamok[0])
            # és bekapcsolja a lapozókat
            self.hatra.config(state = NORMAL)
            self.elore.config(state = NORMAL)
            self.frm_lista.grid(row = 0, column = 3, rowspan = 5, sticky = NW)
            self.listbox.selection_set(0)
            self.bind_all("<Up>", lambda e: self.elozoTetel())
            self.bind_all("<Down>", lambda e: self.kovetkezoTetel())
            self.bind_all("<Prior>",
                          lambda e: self.listbox.yview_scroll(-1, PAGES))
            self.bind_all("<Next>",
                          lambda e: self.listbox.yview_scroll(1, PAGES))
            self.bind_all("<Home>",
                          lambda e: self.tetelKijelzese(self.cikkszamok[0]))
            self.bind_all("<End>",
                          lambda e: self.tetelKijelzese(self.cikkszamok\
                                                    [len(self.cikkszamok) - 1]))

    def vezerloValtozok(self):
        # adott vagy számított értékekhez (label)
        self.cikkszam = StringVar()
        self.keszlet = StringVar()
        self.keszletertek = StringVar()
        self.kivalasztas_erteke = StringVar()
        self.raktarertek = StringVar()
        self.ertek = (self.cikkszam,
                      self.keszlet,
                      self.keszletertek,
                      self.kivalasztas_erteke,
                      self.raktarertek)
        # felhasználó által megadott értékek
        self.megnevezes = StringVar()
        self.becenev = StringVar()
        self.gyarto = StringVar()
        self.leiras = StringVar()
        self.szin = StringVar()
        self.megjegyzes = StringVar()
        self.hely = StringVar()
        self.gyartasido = StringVar()
        self.egyseg = StringVar()
        self.egysegar = StringVar()
        self.valtozas = StringVar()
        self.kiszereles = StringVar()
        self.lejarat = StringVar()
        self.cikkszamok = []  # aktuális kiválasztás cikkszámai
        self.lista = StringVar()  # anyagok listája (listbox-hoz)
        self.szallitolevel = []  # ideiglenes lista szállítólevélhez

    def widgetekElhelyezese(self):
        # előtagok
        frm_elotag = Frame(self)
        frm_elotag.grid(row=0, column=0, rowspan=4, sticky=NW)
        elotag = ("Cikkszám",
                  "Készlet",
                  "Készlet értéke",
                  "Kiválasztás értéke",
                  "Raktár értéke",
                  "Megnevezés",
                  "Becenév",
                  "Gyártó",
                  "Leírás",
                  "Szín",
                  "Megjegyzés",
                  "Hely/projektszám",
                  "Egység",
                  "Egységár",
                  "Kivét/bevét",
                  "Kiszerelés",
                  "Eltarthatóság",
                  "Gyártási idő")
        for elo in elotag:
            Label(frm_elotag, text=elo+":", anchor=W)\
                .grid(row=elotag.index(elo),
                      column=0,
                      sticky=W,
                      padx=PADX,
                      pady=PADY)
        # számított értékek
        frm_cimke = Frame(self)
        frm_cimke.grid(row=0, column=1, sticky=NW)
        for ertek in self.ertek:
            Label(frm_cimke, textvariable=ertek, anchor=E)\
                .grid(row=self.ertek.index(ertek),
                      column=0,
                      sticky=EW,
                      padx=PADX,
                      pady=PADY)
        # utótagok
        Label(frm_cimke, textvariable=self.egyseg, anchor=W)\
            .grid(row=1, column=1, sticky=EW, padx=PADX, pady=PADY)
        Label(frm_cimke, text="Ft", anchor=W)\
            .grid(row=2, column=1, sticky=EW, padx=PADX, pady=PADY)
        Label(frm_cimke, text="Ft", anchor=W)\
            .grid(row=3, column=1, sticky=EW, padx=PADX, pady=PADY)
        Label(frm_cimke, text="Ft", anchor=W)\
            .grid(row=4, column=1, sticky=EW, padx=PADX, pady=PADY)

        # felhasználó által megadott értékek
        frm_hosszu_mezo = Frame(self)
        frm_hosszu_mezo.grid(row=1, column=1, columnspan=2, sticky=NW)
        # megnevezés
        self.megnevezes_bevitel = ttk.Entry(frm_hosszu_mezo,
                                            width=HOSSZU_MEZO,
                                            justify=LEFT,
                                            textvariable=self.megnevezes)
        self.megnevezes_bevitel\
            .grid(row=0, column=0, sticky=W, padx=PADX, pady=PADY)
        self.megnevezes_bevitel.bind("<Return>",\
                            lambda e: self.tetelSzures(self.megnevezes.get()))
        # becenév
        b = ttk.Entry(frm_hosszu_mezo,
                      width=HOSSZU_MEZO,
                      justify=LEFT,
                      textvariable=self.becenev)
        b.grid(row=1, column=0, sticky=W, padx=PADX, pady=PADY)
        b.bind("<Return>", lambda e: self.tetelSzures(self.becenev.get()))
        # gyártó
        b = ttk.Entry(frm_hosszu_mezo,
                      width=HOSSZU_MEZO,
                      justify=LEFT,
                      textvariable=self.gyarto)
        b.grid(row=2, column=0, sticky=W, padx=PADX, pady=PADY)
        b.bind("<Return>", lambda e: self.tetelSzures(self.gyarto.get()))
        # leírás
        b = ttk.Entry(frm_hosszu_mezo,
                      width=HOSSZU_MEZO,
                      justify=LEFT,
                      textvariable=self.leiras)
        b.grid(row=3, column=0, sticky=W, padx=PADX, pady=PADY)
        b.bind("<Return>", lambda e: self.tetelSzures(self.leiras.get()))
        # szín
        b = ttk.Entry(frm_hosszu_mezo,
                      width=HOSSZU_MEZO,
                      justify=LEFT,
                      textvariable=self.szin)
        b.grid(row=4, column=0, sticky=W, padx=PADX, pady=PADY)
        b.bind("<Return>", lambda e: self.tetelSzures(self.szin.get()))
        # megjegyzés
        b = ttk.Entry(frm_hosszu_mezo,
                      width=HOSSZU_MEZO,
                      justify=LEFT,
                      textvariable=self.megjegyzes)
        b.grid(row=5, column=0, sticky=W, padx=PADX, pady=PADY)
        b.bind("<Return>", lambda e: self.tetelSzures(self.megjegyzes.get()))
        # raktári hely vagy projektszám
        b = ttk.Entry(frm_hosszu_mezo,
                      width=KOZEP_MEZO,
                      justify=LEFT,
                      textvariable=self.hely)
        b.grid(row=6, column=0, sticky=W, padx=PADX, pady=PADY)
        b.bind("<Return>", lambda e: self.tetelSzures(self.hely.get()))

        frm_rovid_mezo = Frame(self)
        frm_rovid_mezo.grid(row=2, column=1, sticky=NW)
        # egység
        b = ttk.Entry(frm_rovid_mezo,
                      width=ROVID_MEZO,
                      justify=LEFT,
                      textvariable=self.egyseg)
        b.grid(row=0, column=0, sticky=W, padx=PADX, pady=PADY)
        # egységár
        b = ttk.Entry(frm_rovid_mezo,
                      width=ROVID_MEZO,
                      justify=RIGHT,
                      textvariable=self.egysegar)
        b.grid(row=1, column=0, sticky=W, padx=PADX, pady=PADY)
        # készlet változása
        self.valtozas_bevitel=ttk.Entry(frm_rovid_mezo,
                                        width=ROVID_MEZO,
                                        justify=RIGHT,
                                        textvariable=self.valtozas)
        self.valtozas_bevitel\
            .grid(row=2, column=0, sticky=W, padx=PADX, pady=PADY)
        self.valtozas_bevitel.bind("<Return>", self.keszletValtozasa)
        self.valtozas_bevitel.bind("<KP_Enter>", self.keszletValtozasa)
        # kiszerelés
        b = ttk.Entry(frm_rovid_mezo,
                      width=ROVID_MEZO,
                      justify=RIGHT,
                      textvariable=self.kiszereles)
        b.grid(row=3, column=0, sticky=W, padx=PADX, pady=PADY)
        # eltarthatóság
        b = ttk.Entry(frm_rovid_mezo,
                      width=ROVID_MEZO,
                      justify=RIGHT,
                      textvariable=self.lejarat)
        b.grid(row=5, column=0, sticky=W, padx=PADX, pady=PADY)

        # utótagok
        # egységár
        Label(frm_rovid_mezo, text="Ft /", anchor=W)\
            .grid(row=1, column=1, sticky=W, pady=PADY)
        Label(frm_rovid_mezo, textvariable=self.egyseg, anchor=W)\
            .grid(row=1, column=2, sticky=W, pady=PADY)
        # készlet változása
        Label(frm_rovid_mezo, textvariable=self.egyseg, anchor=W)\
            .grid(row=2, column=1, columnspan=2, sticky=W, pady=PADY)
        # kiszerelés
        Label(frm_rovid_mezo, textvariable=self.egyseg, anchor=W)\
            .grid(row=3, column=1, columnspan=2, sticky=W, pady=PADY)
        # eltarthatóság
        Label(frm_rovid_mezo, text="hónap", anchor=W)\
            .grid(row=5, column=1, columnspan=2, sticky=W, pady=PADY)
        # közepes beviteli mező
        frm_kozep_mezo = Frame(self)
        frm_kozep_mezo.grid(row=3, column=1, sticky=NW)
        # gyártási idő
        b=ttk.Entry(frm_kozep_mezo,
                    width=KOZEP_MEZO,
                    justify=LEFT,
                    textvariable=self.gyartasido)
        b.grid(row=0, column=0, sticky=W, padx=PADX, pady=PADY)
        # utótag
        Label(frm_kozep_mezo, text="(év-hó-nap)", anchor=W)\
            .grid(row=0, column=1, sticky=W, pady=PADY)

        # gombok
        # raktárkezelő
        frm_gomb = LabelFrame(self, text="Készlet-kezelés")
        frm_gomb.grid(row=4, column=0, columnspan=2, sticky=NW)
        ttk.Button(frm_gomb,
                   text="Új",
                   width=GOMB_SZELES,
                   command=self.ujTetel)\
            .grid(row=0, column=0, padx=PADX, pady=PADY)
        ttk.Button(frm_gomb,
                   text="Mentés",
                   width=GOMB_SZELES,
                   command=self.tetelMentese)\
                    .grid(row=0, column=1, padx=PADX, pady=PADY)
        self.hatra = ttk.Button(frm_gomb,
                                text="<<<",
                                width=GOMB_SZELES,
                                command=self.elozoTetel,
                                state=DISABLED)
        self.hatra.grid(row=1, column=0, padx=PADX, pady=PADY)
        self.elore = ttk.Button(frm_gomb,
                                text=">>>",
                                width=GOMB_SZELES,
                                command=self.kovetkezoTetel,
                                state=DISABLED)
        self.elore.grid(row=1, column=1, padx=PADX, pady=PADY)
        ttk.Button(frm_gomb,
                   text="Mutat",
                   width=GOMB_SZELES,
                   command=self.raktarKijelzese)\
                    .grid(row=0, column=2, padx=PADX, pady=PADY)
        ttk.Button(frm_gomb,
                   text="Export",
                   width=GOMB_SZELES,
                   command=self.raktarExport)\
                    .grid(row=1, column=2, padx=PADX, pady=PADY)

        # szállítólevél-kezelő
        frm_gomb2 = LabelFrame(self, text="Szállítólevél")
        frm_gomb2.grid(row=4, column=2, sticky=NW)
        ttk.Button(frm_gomb2,
                   text="Mutat",
                   width=GOMB_SZELES,
                   command=self.szallitoLevelKijelzese)\
                    .grid(row=0, column=0, padx=PADX, pady=PADY)
        ttk.Button(frm_gomb2,
                   text="Új",
                   width=GOMB_SZELES,
                   command=self.uj_szallitolevel)\
                    .grid(row=1, column=0, padx=PADX, pady=PADY)
        ttk.Button(frm_gomb2,
                   text="Export",
                   width=GOMB_SZELES,
                   command=self.szallitoLevelExport)\
                    .grid(row=1, column=1, padx=PADX, pady=PADY)

        # lista megjelenítése
        self.frm_lista = Frame(self)
        v_scroll = Scrollbar(self.frm_lista, orient=VERTICAL)
        v_scroll.grid(row=0, column=1, sticky=N+S)
        self.listbox = Listbox(self.frm_lista,
                               cursor="hand2",
                               font=("DejaVu Sans Mono", "-12"),
                               activestyle="none",
                               listvariable=self.lista,
                               selectmode=SINGLE,
                               width=HOSSZU_MEZO + ROVID_MEZO * 2,
                               height=27,
                               yscrollcommand=v_scroll.set)
        self.listbox.grid(row=0, column=0)
        self.listbox.bind("<<ListboxSelect>>", self.valasztasListabol)
        self.listbox.bind("<Button-4>",
                          lambda e: self.listbox.yview_scroll(-1, UNITS))
        self.listbox.bind("<Button-5>",
                          lambda e: self.listbox.yview_scroll(1, UNITS))
        self.listbox.bind("<MouseWheel>",
                          lambda e: self.listbox.yview_scroll(int(e.delta/120),
                                                              UNITS))
        v_scroll["command"]=self.listbox.yview

        # színjelölő gomb
        ttk.Button(self.frm_lista,
                   text="megjelöl",
                   width=GOMB_SZELES,
                   command=self.megjelol)\
                    .grid(row=1, column=0, padx=PADX, pady=PADY)

    def adatbazisInicializalasa(self):
        self.kapcsolat = sqlite3.connect(ADATBAZIS)
        self.kapcsolat.execute("""
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
            utolso_modositas)
            """)
        self.kapcsolat.execute("""
        CREATE TABLE IF NOT EXISTS raktar_naplo(
            azonosito INTEGER PRIMARY KEY ASC,
            megnevezes,
            egysegar,
            egyseg,
            valtozas,
            datum,
            projektszam)
            """)
        self.kapcsolat.row_factory = sqlite3.Row
        self.kurzor = self.kapcsolat.cursor()
        self.teljesListaKeszitese()

    def kilepesKivalasztasbol(self, _):
        self.teljesListaKeszitese()
        self.tetelKijelzese(self.cikkszamok[0])

    def teljesListaKeszitese(self):
        self.cikkszamok.clear()
        self.kurzor.execute("""
        SELECT *
        FROM raktar
        ORDER BY gyarto, megnevezes;
        """)
        for sor in self.kurzor.fetchall():
            self.cikkszamok.append(sor["cikkszam"])

    def tetelKijelzese(self, cikkszam):
        self.kurzor.execute("""
        SELECT *
        FROM raktar
        WHERE cikkszam = {}
        """.format(cikkszam))
        sor = self.kurzor.fetchone()
        keszlet = float(sor["keszlet"])
        egysegar = sor["egysegar"]
        keszletertek = int(float(keszlet) * egysegar)
        self.cikkszam.set(format(sor["cikkszam"], "0=5"))
        self.keszlet.set(ezresv(format(float(keszlet), ".2f")))
        self.keszletertek.set(ezresv(keszletertek))
        self.kivalasztas_erteke.set(ezresv(self.kivalasztasErteke()))
        self.raktarertek.set(ezresv(self.raktarErtek()))
        self.megnevezes.set(sor["megnevezes"])
        self.becenev.set(sor["becenev"])
        self.gyarto.set(sor["gyarto"])
        self.leiras.set(sor["leiras"])
        self.szin.set(sor["szin"])
        self.megjegyzes.set(sor["megjegyzes"])
        self.egyseg.set(sor["egyseg"])
        self.egysegar.set(ezresv(egysegar))
        self.valtozas.set("")
        self.kiszereles.set(ezresv(sor["kiszereles"]))
        self.hely.set(sor["hely"])
        self.lejarat.set(sor["lejarat"])
        self.gyartasido.set(sor["gyartasido"])
        self.listbox.selection_clear(0, END)  # törli a kijelölést
        self.listaKijelzese()  # kiírja a listát
        # listán is jelöli az aktuális sort
        self.listbox.selection_set(self.cikkszamok.index(cikkszam))
        self.valtozas_bevitel.focus_set()  # fókusz a kivét/bevéten

    def listaKijelzese(self):
        lista = ""
        for cikkszam in self.cikkszamok:
            self.kurzor.execute("""
            SELECT megnevezes, gyarto, keszlet, egyseg
            FROM raktar
            WHERE cikkszam = {}
            """.format(cikkszam))
            sor = self.kurzor.fetchone()
            szokoz = " " if sor["gyarto"] else ""
            egy_sor = "{:<42}{:>8} {}"\
                .format((sor["gyarto"] + szokoz + sor["megnevezes"])[0:40],
                        ezresv(format(float(sor["keszlet"]), ".2f").replace(".", ",")),
                          sor["egyseg"])
            egy_sor = egy_sor.replace(" ", "_")
            lista += (egy_sor + " ")
        self.lista.set(lista)
        for i, cikkszam in enumerate(self.cikkszamok):
            self.kurzor.execute("""
            SELECT jeloles
            FROM raktar
            WHERE cikkszam = {}
            """.format(cikkszam))
            sor = self.kurzor.fetchone()
            if sor["jeloles"]:
                alap, valasztott = sor["jeloles"].split(" ")
                self.listbox.itemconfig(i, bg=alap, selectbackground=valasztott)
            else:
                self.listbox.itemconfig(i, bg="", selectbackground="")

    def kivalasztasErteke(self):
        raktarertek = 0
        for cikkszam in self.cikkszamok:
            self.kurzor.execute("""
            SELECT keszlet, egysegar
            FROM raktar
            WHERE cikkszam = {}
            """.format(cikkszam))
            sor = self.kurzor.fetchone()
            raktarertek += int(float(sor["keszlet"]) * float(sor["egysegar"]))
        return raktarertek

    def raktarErtek(self):
        raktarertek = 0
        self.kurzor.execute("""
        SELECT keszlet, egysegar
        FROM raktar
        """)
        for sor in self.kurzor.fetchall():
            raktarertek += int(float(sor["keszlet"]) * float(sor["egysegar"]))
        return raktarertek

    def elozoTetel(self):
        try:
            cikkszam = int(self.cikkszam.get())
            i = self.cikkszamok.index(cikkszam)
            if i == 0:  # ha az első helyen áll
                cikkszam = self.cikkszamok[-1]
            else:
                cikkszam = self.cikkszamok[i - 1]
        except:
            cikkszam = self.cikkszamok[-1]
        self.tetelKijelzese(cikkszam)

    def kovetkezoTetel(self):
        try:
            cikkszam = int(self.cikkszam.get())
            i = self.cikkszamok.index(cikkszam)
            if i == len(self.cikkszamok) - 1:  # ha az utolsó helyen áll
                cikkszam = self.cikkszamok[0]
            else:
                cikkszam = self.cikkszamok[i + 1]
        except:
            cikkszam = self.cikkszamok[0]
        self.tetelKijelzese(cikkszam)

    def uj_szallitolevel(self) -> None:
        self.szallitolevel.clear()
        messagebox.showinfo(message="Új szállítólevél.")

    def valasztasListabol(self, _):
        valasztas = self.listbox.curselection()
        try:
            self.tetelKijelzese(self.cikkszamok[valasztas[0]])
        except IndexError:
            pass  # még nem jöttem rá, ezt miért dobja

    def keszletValtozasa(self, _):
        # csak meglévőt módosít! új tételt előbb menteni kell
        if self.cikkszam.get():  # ha nincs cikkszám (új tétel), figyelmeztet
            v = self.valtozas.get()
            if v:  # ha üres a bemenet, nem csinál semmit
                try:
                    valtozas = szamot(v)
                except:
                    valtozas = 0
                self.kurzor.execute("""
                SELECT keszlet, megnevezes, egyseg, egysegar
                FROM raktar
                WHERE cikkszam = {}
                """.format(self.cikkszam.get()))
                sor = self.kurzor.fetchone()
                keszlet = float(sor["keszlet"])
                uj_keszlet = valtozas

                mozgas = False  # kivét vagy bevét
                if v.startswith(("-", "+")):
                    # van már a szállítóban azonos tétel?
                    for meglevo in self.szallitolevel:
                        if self.cikkszam.get() == meglevo["cikkszam"]:
                            # ha igen, változik a készlet az adatbázishoz képest
                            keszlet += meglevo["valtozas"]
                    uj_keszlet = keszlet + valtozas
                    mozgas = "Kivét" if v.startswith("-") else "Bevét"
                else:
                    if messagebox\
                        .askokcancel(title=sor["megnevezes"],\
            message="Ez beállít {} {}-t új készletként.\nBiztos vagy benne?"\
                        .format(uj_keszlet, sor["egyseg"])):
                        datumbelyeg = strftime("%Y-%m-%d")
                        self.kapcsolat.execute("""
                        UPDATE raktar
                        SET keszlet = ?, utolso_modositas = ?
                        WHERE cikkszam = ?
                        """, (uj_keszlet, datumbelyeg, self.cikkszam.get()))
                        self.kapcsolat.commit()
                    else:
                        return

                # van ellenkező előjellel ugyanolyan tétel?
                for meglevo in self.szallitolevel:
                    # névazonosságot keres, nem cikkszámot
                    if sor["megnevezes"] == meglevo["megnevezes"] and\
                    valtozas == meglevo["valtozas"] * -1:
                        self.szallitolevel.remove(meglevo)
                        messagebox\
                        .showinfo(title="Törölve a szállítólevélről:",
                            message="{}:\n {} {}".format(sor["megnevezes"],
                                                         valtozas,
                                                         sor["egyseg"]))
                        self.valtozas.set("")
                        return

                # ha érvényes az új készlet, beírja, egyébként figyelmeztet
                if uj_keszlet >= 0:
                    if mozgas:
                        szallito = {}
                        szallito["cikkszam"] = self.cikkszam.get()
                        szallito["megnevezes"] = sor["megnevezes"]
                        szallito["valtozas"] = valtozas
                        szallito["keszlet"] = uj_keszlet
                        szallito["egyseg"] = sor["egyseg"]
                        szallito["egysegar"] = sor["egysegar"]
                        self.szallitolevel.append(szallito)
                        print("{}: {} {} {}".format(mozgas,
                                                    abs(valtozas),
                                                    sor["egyseg"],
                                                    sor["megnevezes"]))
                    self.valtozas.set("")
                else:
                    messagebox.showwarning(title="Készlethiány!",
                                           message="{}: {} {}".\
                                            format(sor["megnevezes"],
                                                   keszlet,
                                                   sor["egyseg"]))
        else:
            messagebox.showerror(title="Hiba!",
                                 message="Előbb hozz létre új tételt!")

    def tetelMentese(self, e=None):
        try:
            valtozas = szamot(self.valtozas.get())
        except:
            valtozas = 0
        try:
            egysegar = szamot(self.egysegar.get())
        except:
            egysegar = 0
        try:
            kiszereles = szamot(self.kiszereles.get())
        except:
            kiszereles = 0
        megnevezes = self.megnevezes.get()
        try:  # ha üres lenne, hibát ad
            # első betű nagy legyen
            megnevezes = megnevezes[0].upper() + megnevezes[1:]
        except:
            pass
        # dátumbélyeg formátuma: 2015-02-27 SQL standard
        datumbelyeg = strftime("%Y-%m-%d")
        # ha van (kijelzett!) cikkszám, csak módosít
        if self.cikkszam.get():
            fajta = "módosítva"
            self.kapcsolat.execute("""
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
                utolso_modositas = ?
            WHERE cikkszam = ?
            """, (megnevezes,
                  self.becenev.get(),
                  self.gyarto.get(),
                  self.leiras.get(),
                  self.szin.get(),
                  self.megjegyzes.get(),
                  self.egyseg.get(),
                  egysegar,
                  kiszereles,
                  self.hely.get(),
                  self.lejarat.get(),
                  self.gyartasido.get(),
                  datumbelyeg,
                  self.cikkszam.get()))
            self.kapcsolat.commit()
            # módosításkor előfordul, hogy a készlet is változik
            self.keszletValtozasa(1)
        # ha nincs, egy új bejegyzés, készlet-változás lesz a kiinduló készlet
        else:
            fajta = "mentve, mint új tétel"
            if valtozas < 0:
                valtozas = 0
            self.kapcsolat.execute("""
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
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (valtozas,
                  megnevezes,
                  self.becenev.get(),
                  self.gyarto.get(),
                  self.leiras.get(),
                  self.szin.get(),
                  self.megjegyzes.get(),
                  self.egyseg.get(),
                  egysegar,
                  kiszereles,
                  self.hely.get(),
                  self.lejarat.get(),
                  self.gyartasido.get(),
                  datumbelyeg,
                  datumbelyeg))
            self.hatra.config(state=NORMAL)  # első indításnál bekapcsol
            self.elore.config(state=NORMAL)
            self.frm_lista.grid(row=0, column=3, rowspan=5, sticky=NW)
            self.kapcsolat.commit()
            self.teljesListaKeszitese()
            self.listaKijelzese()
            # utolsó mentett elem előkerítése
            self.tetelKijelzese(self.kurzor.execute("""
            SELECT last_insert_rowid()
            """).fetchone()[0])
        print("{} {}.".format(megnevezes, fajta))

    def ujTetel(self):
        self.cikkszamok.clear()
        self.kurzor.execute("SELECT cikkszam FROM raktar")
        for sor in self.kurzor.fetchall():
            self.cikkszamok.append(sor["cikkszam"])
        self.cikkszam.set("")
        self.megnevezes_bevitel.focus()

    def tetelSzures(self, szuro):
        print("Szűrés a {} kifejezésre.".format(szuro))
        szuro = szuro.lower()
        self.cikkszamok.clear()
        self.kurzor.execute("""
        SELECT cikkszam,
                megnevezes,
                becenev,
                gyarto,
                leiras,
                szin,
                megjegyzes,
                hely
        FROM raktar
        ORDER BY gyarto, megnevezes
        """)
        for sor in self.kurzor.fetchall():
            if szuro in sor["megnevezes"].lower() or \
                szuro in sor["becenev"].lower() or \
                    szuro in sor["gyarto"].lower() or \
                        szuro in sor["leiras"].lower() or \
                            szuro in sor["szin"] or \
                                szuro in sor["megjegyzes"].lower() or \
                                    szuro in sor["hely"].lower():
                self.cikkszamok.append(sor["cikkszam"])
                print(".", end="")
        print()
        if len(self.cikkszamok) == 0:  # ha nincs találat
            self.teljesListaKeszitese()
        self.tetelKijelzese(self.cikkszamok[0])

    def megjelol(self):
        valasztas = self.listbox.curselection()
        hatterszin = self.listbox.itemcget(valasztas[0], "background")
        if hatterszin in JELOLOSZIN:
            self.kurzor.execute("""
            UPDATE raktar
            SET jeloles = ?
            WHERE cikkszam = ?
            """, ("", self.cikkszamok[valasztas[0]]))
        else:
            self.kurzor.execute("""
            UPDATE raktar SET jeloles = ? WHERE cikkszam = ?
            """, (JELOLOSZIN[0] + " " + JELOLOSZIN[1],
                  self.cikkszamok[valasztas[0]]))
        self.kapcsolat.commit()
        self.tetelKijelzese(self.cikkszamok[valasztas[0]])

    def show_stock(self) -> str:
        result = ""
        result += Rep.cimsor("raktárkészlet")
        result += Rep.fejlec(sorszám=8,
                             megnevezés=33,
                             készlet=14,
                             egységár=16,
                             érték=9)
        result += Rep.stock2str(self.kurzor, self.cikkszamok)
        result += Rep.vonal()
        result += "Kiválasztás értéke összesen:                            \
         {:>12} Ft\n".format(ezresv(self.kivalasztasErteke()))
        result += Rep.vonal()
        result += "{}-i állapot.\n".format(strftime("%Y.%m.%d"))
        return result

    def raktarKijelzese(self):
        print(self.show_stock())

    def raktarExport(self) -> None:
        filename = "raktar_" + strftime("%Y%m%d")
        self._filesession.export(filename, self.show_stock(), False)
        messagebox.showinfo(message="Raktárkészlet exportálva.")

    def show_waybill(self) -> str:
        result = Rep.cimsor("szállítólevél")
        result += Rep.fejlec(sorszám=9, megnevezés=54, mennyiség=10, egység=7)
        result += Rep.waybill2str(self.szallitolevel)
        result += Rep.vonal()
        return result

    def szallitoLevelKijelzese(self):
        print(self.show_waybill())

    def szallitoLevelExport(self):
        if not self.szallitolevel:
            messagebox.showerror(title="Hiba!",
                                 message="Üres a szállítólevél!")
            return
        while True:
            projektszam = askstring("Költséghely",
                                    "Kérek egy projektszámot:",
                                    initialvalue=self.hely.get())
            if not projektszam:
                return
            if not valid_projectnr(projektszam):
                messagebox.showerror(title="Hiba!",
                                     message="Nem megfelelő projektszám!")
                continue
            break
        filenev = self.szallitolevel_fileneve(projektszam)
        projektszam = fmt_projectnr(projektszam)
        sorszam = 1
        datumbelyeg = strftime("%Y-%m-%d")
        datumbelyeg_kijelzo = strftime("%Y.%m.%d.")
        dirfilenev = EXPORTFOLDER + filenev + ".txt"
        f = open(dirfilenev, "w")
        f.write(Rep.cimsor(szoveg="szállítólevél"))
        f.write("{:>79}".format("száma: {}\n".format(filenev)))
        f.write("\nSzállító:                                Vevő:")
        for sor in zip(SZERVEZET, VEVO):
            f.write("\n{:<41}{}".format(sor[0], sor[1]))
        f.write("\n\n")
        f.write(Rep.fejlec(sorszám=9, megnevezés=54, mennyiség=10, egység=7))
        for sor in self.szallitolevel:
            self.kapcsolat.execute("""
            INSERT INTO raktar_naplo(
                megnevezes,
                egysegar,
                egyseg,
                valtozas,
                datum,
                projektszam)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (sor["megnevezes"],
                  sor["egysegar"],
                  sor["egyseg"],
                  sor["valtozas"],
                  datumbelyeg,
                  projektszam))
            self.kapcsolat.execute("""
            UPDATE raktar
            SET keszlet = ?, utolso_modositas = ? WHERE cikkszam = ?
            """, (float(sor["keszlet"]), datumbelyeg, sor["cikkszam"]))
            f.write("{:>6}   {:<50} {:>12} {}\n"\
                    .format(format(sorszam, "0=5"),
                            sor["megnevezes"][0:49],
                            ezresv(format(abs(sor["valtozas"]), ".2f")),
                            sor["egyseg"]))
            sorszam += 1
        self.kapcsolat.commit()
        f.write(Rep.vonal())
        f.write("\nKelt: Herend, {}\n".format(datumbelyeg_kijelzo))

        f.write("\n\n\n\n")
        f.write("             ___________________          ___________________\n")
        f.write("               Hartmann Zoltán\n")
        f.write("                 kiállította                   átvette\n")
        f.close()
        self.szallitolevel.clear()
        messagebox.showinfo(title=projektszam,
                            message="Szállítólevél exportálva.")
        self.tetelKijelzese(int(self.cikkszam.get()))


    def kovetkezo_szallitolevel_szama(self, projektszam: str) -> int:
        """A szállítólevél száma néz ki: 23_076_2.
        Kell egy query az adatbázisból, hány darab azonos projektszámmal kezdődő
        szállítólevél van eddig."""
        osszes = self.kapcsolat.execute(f"""
        SELECT COUNT(DISTINCT projektszam)
        FROM raktar_naplo
        WHERE projektszam = "{fmt_projectnr(projektszam)}";
        """)
        return osszes.fetchone()[0] + 1


    def szallitolevel_fileneve(self, projektszam: str) -> str:
        return "{}_{}".format(fmt_projectnr(projektszam),
                              self.kovetkezo_szallitolevel_szama(projektszam))


def foProgram():
    raktar = RaktarKeszlet()
    raktar.mainloop()


if __name__ == "__main__":
    foProgram()


