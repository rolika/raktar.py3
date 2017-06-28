# raktar.py3
Raktárkészlet-nyilvántartó program

Kezelési utasítás

1.  Első indítás
    Első indításkor a program létrehozza az adatbázist, amely természetesen üres, és üresek a kijelzők is. Első lépés az adatbázis feltöltése.

2.  Kezelőfelületek
    A kezelőfelület két részből áll.
    A bal oldalon van a szerkesztőfelület, ill. a részletes kijelzés.

    Cikkszám: a rendszer automatikusan cikkszámot rendel minden egyes tételhez.
    Készlet: a tételhez tartozó mennyiség, annak mértékegységével együtt.
    Kiválasztás értéke: ha szűrőfeltétel lett megadva, annak értéke.
    Raktár értéke: kiválasztástól függetlenül mindig a raktár teljes értékét mutatja.
    Megnevezés: a tétel egyértelmű beazonosítása. Ez a megnevezés jelenik meg a jobb oldali listában, de az exportált (nyomtatható) listákban is. Pl. Sikaplan 15 G, vagy Ejot TKR 140 mm
    Gyártó: gyártó cég megnevezése, pl. Sika vagy Ejot
    Leírás: tételt jellemző leírás, pl. 1,5 mm pvc fólia, vagy önmetsző csavar, kötőelem
    Megjegyzés: egyéb megjegyzés
    Egység: a tétel jellemző mértékegysége, pl. m2 vagy db
    Egységár: mennyibe kerül
    Készlet: előjel nélkül megadva beállítja a készletet az adott értékre. + előjellel hozzáad értéket (készletet növel), - előjellel pedig készletet csökkent. (A szállítólevél csak előjeles mennyiségeket vesz figyelembe, ld. ott.)
    Kiszerelés: adott termék kiszerelése. Pl. 30 vagy 40 m2, vagy 500 db.
    Raktári hely: hol található a raktárban.
    Eltarthatóság: szavatossági idő hónapokban megadva.
    Gyártási idő: gyártási idő megadása ÉÉÉÉ-HH-NN formátumban. A program kijelzi, ha lejárt a termék.

    A nyilvántartás értelmes vezetéséhez az alábbi értékeket kell megadni:
    - megnevezés,
    - egység,
    - egységár,
    - készlet és változásai.
    Ebben az esetben képes a program a raktárkészletről listát készíteni, amely tartalmazza az egyes tételek és a teljes raktár értékét is.
        
    A jobb oldalon egy lista található, a raktárkészlet összes elemével, vagy az aktuális kiválasztással. A lista rövid információt ad az elemekről, feltüntetve a megnevezés és a mennyiséget (ennek mértékegységével együtt.)
    A tételek innen is kiválaszthatók bal egérgombbal.
    A listát lehet görgetni az egérrel és fel-le billentyűkkel, lapozni a PageUp-PageDown billentyűkkel, az elejére lehet ugrani a Home, a végére pedig az End billentyűvel.

    Alul találhatók a kezelőgombok.

    Új: új tétel bevitele, üres mezőkkel. E gomb kilép a kiválasztásból.
    Mentés: Elmenti a kijelzett tételt. Meglévő esetén csak módosít, új esetén létrehoz. A Mentés-gomb nem frissíti a kijelzőt. Az elgondolás emögött az, hogy sokkal egyszerűbb közel azonos termékeket úgy felvinni, hogy csak az egyes mezőket változtatjuk meg (pl. gyártó ugyanaz).
    <<<: előrelapoz a tételek között. A legelején az utolsó elemre ugrik.
    >>>: hátralapoz a tételek között. A legvégén az első elemre ugrik.

3.  Tételek bevitele
