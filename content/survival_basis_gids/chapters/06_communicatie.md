# Hoofdstuk 6: Off-Grid Communicatie — Verbonden Blijven Zonder Internet of Telefoonnet

> **Praktische samenvatting:** In een crisis valt communicatie-infrastructuur vaak als eerste weg: overbelasting van mobiele netwerken, stroomuitval bij zendmasten, of fysieke schade aan kabels en torens. Wie een alternatief communicatienetwerk heeft, is enorm in het voordeel. Dit hoofdstuk behandelt alle praktische opties: van portofoons tot korte-golf radio, van mesh-netwerken tot gecodeerde berichten, en hoe je een lokaal communicatienet opzet voor je gemeenschap.

---

## Waarom communicatie je eerste bottleneck is in een crisis

Communicatie is de zenuw van iedere crisis-respons. Zonder communicatie:

- Weet je niet wat er aan de hand is of waar
- Kun je geen hulp coördineren
- Raken familieleden gescheiden zonder mogelijkheid om contact te zoeken
- Ben je afhankelijk van geruchten in plaats van feiten
- Kun je geen noodsituaties doorgeven aan hulpverleners

De Nederlandse 112-dienst en het openbare alarmeringsnetwerk NL-Alert zijn uitstekend — maar ze zijn afhankelijk van elektriciteit en dataverbindingen. Bij grootschalige calamiteiten overbelasten mobiele netwerken binnen minuten; bij stroomuitval vallen celmasten na 4-8 uur (op batterijbackup) uit.

**Jouw doel:** Een communicatiepakket dat onafhankelijk werkt van het publieke netwerk.

---

## Communicatieniveaus en afstandsbereik

Kies communicatiemiddelen per afstandsniveau:

| Niveau | Afstand | Oplossing |
|--------|---------|-----------|
| Lokaal (thuis, tuin) | 0-100m | Touw + blikken, handgebaren, fysiek contact |
| Buurt | 100m-2km | Portofoons (PMR446), semafoon |
| Regionaal | 2km-50km | VHF/UHF radio (C2000 via hulpverleners, of amateur radio) |
| Nationaal/Internationaal | 50km-wereldwijd | HF/Shortwave radio, satelliet communicatie |

---

## PMR446 Portofoons — De buurtcommunicatie standard

### Wat zijn PMR446 portofoons?

PMR (Private Mobile Radio) 446 MHz zijn draagbare twee-richtings-radio's (walkie-talkies) die in heel Europa vrij te gebruiken zijn zonder vergunning. Ze werken op de 446 MHz-band met maximaal 0,5W vermogen.

**Praktisch bereik:**
- Open terrein: 3-8 km
- Stedelijk gebied: 0,5-2 km (gebouwen dempen het signaal sterk)
- Binnenshuis: 100-500m

**Voordelen:**
- Geen vergunning nodig
- Goedkoop (€20-80 per paar)
- Eenvoudig in gebruik
- Breed beschikbaar — ook buren en familie kunnen zonder vergunning deelnemen

**Nadelen:**
- Beperkt bereik
- Gedeeld kanaal met andere gebruikers (geen privacy)
- Niet versleuteld

**Aanbevolen modellen:**
- Midland G9 Pro: goede bouw, rijkere functies, betaalbaar
- Motorola Talkabout T62: bewezen kwaliteit, waterdicht
- Retevis RT22: budget-optie, soms al voor €15 per paar

### Kanaalplannen voor buurtnetwerken

PMR446 heeft 16 standaardkanalen (8 origineel + 8 toegevoegd in nieuwe normen). Wijs vaste kanalen toe voor je gemeenschap:

- **Kanaal 1:** Buurtoproep / noodoproep (altijd vrij houden voor nood)
- **Kanaal 2:** Dagelijks verkeer groep A
- **Kanaal 3:** Dagelijks verkeer groep B
- **Kanaal 8:** Regionaal noodkanaal (officieel noodkanaal in sommige landen)

Maak een simpele kaart met kanaal-toewijzingen voor je buurt en deel dit mee voor een crisis.

---

## Noodradio — Ontvangen van officiële berichten

### Urgentie van noodradio

Als één apparaat verplicht is in jouw noodkit, dan is het een noodradio. Hiermee ontvang je:
- Rijksoverheid waarschuwingen
- KNMI weerberichten en stormwaarschuwingen
- Regionale omroepen met lokale situatie-informatie
- Calamiteitenzender (in NL: Radio 1 en regionale omroepen)

**Minimale eisen aan een noodradio:**
- Batterijbediend (AA of AAA — breed beschikbaar)
- Dynamo/handkruk als backup (laadt een interne accu)
- Zowel AM als FM
- Klein, lichtgewicht, robuust

