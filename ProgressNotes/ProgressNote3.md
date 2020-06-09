## Harmadik hét

**Előző hét**: Felállítottuk a Heroku-t hogy a base térkép működjön. [Ha minden igaz itt működik](https://projectgreencity.herokuapp.com/). Csináltunk teszt adatokat, de itt nagy limitáció, hogy még most se tudjuk pontosan hogy fognak kinézni (milyen kiterjesztés és pontosan hol). Egyelőre local szerveren fut egy Dash, ami ábrázolja a napi látogatás számot amit a teszt adatokból töltünk be, illetve továbbra is a térkép működik. 

**Ami elmaradt**: A heroku debugolása elvitt sok időt sajnos, ezért a Drive-os integráció nem sikerült és a teszt adatok teljeskörű felhasználása se történt még meg. 
  - Ami megvan: Local szerveren legördülő menü, amiben ha kiválasztasz egy erdőt vagy parkot akkor rázummol a térképen + alul egy ábra a teszt adatokon mutatja napi óránkénti látogatás számot
  - Amit még szeretnénk: + egy ploty ábra ami a több napi átlag alakulását mutatja parkonként + pár táblázat ami top 5 parkokat mutat (top abszolut látogatók szerint, relatív látogató szám (területméret alapján) stb.)

**Következő hét**: Local serveren legyen kész a teszt adatokkal az app. Google Drive-ot integráljuk valahogy a rendszerbe (onnan olvassuk be a teszt adatokat). Ha ez megvan akkor Drive-ról beolvasva az adatokat szeretnénk majd futtatni a Heroku-n keresztül a web app-ot. Hosszabb távon még javítani kell az adatfrissítést, de erre már vannak ötleteink (sajnos ehhez is látni kéne, hogy hogyan lesznek elnevezve a frissülő látogatási adatok)

**Olvasmányok**:
- [Foliumot nézegettük](https://python-visualization.github.io/folium/quickstart.html)
- Nameg a [Dash-t](https://towardsdatascience.com/a-gentle-invitation-to-interactive-visualization-with-dash-a200427ccce9) is tanulmányoztuk
