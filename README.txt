Návod na inštaláciu a spustenie.

Stiahnite celı prieèinok projektu z https://github.com/TIS2018-FMFI/shmu.

Do prieèinka /data nakopírujte potrebné súbory. Do /data/nc_pollutants NetCDF súbory. 
Do /data/csv_pollutants CSV dáta - merania staníc. Do /data/stanice_shp  SHP súbory s  informáciami o meracích staniciach.
V súbore /data/config.json si nakonfigurujete cesty a názvy jednotlivıch koncentrácii, staníc a mrieky vo formáte JSON.

V prieèinku /src sú uloené zdrojové kódy aplikácie a v prièinku /src/generated generované súbory. Webovı vıstup aplikácie
sa nachádza v prieèinku /src/web. 

Pred spustením je treba nainštalova potrebné python moduly. Sú uvedené aj so závislosami v súbore PACKAGES. Po ich úspešnom nainštalovaní 
treba spusti skript main.py z prieèinka /src. Buï v nejakom pythonovskom editore alebo cez príkazovı riadok príkazom: 
python main.py (ak je nastavená PATH k python interpretru). Skript vypíše "nacitavam data", chví¾u pracuje a po vypísaní "koniec nacitavania dat"
beí localhost server na porte 8000. Aplikácia nabehne po zadaní URL adresy http://localhost:8000/ do prehliadaèa. Podporované sú Chrome, Firefox, Safari.

APLIKÁCIA POTREBUJE INTERNETOVÉ PRIPOJENIE.

Pouívanie aplikácie:

Na mape sa zobrazí raster pre najmenší deò v súbore, ktorı je prvı uvedenı v configu v nc_pollutants. Mapa sa dá pribliova, posúva.
Po kliknutí na štvorèek rastra sa zobrazí konkrétna namodelovaná hodnota. Po kliknutí na stanicu sa zobrazia údaje o nej a nameraná hodnota.
Dátum sa dá zmeni kliknutím na box s dátumom a zvolením konkrétneho dòa. Vıber je obmedzenı pod¾a obsahu nahratého NetCDF súboru. Ak je v configu v nc_pollutants,
viac ako jedna koncentrácia, tak je moné medzi nimi prepína v boxe ved¾a dátumu. Vıber farebnej schémy rastra sa dá zvoli v boxe ved¾a. Tlaèítkom PLAY sa spustí 
animácia rastrov po hodinách v danom dni. Animácia sa v danom dni opakuje kım ju nezastavíte tım istım tlaèítkom. Èas sa dá meni aj ruène, potiahnutím slidra na osi pod mapou.
Ak sa aplikácia nespráva pod¾a predstáv, treba skontrolova vıstup main.py, kde sú vıpisy zo servra, ale budú tam vypísané aj prípadné chyby v python Traceback formáte.
Aplikácia sa ukonèí ukonèením serverovej èasti.