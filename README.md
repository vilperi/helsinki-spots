# HelsinkiSpots

Tämä sovellus on tarkoitettu mielenkiintoisten kaupunkikohteiden listaamisen Helsingissä. Kohde voi olla esimerkiksi nähtävyys, aktiviteetti, arkkitehtuurinen kohde, katutaideteos tai hyvä skeittauspaikka. Kohde voi olla myös esimerkiksi viihtyisä paikka puistossa tai paikka, josta aukeaa kiva näkymä. Käyttäjät voivat antaa kohteista lisätietoa kommentoiden sekä omia että muiden luomia kohteita antaen niistä omaan paikkallistuntemukseen perustuvia kommentteja.

(Karttasovellus tulee kurssin jälkeen.)

## Sovelluksen toiminnot

- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy lisäämään kohteita kirjauduttuaan sisään. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään kohteita.
- Käyttäjä pystyy valitsemaan lisäämälleen kohteelle yhden kategorian.
- Käyttäjä pystyy selaamaan kohteita. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät kohteet.
- Käyttäjä pystyy etsimään tietokohteita hakusanalla sekä kategorian perusteella. Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä kohteita.
- Sekä omia että muiden tekemiä kohteita pystyy kommentoimaan. Omia kommentteja pystyy muokkaamaan tai poistamaan.
- Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tilastoja ja käyttäjän lisäämät kohteet.

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

## Sovelluksen isojen tietomäärien käsittely
- Sovellusta on testattu testidatalla seed.py tiedoston avulla, joka loi 10^6 kohdetta ja 10^7 kommenttia.
- Parannukset, jotka tehtiin vastausnopeuksien nopeuttamiseksi:
  1. Etusivun kohteiden ja kohdesivulla kommenttien sivuttaminen.
  2. SQL-kyselyn parantaminen (yhdistelmätauluista alikyselyihin).
  3. Tietokannan indeksointi
- Ennen indeksointia etusivun lataamiseen meni 5,12 s. Indeksoinnin jälkeen se kesti 0,05 s.