# HelsinkiSpots

Tämä sovellus on tarkoitettu mielenkiintoisten kaupunkikohteiden listaamisen Helsingissä. Kohde voi olla esimerkiksi nähtävyys, aktiviteetti, arkkitehtuurinen kohde, katutaideteos tai hyvä skeittauspaikka. Kohde voi olla myös esimerkiksi viihtyisä paikka puistossa tai paikka, josta aukeaa kiva näkymä. Käyttäjät voivat antaa kohteista lisätietoa kommentoiden sekä omia että muiden luomia kohteita antaen niistä omaan paikkallistuntemukseen perustuvia kommentteja.

(Karttasovellus tulee kurssin jälkeen.)

## Sovelluksen toiminnot

Kohdat, joita ei vielä sovelluksesta löydy ovat ~~yliviivattu~~
- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy lisäämään kohteita. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään kohteita.
- Käyttäjä pystyy selaamaan kohteita. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät kohteet.
- Käyttäjä pystyy etsimään tietokohteita hakusanalla. Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä kohteita.
- ~~Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tilastoja ja käyttäjän lisäämät kohteet.~~
- Käyttäjä pystyy valitsemaan lisäämälleen kohteelle yhden luokittelun (esim. nähtävyys, aktiviteetti, arkkitehtuurinen kohde, katutaideteos).
- Sekä omia että muiden tekemiä kohteita pystyy kommentoimaan.

## Sovelluksen asennus

Asenna `flask`-kirjasto:

```
$ pip install flask
```

Luo tietokannan taulut:

```
$ sqlite3 database.db < schema.sql
```

Voit käynnistää sovelluksen näin:

```
$ flask run
```

## Käyttöohjeet
- Voit hakea koordinaatit kohteelle osoitteesta https://kartta.paikkatietoikkuna.fi/
  - Klikkaa oikeassa laidassa *XY* -painiketta. Klikkaa sen jälkeen kohteesi sijainti kartalta ja kopioi koordinaatit lomakkeelle.