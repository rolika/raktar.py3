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
from time import strftime #időbélyeghez
import sqlite3
import os #ikon miatti különbség kezeléséhez
from szam_megjelenites import *

PROGRAM = 'Készlet-nyilvántartó'
VERZIO = '027'
WINDOWS_IKON = 'wevik.ico'
LINUX_IKON = 'wevik.gif'
ADATBAZIS = 'adatok.db'
SZERVEZET = 'Wevik Engineer Kft.\n8445-Városlőd\nPille utca 56.'

#grid-jellemzők
HOSSZU_MEZO = 42
KOZEP_MEZO = 12
ROVID_MEZO = 8
GOMB_SZELES = 8
PADX = 2
PADY = 2

def foProgram():
    raktar = RaktarKeszlet()
    raktar.mainloop()

class RaktarKeszlet(Frame):
    def __init__(self, root = None):
        Frame.__init__(self, root)
        if os.name == 'posix':
            ikon = PhotoImage(file = LINUX_IKON)
            self.master.tk.call('wm', 'iconphoto', self.master._w, ikon)
        else:
            self.master.iconbitmap(default = WINDOWS_IKON)
        self.master.title(PROGRAM + " v" + VERZIO)
        self.grid()
        self.vezerloValtozok()
        self.widgetekElhelyezese()
        self.adatbazisInicializalasa()
        self.bind_all('<Escape>', self.kilepesKivalasztasbol) #esc-re törli a kiválasztást
        if len(self.cikkszamok) > 0: #első indításkor üres az adatbázis
            self.tetelKijelzese(self.cikkszamok[0]) #egyébként az első tételt írja ki
            self.hatra.config(state = NORMAL) #és bekapcsolja a lapozókat
            self.elore.config(state = NORMAL)
            self.frm_lista.grid(row = 0, column = 3, rowspan = 5, sticky = NW)
            self.listbox.selection_set(0)
            self.bind_all('<Up>', lambda e: self.elozoTetel())
            self.bind_all('<Down>', lambda e: self.kovetkezoTetel())
            self.bind_all('<Prior>', lambda e: self.listbox.yview_scroll(-1, PAGES))
            self.bind_all('<Next>', lambda e: self.listbox.yview_scroll(1, PAGES))
            self.bind_all('<Home>', lambda e: self.tetelKijelzese(self.cikkszamok[0]))
            self.bind_all('<End>', lambda e: self.tetelKijelzese(self.cikkszamok[len(self.cikkszamok) - 1]))

    def vezerloValtozok(self):
        self.cikkszam, self.keszlet, self.keszletertek, self.kivalasztas_erteke, self.raktarertek = StringVar(), StringVar(), StringVar(), StringVar(), StringVar() #adott vagy számított értékekhez (label)
        self.ertek = (self.cikkszam, self.keszlet, self.keszletertek, self.kivalasztas_erteke, self.raktarertek)
        self.megnevezes, self.gyarto, self.leiras, self.megjegyzes, self.hely = StringVar(), StringVar(), StringVar(), StringVar(), StringVar() #felhasználó által megadott értékek - hosszú mezők (entry)
        self.gyartasido = StringVar() #felhasználó által megadott értékek - közép mezők (entry)
        self.egyseg, self.egysegar, self.valtozas, self.kiszereles, self.lejarat = StringVar(), StringVar(), StringVar(), StringVar(), StringVar() #felhasználó által megadott értékek - rövid mezők (entry)
        self.cikkszamok = [] #aktuális kiválasztás cikkszámai
        self.lista = StringVar() #anyagok listája (listbox-hoz)
        self.szallitolevel = [] #ideiglenes lista szállítólevélhez

    def widgetekElhelyezese(self):
        #előtagok
        frm_elotag = Frame(self)
        frm_elotag.grid(row = 0, column = 0, rowspan = 4, sticky = NW)
        elotag = ('Cikkszám', 'Készlet', 'Készlet értéke', 'Kiválasztás értéke', 'Raktár értéke', 'Megnevezés', 'Gyártó', 'Leiras', 'Megjegyzés', 'Hely/cél', 'Egység', 'Egységár', 'Készlet-változás', 'Kiszerelés', 'Eltarthatóság', 'Gyártási idő')
        for elo in elotag:
            Label(frm_elotag, text = elo + ':', anchor = W).grid(row = elotag.index(elo), column = 0, sticky = W, padx = PADX, pady = PADY)
        #számított értékek
        frm_cimke = Frame(self)
        frm_cimke.grid(row = 0, column = 1, sticky = NW)
        for ertek in self.ertek:
            Label(frm_cimke, textvariable = ertek, anchor = E).grid(row = self.ertek.index(ertek), column = 0, sticky = EW, padx = PADX, pady = PADY)
        ##utótagok
        Label(frm_cimke, textvariable = self.egyseg, anchor = W).grid(row = 1, column = 1, sticky = EW, padx = PADX, pady = PADY)
        Label(frm_cimke, text = "Ft", anchor = W).grid(row = 2, column = 1, sticky = EW, padx = PADX, pady = PADY)
        Label(frm_cimke, text = "Ft", anchor = W).grid(row = 3, column = 1, sticky = EW, padx = PADX, pady = PADY)
        Label(frm_cimke, text = "Ft", anchor = W).grid(row = 4, column = 1, sticky = EW, padx = PADX, pady = PADY)
        #felhasználó által megadott értékek
        ##hosszú beviteli mezők
        frm_hosszu_mezo = Frame(self)
        frm_hosszu_mezo.grid(row = 1, column = 1, columnspan = 2, sticky = NW)
        ###megnevezés
        self.megnevezes_bevitel = ttk.Entry(frm_hosszu_mezo, width = HOSSZU_MEZO, justify = LEFT, textvariable = self.megnevezes)
        self.megnevezes_bevitel.grid(row = 0, column = 0, sticky = W, padx = PADX, pady = PADY)
        self.megnevezes_bevitel.bind('<Return>', lambda e: self.tetelSzures(self.megnevezes.get()))
        ###gyártó
        b = ttk.Entry(frm_hosszu_mezo, width = HOSSZU_MEZO, justify = LEFT, textvariable = self.gyarto)
        b.grid(row = 1, column = 0, sticky = W, padx = PADX, pady = PADY)
        b.bind('<Return>', lambda e: self.tetelSzures(self.gyarto.get()))
        ###típus
        b = ttk.Entry(frm_hosszu_mezo, width = HOSSZU_MEZO, justify = LEFT, textvariable = self.leiras)
        b.grid(row = 2, column = 0, sticky = W, padx = PADX, pady = PADY)
        b.bind('<Return>', lambda e: self.tetelSzures(self.leiras.get()))
        ###megjegyzés
        b = ttk.Entry(frm_hosszu_mezo, width = HOSSZU_MEZO, justify = LEFT, textvariable = self.megjegyzes)
        b.grid(row = 3, column = 0, sticky = W, padx = PADX, pady = PADY)
        b.bind('<Return>', lambda e: self.tetelSzures(self.megjegyzes.get()))
        ###raktári hely
        b = ttk.Entry(frm_hosszu_mezo, width = HOSSZU_MEZO, justify = LEFT, textvariable = self.hely)
        b.grid(row = 4, column = 0, sticky = W, padx = PADX, pady = PADY)
        b.bind('<Return>', lambda e: self.tetelSzures(self.hely.get()))
        ##rövid beviteli mezők
        frm_rovid_mezo = Frame(self)
        frm_rovid_mezo.grid(row = 2, column = 1, sticky = NW)
        ###egység
        b = ttk.Entry(frm_rovid_mezo, width = ROVID_MEZO, justify = LEFT, textvariable = self.egyseg)
        b.grid(row = 0, column = 0, sticky = W, padx = PADX, pady = PADY)
        ###egységár
        b = ttk.Entry(frm_rovid_mezo, width = ROVID_MEZO, justify = RIGHT, textvariable = self.egysegar)
        b.grid(row = 1, column = 0, sticky = W, padx = PADX, pady = PADY)
        ###készlet változása
        self.valtozas_bevitel = ttk.Entry(frm_rovid_mezo, width = ROVID_MEZO, justify = RIGHT, textvariable = self.valtozas)
        self.valtozas_bevitel.grid(row = 2, column = 0, sticky = W, padx = PADX, pady = PADY)
        self.valtozas_bevitel.bind('<Return>', self.keszletValtozasa)
        self.valtozas_bevitel.bind('<KP_Enter>', self.keszletValtozasa)
        ###kiszerelés
        b = ttk.Entry(frm_rovid_mezo, width = ROVID_MEZO, justify = RIGHT, textvariable = self.kiszereles)
        b.grid(row = 3, column = 0, sticky = W, padx = PADX, pady = PADY)
        ###eltarthatóság
        b = ttk.Entry(frm_rovid_mezo, width = ROVID_MEZO, justify = RIGHT, textvariable = self.lejarat)
        b.grid(row = 5, column = 0, sticky = W, padx = PADX, pady = PADY)
        ##utótagok
        ###egységár
        Label(frm_rovid_mezo, text = "Ft /", anchor = W).grid(row = 1, column = 1, sticky = W, pady = PADY)
        Label(frm_rovid_mezo, textvariable = self.egyseg, anchor = W).grid(row = 1, column = 2, sticky = W, pady = PADY)
        ###készlet változása
        Label(frm_rovid_mezo, textvariable = self.egyseg, anchor = W).grid(row = 2, column = 1, columnspan = 2, sticky = W, pady = PADY)
        ###kiszerelés
        Label(frm_rovid_mezo, textvariable = self.egyseg, anchor = W).grid(row = 3, column = 1, columnspan = 2, sticky = W, pady = PADY)
        ###eltarthatóság
        Label(frm_rovid_mezo, text = 'hónap', anchor = W).grid(row = 5, column = 1, columnspan = 2, sticky = W, pady = PADY)
        ##közepes beviteli mező
        frm_kozep_mezo = Frame(self)
        frm_kozep_mezo.grid(row = 3, column = 1, sticky = NW)
        ###gyártási idő
        b = ttk.Entry(frm_kozep_mezo, width = KOZEP_MEZO, justify = LEFT, textvariable = self.gyartasido)
        b.grid(row = 0, column = 0, sticky = W, padx = PADX, pady = PADY)
        ###utótag
        Label(frm_kozep_mezo, text = '(év-hó-nap)', anchor = W).grid(row = 0, column = 1, sticky = W, pady = PADY)
        #gombok
        ##tétel-kezelő
        frm_gomb = LabelFrame(self, text = 'Készlet-kezelés')
        frm_gomb.grid(row = 4, column = 0, columnspan = 2, sticky = NW)
        ttk.Button(frm_gomb, text = 'Új', width = GOMB_SZELES, command = self.ujTetel).grid(row = 0, column = 0, padx = PADX, pady = PADY)
        ttk.Button(frm_gomb, text = 'Mentés', width = GOMB_SZELES, command = self.tetelMentese).grid(row = 0, column = 1, padx = PADX, pady = PADY)
        self.hatra = ttk.Button(frm_gomb, text = '<<<', width = GOMB_SZELES, command = self.elozoTetel, state = DISABLED)
        self.hatra.grid(row = 1, column = 0, padx = PADX, pady = PADY)
        self.elore = ttk.Button(frm_gomb, text = '>>>', width = GOMB_SZELES, command = self.kovetkezoTetel, state = DISABLED)
        self.elore.grid(row = 1, column = 1, padx = PADX, pady = PADY)
        ttk.Button(frm_gomb, text = 'Mutat', width = GOMB_SZELES, command = self.raktarKijelzese).grid(row = 0, column = 2, padx = PADX, pady = PADY)
        ttk.Button(frm_gomb, text = 'Export', width = GOMB_SZELES, command = self.raktarExport).grid(row = 1, column = 2, padx = PADX, pady = PADY)
        ##szállítólevél-kezelő
        frm_gomb2 = LabelFrame(self, text = 'Szállítólevél')
        frm_gomb2.grid(row = 4, column = 2, sticky = NW)
        ttk.Button(frm_gomb2, text = 'Mutat', width = GOMB_SZELES, command = self.szallitoLevelKijelzese).grid(row = 0, column = 0, padx = PADX, pady = PADY)
        ttk.Button(frm_gomb2, text = 'Töröl', width = GOMB_SZELES, command = self.szallitolevel.clear).grid(row = 1, column = 0, padx = PADX, pady = PADY)
        ttk.Button(frm_gomb2, text = 'Export', width = GOMB_SZELES, command = self.szallitoLevelExport).grid(row = 1, column = 1, padx = PADX, pady = PADY)
        #lista megjelenítése
        self.frm_lista = Frame(self)
        v_scroll = Scrollbar(self.frm_lista, orient = VERTICAL)
        v_scroll.grid(row = 0, column = 1, sticky = N + S)
        self.listbox = Listbox(self.frm_lista, cursor = 'hand2', font = ('DejaVu Sans Mono', '-12'), activestyle = 'none', listvariable = self.lista, selectmode = SINGLE, width = HOSSZU_MEZO + ROVID_MEZO * 2, height = 27, yscrollcommand = v_scroll.set)
        self.listbox.grid(row = 0, column = 0)
        self.listbox.bind('<<ListboxSelect>>', self.valasztasListabol)
        self.listbox.bind('<Button-4>', lambda e: self.listbox.yview_scroll(-1, UNITS))
        self.listbox.bind('<Button-5>', lambda e: self.listbox.yview_scroll(1, UNITS))
        self.listbox.bind('<MouseWheel>', lambda event: self.listbox.yview_scroll(int(event.delta / 120), UNITS))
        v_scroll['command'] = self.listbox.yview

    def adatbazisInicializalasa(self):
        self.kapcsolat = sqlite3.connect(ADATBAZIS)
        self.kapcsolat.execute('CREATE TABLE IF NOT EXISTS raktar(cikkszam INTEGER PRIMARY KEY ASC, keszlet, megnevezes, gyarto, leiras, megjegyzes, egyseg, egysegar, kiszereles, hely, lejarat, gyartasido, letrehozas, utolso_modositas)')
        self.kapcsolat.execute('CREATE TABLE IF NOT EXISTS raktar_naplo(cikkszam INTEGER PRIMARY KEY ASC, megnevezes, egyseg, egysegar, valtozas, datum, projektszam)')
        self.kapcsolat.row_factory = sqlite3.Row
        self.kurzor = self.kapcsolat.cursor()
        self.teljesListaKeszitese()

    def kilepesKivalasztasbol(self, event):
        self.teljesListaKeszitese()
        self.tetelKijelzese(self.cikkszamok[0])

    def teljesListaKeszitese(self):
        self.cikkszamok.clear()
        self.kurzor.execute('SELECT * FROM raktar ORDER BY megnevezes')
        for sor in self.kurzor.fetchall():
            self.cikkszamok.append(sor['cikkszam'])

    def tetelKijelzese(self, cikkszam):
        self.kurzor.execute('SELECT * FROM raktar WHERE cikkszam = {}'.format(cikkszam))
        sor = self.kurzor.fetchone()
        keszlet = sor['keszlet']
        egysegar = sor['egysegar']
        keszletertek = int(keszlet * egysegar)
        self.cikkszam.set(format(sor['cikkszam'], '0=5'))
        self.keszlet.set(ezresv(format(keszlet, '.2f')))
        self.keszletertek.set(ezresv(keszletertek))
        self.kivalasztas_erteke.set(ezresv(self.kivalasztasErteke()))
        self.raktarertek.set(ezresv(self.raktarErtek()))
        self.megnevezes.set(sor['megnevezes'])
        self.gyarto.set(sor['gyarto'])
        self.leiras.set(sor['leiras'])
        self.megjegyzes.set(sor['megjegyzes'])
        self.egyseg.set(sor['egyseg'])
        self.egysegar.set(ezresv(egysegar))
        self.valtozas.set('')
        self.kiszereles.set(ezresv(sor['kiszereles']))
        self.hely.set(sor['hely'])
        self.lejarat.set(sor['lejarat'])
        self.gyartasido.set(sor['gyartasido'])
        self.valtozas_bevitel.focus()
        self.listbox.selection_clear(0, END) #törli a kijelölést
        self.listaKijelzese() #kiírja a listát
        self.listbox.selection_set(self.cikkszamok.index(cikkszam)) #listán is jelöli az aktuális sort

    def listaKijelzese(self):
        lista = ''
        for cikkszam in self.cikkszamok:
            self.kurzor.execute('SELECT megnevezes, keszlet, egyseg FROM raktar WHERE cikkszam = {}'.format(cikkszam))
            sor = self.kurzor.fetchone()
            egy_sor = '{:<42}{:>8} {}'.format(sor['megnevezes'][0:40], ezresv(format(sor['keszlet'], '.2f').replace('.', ',')), sor['egyseg'])
            egy_sor = egy_sor.replace(' ', '_')
            lista += (egy_sor + ' ')
        self.lista.set(lista)

    def kivalasztasErteke(self):
        raktarertek = 0
        for cikkszam in self.cikkszamok:
            self.kurzor.execute('SELECT keszlet, egysegar FROM raktar WHERE cikkszam = {}'.format(cikkszam))
            sor = self.kurzor.fetchone()
            raktarertek += int(sor['keszlet'] * sor['egysegar'])
        return raktarertek

    def raktarErtek(self):
        raktarertek = 0
        self.kurzor.execute('SELECT keszlet, egysegar FROM raktar')
        for sor in self.kurzor.fetchall():
            raktarertek += int(sor['keszlet'] * sor['egysegar'])
        return raktarertek

    def elozoTetel(self):
        try:
            cikkszam = int(self.cikkszam.get())
            i = self.cikkszamok.index(cikkszam)
            if i == 0: #ha az első helyen áll
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
            if i == len(self.cikkszamok) - 1: #ha az utolsó helyen áll
                cikkszam = self.cikkszamok[0]
            else:
                cikkszam = self.cikkszamok[i + 1]
        except:
            cikkszam = self.cikkszamok[0]
        self.tetelKijelzese(cikkszam)

    def valasztasListabol(self, event):
        valasztas = self.listbox.curselection()
        self.tetelKijelzese(self.cikkszamok[valasztas[0]])

    def keszletValtozasa(self, event):
         #csak meglévőt módosít! új tételt előbb menteni kell
        if self.cikkszam.get(): #ha nincs cikkszám (új tétel), nem csinál semmit
            v = self.valtozas.get()
            if v: #ha üres a bemenet, nem csinál semmit
                try:
                    valtozas = szamot(v)
                except:
                    valtozas = 0
                try:
                    egysegar = szamot(self.egysegar.get())
                except:
                    egysegar = 0
                datumbelyeg = strftime('%Y-%m-%d')
                self.kurzor.execute('SELECT keszlet FROM raktar WHERE cikkszam = {}'.format(self.cikkszam.get()))
                sor = self.kurzor.fetchone()
                keszlet = sor['keszlet']
                uj_keszlet = valtozas
                szallito = False #szállítólevélbe kerül, vagy sem
                if v.startswith(('-', '+')):
                    uj_keszlet = keszlet + valtozas
                    szallitolevel = True
                if uj_keszlet >= 0: #ha érvényes az új készlet, beírja, egyébként nem történik semmi
                    self.kapcsolat.execute('INSERT INTO raktar_naplo(megnevezes, egyseg, egysegar, valtozas, datum, projektszam) VALUES (?, ?, ?, ?, ?, ?)', (self.megnevezes.get(), self.egyseg.get(), egysegar, valtozas, datumbelyeg, self.hely.get())) #csak a +- változást menti
                    self.kapcsolat.execute('UPDATE raktar SET keszlet = ?, utolso_modositas = ? WHERE cikkszam = ?', (uj_keszlet, datumbelyeg, self.cikkszam.get()))
                    self.kapcsolat.commit()
                    if szallitolevel:
                        szallito = {}
                        szallito['megnevezes'] = self.megnevezes.get()
                        szallito['mennyiseg'] = valtozas
                        szallito['egyseg'] = self.egyseg.get()
                        self.szallitolevel.append(szallito)
                    self.tetelKijelzese(int(self.cikkszam.get()))

    def tetelMentese(self):
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
        try: #ha üres lenne, hibát ad
            megnevezes = megnevezes[0].upper() + megnevezes[1:] #első betű nagy legyen
        except:
            pass
        datumbelyeg = strftime('%Y-%m-%d') #dátumbélyeg formátuma: 2015-02-27 SQL standard
        if self.cikkszam.get(): #ha van (kijelzett!) cikkszám, csak módosít
            self.kapcsolat.execute('UPDATE raktar SET megnevezes = ?, gyarto = ?, leiras = ?, megjegyzes = ?, egyseg = ?, egysegar = ?, kiszereles = ?, hely = ?, lejarat = ?, gyartasido = ?, utolso_modositas = ? WHERE cikkszam = ?', (megnevezes, self.gyarto.get(), self.leiras.get(), self.megjegyzes.get(), self.egyseg.get(), egysegar, kiszereles, self.hely.get(), self.lejarat.get(), self.gyartasido.get(), datumbelyeg, self.cikkszam.get()))
            self.kapcsolat.commit()
            self.keszletValtozasa(1) #módosításkor előfordul, hogy a készlet is változik
        else: #ha nincs cikkszám, készít egy új bejegyzést, készlet-változás lesz a kiinduló készlet
            if valtozas < 0:
                valtozas = 0
            self.kapcsolat.execute('INSERT INTO raktar(keszlet, megnevezes, gyarto, leiras, megjegyzes, egyseg, egysegar, kiszereles, hely, lejarat, gyartasido, letrehozas, utolso_modositas) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (valtozas, megnevezes, self.gyarto.get(), self.leiras.get(), self.megjegyzes.get(), self.egyseg.get(), egysegar, kiszereles, self.hely.get(), self.lejarat.get(), self.gyartasido.get(), datumbelyeg, datumbelyeg))
            self.hatra.config(state = NORMAL) #első indításnál bekapcsol
            self.elore.config(state = NORMAL)
            self.frm_lista.grid(row = 0, column = 3, rowspan = 5, sticky = NW)
            self.kapcsolat.commit()
            self.teljesListaKeszitese()
            self.listaKijelzese()
            self.tetelKijelzese(self.kurzor.execute('SELECT last_insert_rowid()').fetchone()[0]) #utolsó mentett elem előkerítése

    def ujTetel(self):
        self.cikkszamok.clear()
        self.kurzor.execute('SELECT cikkszam FROM raktar')
        for sor in self.kurzor.fetchall():
            self.cikkszamok.append(sor['cikkszam'])
        self.cikkszam.set('')
        self.megnevezes_bevitel.focus()

    def tetelSzures(self, szuro):
        szuro = szuro.lower()
        self.cikkszamok.clear()
        self.kurzor.execute('SELECT cikkszam, megnevezes, gyarto, leiras, megjegyzes, hely FROM raktar ORDER BY megnevezes')
        for sor in self.kurzor.fetchall():
            if szuro in sor['megnevezes'].lower() or szuro in sor['gyarto'].lower() or szuro in sor['leiras'].lower() or szuro in sor['megjegyzes'].lower() or szuro in sor['hely'].lower():
                self.cikkszamok.append(sor['cikkszam'])
        if len(self.cikkszamok) == 0: #ha nincs találat
            self.teljesListaKeszitese()
        self.tetelKijelzese(self.cikkszamok[0])

    def raktarKijelzese(self):
        sorszam = 1
        print('{:_^79}'.format('R A K T Á R'))
        print('\nSorszám_Megnevezés_______________________Készlet_______Egységár________Érték___\n')
        for cikkszam in self.cikkszamok:
            self.kurzor.execute('SELECT megnevezes, keszlet, egyseg, egysegar FROM raktar WHERE cikkszam = {}'.format(cikkszam))
            sor = self.kurzor.fetchone()
            if sor['keszlet']:
                print('{:>6}  {:<28} {:>8} {} {:>9} Ft/{} {:>11} Ft'.format(format(sorszam, '0=5'), sor['megnevezes'][0:28], ezresv(format(sor['keszlet'], '.2f')), sor['egyseg'], ezresv(sor['egysegar']), sor['egyseg'], ezresv(int(sor['keszlet'] * sor['egysegar']))))
                sorszam += 1
        print('_______________________________________________________________________________')
        print('Kiválasztás értéke összesen:                                    {:>12} Ft'.format(ezresv(self.kivalasztasErteke())))

    def valtozasKijelzese(self):
        sorszam = 1
        print('{:_^79}'.format('R A K T Á R N A P L Ó'))
        print('\nSorszám__Megnevezés_______________________Készlet______Egységár________Érték___\n')
        projekt = self.hely.get()
        idoszak = self.lejarat.get()
        szuro = ''
        for sor in self.kurzor.execute('SELECT * FROM raktar_naplo {} ORDER BY datum'.format(szuro)):
            print('{:>6}   {:<28} {:>8} {} {:>8} Ft/{} {:>11} Ft'.format(format(sorszam, '0=5'), sor['megnevezes'][0:28], ezresv(format(sor['valtozas'], '.2f')), sor['egyseg'], ezresv(sor['egysegar']), sor['egyseg'], ezresv(int(sor['valtozas'] * sor['egysegar']))))
            sorszam += 1
        print('_______________________________________________________________________________')

    def szallitoLevelKijelzese(self):
        sorszam = 1
        print('{:_^79}'.format('S Z Á L L Í T Ó L E V É L'))
        print('\nSorszám__Megnevezés____________________________________________Mennyiség_Egység\n')
        for sor in self.szallitolevel:
            print('{:>6}   {:<50} {:>12} {}'.format(format(sorszam, '0=5'), sor['megnevezes'][0:49], ezresv(format(abs(sor['mennyiseg']), '.2f')), sor['egyseg']))
            sorszam += 1
        print('_______________________________________________________________________________')

    def szallitoLevelExport(self):
        sorszam = 1
        datumbelyeg_file = strftime('%Y%m%d%H%M%S')
        datumbelyeg_kijelzo = strftime('%Y.%m.%d.')
        f = open('szallito{}.txt'.format(datumbelyeg_file),'w')
        f.write('\n{:_^79}\n'.format('S Z Á L L Í T Ó L E V É L'))
        f.write('{:>79}'.format('száma: {}{}\n'.format(SZERVEZET[0], datumbelyeg_file)))        
        szallito = SZERVEZET.split('\n')
        vevo = self.hely.get()
        vevo = vevo.split('\\')
        l = len(vevo)
        if l < 3: #hogy mindenképpen kiírja legalább a szállítót
            for i in range(3 - l):
                vevo.append("")        
        f.write('\nSzállító:________________________________Vevő:_________________________________')
        for sor in zip(szallito, vevo):
            f.write('\n{:<41}{}'.format(sor[0], sor[1]))        
        f.write('\n\nSorszám__Megnevezés____________________________________________Mennyiség_Egység\n\n')
        for sor in self.szallitolevel:
            f.write('{:>6}   {:<50} {:>12} {}\n'.format(format(sorszam, '0=5'), sor['megnevezes'][0:49], ezresv(format(abs(sor['mennyiseg']), '.2f')), sor['egyseg']))
            sorszam += 1
        f.write('_______________________________________________________________________________\n')
        f.write('\nKelt: Herend, {}\n'.format(datumbelyeg_kijelzo))
        
        f.write('\n\n\n\n')
        f.write('\n{:^79}\n'.format('_____________________          _____________________'))
        f.write('{:^79}\n'.format('Szállító                         Vevő'))
        f.close()
        print('Szállítólevél exportálva.')

    def raktarExport(self):
        sorszam = 1
        datumbelyeg_file = strftime('%Y%m%d%H%M%S')
        datumbelyeg_kijelzo = strftime('%Y.%m.%d.')
        f = open('raktar{}.txt'.format(datumbelyeg_file),'w')
        f.write(SZERVEZET)
        f.write('\n{:_^79}\n'.format('R A K T Á R K É S Z L E T'))
        f.write('\nSorszám_Megnevezés_______________________Készlet_______Egységár________Érték___\n\n')
        for cikkszam in self.cikkszamok:
            self.kurzor.execute('SELECT megnevezes, keszlet, egyseg, egysegar FROM raktar WHERE cikkszam = {}'.format(cikkszam))
            sor = self.kurzor.fetchone()
            if sor['keszlet']:
                f.write('{:>6}  {:<28} {:>8} {} {:>9} Ft/{} {:>11} Ft\n'.format(format(sorszam, '0=5'), sor['megnevezes'][0:28], ezresv(format(sor['keszlet'], '.2f')), sor['egyseg'], ezresv(sor['egysegar']), sor['egyseg'], ezresv(int(sor['keszlet'] * sor['egysegar']))))
                sorszam += 1
        f.write('_______________________________________________________________________________\n')
        f.write('\nKiválasztás értéke összesen:                                    {:>12} Ft\n'.format(ezresv(self.kivalasztasErteke())))
        f.write('Raktár értéke összesen:                                         {:>12} Ft\n'.format(ezresv(self.raktarErtek())))
        f.write('\nKelt: Városlőd, {}\n'.format(datumbelyeg_kijelzo))
        f.close()
        print('Raktárkészlet exportálva.')

if __name__ == '__main__':
    foProgram()