**Aanbevolen modellen:**
- Eton FRX3+: dynamo + zonne-energie + USB-oplader, AM/FM/NOAA (voor Nederland: AM/FM voldoende)
- Sangean PR-D4: eenvoudig, betrouwbaar, lang batterijleven
- Kaito KA500: dynamo + zonnepaneel + zaklamp, breed frequentiebereik

### DAB+ en FM/AM in noodsituaties

Nederland heeft een uitgebreid DAB+ (digitale radio) netwerk. DAB+ vereist echter een DAB+-ontvanger en werkt via digitale decodering. Voordeel: betere geluidskwaliteit. Nadeel: uitvalliger bij slechte signaalomstandigheden dan analoge FM/AM.

**Aanbeveling:** Zorg voor zowel DAB+ als FM/AM ontvangst. Bij calamiteiten zenden Nederlandse radiozenders op zowel FM als DAB+.

---

## Kortegolf en amateur radio

### Waarom kortegolf (HF)?

Kortegolf radio (3-30 MHz) heeft een unieke eigenschap: het signaal kaatst terug van de ionosfeer (een laag in de atmosfeer) waardoor communicatie over duizenden kilometers mogelijk is zonder tussenliggende infrastructuur. Dit is de basis van internationale noodcommunicatie.

**Kortegolf ontvangen (zonder vergunning):**
- SDR-receiver (Software Defined Radio): een USB-dongle voor €25-30 die met software (SDR#, GQRX) tientallen frequenties kan ontvangen
- Traditionele shortwave-radio: modellen van Tecsun, Sangean, Sony ontvangen 1-30 MHz inclusief internationale noodfrequenties
- Luister naar: BBC World Service, Radio Nederland Wereldomroep-successors, DW, VOA — allemaal op shortwave actief

**Kortegolf uitzenden (met amateurslicentie):**
In Nederland vereist het uitzenden op kortegolf een amateurslicentie (Novice of Volledige). De cursus duurt enkele maanden en kost circa €100-150 voor cursus en examen (Agentschap Telecom). Na het behalen van het N- of F-certificaat mag je:
- Uitzenden op gereguleerde amateurbanden
- Deelnemen aan internationale noodnetwerken (IARU Regio 1 Emergency)
- Communiceren met andere radioamateurs wereldwijd

**Waarde in een crisis:** Een gelicentieerde radioamateur in je gemeenschap is een onschatbare asset. Zoek contact met de lokale amateurvereniging (VERON) voor meer informatie.

### APRS — Automatische positiemelding

APRS (Automatic Packet Reporting System) is een protocol waarmee je positie- en tekstberichten kunt versturen via amateur radio-frequenties. Het werkt zonder internet en heeft een wereldwijd netwerk van igates (gateway-stations) die berichten doorsturen.

Met een APRS-capable portofoon (zoals de Kenwood TH-D74) kun je berichten versturen die via het amateurrnet worden doorgegeven — zelfs in afgelegen gebieden zonder mobiele dekking.

---

## Mesh-netwerken en lokale communicatie zonder internet

### Wat zijn mesh-netwerken?

Een mesh-netwerk is een draadloos netwerk waarbij elk knooppunt tegelijk router is — berichten vinden zelf hun weg van knooppunt naar knooppunt zonder centrale server. Als een knoop uitvalt, route het netwerk er omheen.

**Merakels (Meshtastic):** Een goedkoop, open-source LoRa-gebaseerd mesh-netwerk. LoRa (Long Range) radio gebruikt 433/868 MHz en bereikt 3-15 km in open terrein, 0,5-2 km stedelijk. Apparaten kosten €25-50 (TTGO T-Beam of Heltec LoRa32).

**Mogelijkheden Meshtastic:**
- Tekst- en GPS-berichten sturen zonder SIM, WiFi of internet
- Bereik van 15-30 km met een paar knooppunten (relay)
- Volledig versleuteld
- Open source software voor Android en iOS
- Ideaal voor buurtnetwerken van preppers

**Installatie (Meshtastic):**
1. Koop TTGO T-Beam of Heltec LoRa32 module (€25-40)
2. Flash Meshtastic-firmware via USB
3. Configureer via smartphone-app (Bluetooth)
4. Stel kanaalnaam en optionele versleuteling in
5. Plaatse tweede knooppunt bij buur/partner voor eerste hop

### GoTenna en Zello

**GoTenna Mesh:** Commercieel product dat SMS over mesh-radio verstuurt. Duurder maar gebruiksvriendelijker dan Meshtastic. Bereik 2-8 km per hop.

**Zello:** Walkie-talkie app over internet. Werkt zolang er internet is. Minder geschikt voor echte noodsituatie maar uitstekend als primair medium met mesh/radio als backup.

---

## Satelietcommunicatie

### Wanneer satelietcommunicatie?

Satellietcommunicatie werkt onafhankelijk van terrestrische infrastructuur. Dit maakt het ideaal voor:
- Afgelegen gebieden zonder netwerk
- Zeeschepen en expedities
- Gebieden waar alle terrestrische communicatie is uitgevallen

**Opties voor particulieren:**

**Garmin inReach Mini 2:** Twee-richtings sms via Iridium-satelliet. Abonnement vereist (~€15-35/maand afhankelijk van plan). Ideaal voor sporadisch gebruik. Bereikt redding over de hele wereld.

**SPOT Gen4:** Eén-richting: stuurt GPS-positie en noodoproep via GlobalStar. Goedkoper abonnement maar minder functies.

**Thuraya / Iridium satelliettelefoon:** Volledig satelliettelefoon voor stem en data. Duur ($500-1500 voor apparaat + $1-2/min belkosten). Overkill voor thuisgebruik maar onmisbaar voor expedities.

**Starlink (terminals):** Biedt snel breedband internet via LEO-satellieten. Duur (~€350 voor hardware, €50-100/maand). Werkt in gebieden zonder terrestrisch internet. Starlink-terminals vereisen stroom (45-100W) en zijn niet echt draagbaar in huidige vorm.

---

## Codering en berichten-discipline

In een crisis is het belangrijk om je berichten efficiënt en soms vertrouwelijk te houden.

### Radioprotocol voor beginners

Als je een portofoon of radio gebruikt in een georganiseerd netwerk:

- **Denk na voor je praat** — plannen wat je wilt zeggen bespaart zendtijd
- **Roep-, antwoord-** patroon: "Hier Jan Jansen voor Piet de Vries, ontvangst?"
- **Over** = ik ben klaar, jij kunt praten
- **Wissel** of **Out** = gesprek beëindigd
- **Break Break** = prioriteitsbericht, vrij houden van kanaal
- **Noodoproep:** "Mayday Mayday Mayday — hier [naam], [locatie], [noodsituatie]"

### Licht-signalen (noodcommunicatie)

Bij volledig gebrek aan radio:
- **Spiegelsein:** Een zakspiegeltje of glanzend oppervlak kan zonlicht over 15-20 km reflecteren — zichtbaar voor vliegtuigen en verre waarnemers
- **Vuur- en rooksignalen:** 3 vuren in driehoek = internationaal noodteken; wit rook (groen gras of bladeren) bij dag is goed zichtbaar
- **SOS in morse:** ··· −−− ··· (drie korte, drie lange, drie korte flitsen of tonen)

### Berichten-drop (dead drop)

In een scenario waar radiocommunicatie onveilig is, kunnen vooraf afgesproken fysieke drop-locaties worden gebruikt:
- Steen met inkervingen
- Brief in waterdichte zak onder een steen
- Gekleurd teken aan brievenbus of deur

---

## Noodcommunicatieplan voor het huishouden

Elk huishouden zou een noodcommunicatieplan moeten hebben, opgesteld *vóór* een crisis.

### Basisplan

1. **Primair ontmoetingspunt:** Een specifieke locatie waar alle gezinsleden naartoe gaan als contact niet mogelijk is (bijv.: voordeur van oma, school, gemeentehuis)
2. **Secundair ontmoetingspunt:** Als het primaire punt niet bereikbaar is
3. **Buiten-de-stad contact:** Één persoon buiten de regio die berichten kan relay-en (vaak is afstandsgesprek makkelijker dan lokaal tijdens regionaal incident)
4. **Check-in tijdstip:** Dagelijks tijdstip voor radiocommunicatie (bv. 08:00 en 20:00)
5. **Kanalen/frequenties:** Welke portofoon-kanalen je gebruikt

### Documenteer en laminer het plan

Druk het noodcommunicatieplan af, laminer het, en bewaar in ieder auto, noodtas, en op de koelkast. Kinderen moeten hun eigen exemplaar hebben.

---

## Checklist off-grid communicatie

### Minimumpakket
- [ ] Batterij/dynamo noodradio (AM/FM minimaal)
- [ ] 2× PMR446 portofoons (per huishouden)
- [ ] Extra batterijen AA/AAA voor radio en portofoons
- [ ] Noodcommunicatieplan (gedocumenteerd en bij iedereen)

### Uitgebreid pakket
- [ ] Set van 4-6 PMR446 portofoons voor buurtnetwerk
- [ ] Meshtastic-apparaten (2+) voor buurtmesh-netwerk
- [ ] SDR-receiver voor kortegolfontvangst
- [ ] Kortegolf AM/SW-radio (Tecsun PL-660 of vergelijkbaar)
- [ ] Garmin inReach Mini (voor buiten-netwerk noodoproepen)

### Gevorderd pakket
- [ ] Amateur radio certificaat (N-certificaat minimaal)
- [ ] VHF/UHF amateur portofoon (Baofeng UV-5R als budget-start, maar ook Yaesu, Kenwood)
- [ ] HF-transceiver voor lange-afstandcommunicatie
- [ ] Antenne-installatie (dipool of verical voor HF)

---

## Digitale communicatie in (gedeeltelijk) werkende netwerken

In veel crises is het netwerk niet volledig uitgevallen maar eerder overbelast. Er zijn manieren om efficiënter gebruik te maken van een traag of gedeeltelijk werkend netwerk.

### SMS versus bellen

Bij netwerkoverlast komen SMS-berichten vaak wél door terwijl bellen mislukt. Dit heeft te maken met de lagere bandbreedte die SMS vereist. Gebruik SMS als eerste keuze in een crisis.

### WhatsApp en messaging apps

WhatsApp, Signal en Telegram gebruiken dataverbinding in plaats van traditioneel bellen. Bij lage signaalsterkte kunnen deze apps soms kleine tekstberichten versturen wanneer bellen onmogelijk is.

**Tips:**
- Stuur korte, informatieve berichten in plaats van lange verhalen
- Gebruik geen zware bijlagen (foto's, video) als het netwerk overbelast is
- Stel bevestiging in (lees-ontvangst) zodat je weet of je bericht aankwam

### Noodberichten via SMS

In Nederland stuurt de overheid NL-Alert-berichten via Cell Broadcast — dit is een nooduitzending naar alle telefoons in een bepaald gebied, vergelijkbaar met een FM-radio uitzending over het mobiele netwerk. Het werkt ook bij overbelasting van het netwerk.

- NL-Alert is automatisch ingeschakeld op moderne smartphones
- Controleer in je telefooninstellingen of NL-Alert is ingeschakeld

---

## Communicatiebeveiliging en privacy

In een crisis kunnen communicatiekanalen afgeluisterd worden of kan er verkeerde informatie circuleren. Basisbewustzijn van communicatiebeveiliging is waardevol.

### Versleuteling van berichten

- **Signal:** De meest veilige messaging-app, volledig end-to-end versleuteld, open source. Ideale keuze voor privéberichten.
- **WhatsApp:** Ook end-to-end versleuteld maar eigendom van Meta; metadata wordt bijgehouden.
- **SMS:** Niet versleuteld; eenvoudig te onderscheppen.
- **Radiotransmissie (portofoon/amateur):** Volledig openbaar tenzij je versleuteling gebruikt; ga ervan uit dat alles meegelezen kan worden.

### Communicatie in publieke ruimtes

Op PMR- of amateurbanden moet je aannemen dat iedereen meeluistert. Gebruik nooit:
- Volledige namen en adressen
- Informatie over waardevolle voorraad of bezittingen
- Details over je beveiligingssituatie

Gebruik codes of afkortingen voor gevoelige informatie (noodstatus, locatiedetails). Bespreek je codesysteem van tevoren met je netwerk.

---

## Communicatie voor kinderen in noodsituaties

Kinderen moeten hun eigen basis-noodcommunicatieplan kennen.

### Wat elk kind moet weten

- **Volledige naam van beide ouders en thuis-adres**
- **Telefoonnummer ouder** (uit het hoofd geleerd)
- **Schoolemergency protocol** (weet het kind welke procedures de school hanteert?)
- **Ontmoetingspunt 1 en 2**
- **Hoe 112 te bellen** (en wanneer)
- **Hoe een bericht te sturen** via SMS als bellen niet lukt

### Oefenen van communicatieplan met kinderen

- Bespreek het plan minimaal één keer per jaar (bv. bij aanvang van het nieuwe schooljaar)
- Speel een scenario na: "Stel dat er een alarm is op school. Wat doe jij?"
- Laat kinderen het telefoonnummer van buitenaf contact opnemen
- Geef kinderen een gelamineerde kaart met contactnummers in hun schooltas

---

## Samenvatting

Off-grid communicatie vereist voorbereiding maar is eenvoudig te implementeren:

1. **Noodradio** — het minimale; ontvang officiële berichten bij elke ramp
2. **PMR446 portofoons** — goedkoop, vergunningsvrij, ideaal voor buurtcommunicatie
3. **Mesh-netwerken (Meshtastic)** — de toekomst van lokale noodcommunicatie
4. **Satelietoptie** — voor extreme situaties
5. **Plan vooraf** — ontmoetingspunten, check-in tijden, kanalen
6. **NL-Alert** — controleer of dit is ingeschakeld op jouw smartphone
7. **Communicatiebeveiliging** — op publieke banden is alles openbaar; gebruik codes voor gevoelige info
8. **Kinderplan** — kinderen moeten hun noodplan kennen en hebben geoefend

Communicatie is het verschil tussen gecoördineerde respons en chaos. Wie goed communiceert, overleeft beter.

---

*Volgende hoofdstuk: Onderdak en isolatie DIY — jezelf beschermen tegen de elementen →*
