N�vod na in�tal�ciu a spustenie.

Stiahnite cel� prie�inok projektu z https://github.com/TIS2018-FMFI/shmu.

Do prie�inka /data nakop�rujte potrebn� s�bory. Do /data/nc_pollutants NetCDF s�bory. 
Do /data/csv_pollutants CSV d�ta - merania stan�c. Do /data/stanice_shp  SHP s�bory s  inform�ciami o merac�ch staniciach.
V s�bore /data/config.json si nakonfigurujete cesty a n�zvy jednotliv�ch koncentr�cii, stan�c a mrie�ky vo form�te JSON.

V prie�inku /src s� ulo�en� zdrojov� k�dy aplik�cie a v pri�inku /src/generated generovan� s�bory. Webov� v�stup aplik�cie
sa nach�dza v prie�inku /src/web. 

Pred spusten�m je treba nain�talova� potrebn� python moduly. S� uveden� aj so z�vislos�ami v s�bore PACKAGES. Po ich �spe�nom nain�talovan� 
treba spusti� skript main.py z prie�inka /src. Bu� v nejakom pythonovskom editore alebo cez pr�kazov� riadok pr�kazom: 
python main.py (ak je nastaven� PATH k python interpretru). Skript vyp�e "nacitavam data", chv�u pracuje a po vyp�san� "koniec nacitavania dat"
be�� localhost server na porte 8000. Aplik�cia nabehne po zadan� URL adresy http://localhost:8000/ do prehliada�a. Podporovan� s� Chrome, Firefox, Safari.

APLIK�CIA POTREBUJE INTERNETOV� PRIPOJENIE.

Pou��vanie aplik�cie:

Na mape sa zobraz� raster pre najmen�� de� v s�bore, ktor� je prv� uveden� v configu v nc_pollutants. Mapa sa d� pribli�ova�, pos�va�.
Po kliknut� na �tvor�ek rastra sa zobraz� konkr�tna namodelovan� hodnota. Po kliknut� na stanicu sa zobrazia �daje o nej a nameran� hodnota.
D�tum sa d� zmeni� kliknut�m na box s d�tumom a zvolen�m konkr�tneho d�a. V�ber je obmedzen� pod�a obsahu nahrat�ho NetCDF s�boru. Ak je v configu v nc_pollutants,
viac ako jedna koncentr�cia, tak je mo�n� medzi nimi prep�na� v boxe ved�a d�tumu. V�ber farebnej sch�my rastra sa d� zvoli� v boxe ved�a. Tla��tkom PLAY sa spust� 
anim�cia rastrov po hodin�ch v danom dni. Anim�cia sa v danom dni opakuje k�m ju nezastav�te t�m ist�m tla��tkom. �as sa d� meni� aj ru�ne, potiahnut�m slidra na osi pod mapou.
Ak sa aplik�cia nespr�va pod�a predst�v, treba skontrolova� v�stup main.py, kde s� v�pisy zo servra, ale bud� tam vyp�san� aj pr�padn� chyby v python Traceback form�te.
Aplik�cia sa ukon�� ukon�en�m serverovej �asti.