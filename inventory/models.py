from django.db import models
from datetime import datetime, timedelta, timezone
import pytz

JA_NEIN_CHOICES = [
        ('Ja', 'Ja'), ('Nein', 'Nein'), ('Nicht sicher', 'Nicht sicher')
    ]

ZAHLUNGSART_CHOICES = [
    ('Bar','Bar'), ('Karte', 'Karte'), ('Überweisung','Überweisung')
]

ZUSTAND_CHOICES = [
    ("Neu", "Neu"), ("Gebraucht", "Gebraucht")
]
class BasicInformation(models.Model):
    zustand = models.CharField(choices=ZUSTAND_CHOICES, default="Neu", max_length=20)
    marke = models.CharField(max_length=50)
    model = models.CharField(max_length=100,unique=True)
    anzahl = models.IntegerField(default=1)
    artikel_nr = models.CharField(max_length=200, null=True, blank=True)
    einkaufsdatum = models.DateField(null=True, blank=True)
    preis = models.FloatField(null=True, blank=True)
    energie = models.CharField(max_length=10, null=True, blank=True)
    bestellungsnummer = models.IntegerField(null=True, blank=True)
    serial_number = models.CharField(max_length=200, null=True, blank=True)
    farbe = models.CharField(max_length=50, null=True, blank=True)
    Beschreibung = models.TextField(max_length=5000, null=True, blank=True)
    note = models.TextField(max_length=1000, null=True, blank=True)
    Kauf_preis = models.FloatField(null= True, blank=True)


class Gerät(BasicInformation):

    def __str__(self):
        return self.marke

class Waschmaschine(BasicInformation):
    FASSUNG_CHOICES = [
        ("5", "5"),("6", "6"),("7", "7"),("8", "8"),("9", "9"),("10", "10"),("mehr", "mehr"),

    ]
    fassung = models.CharField(max_length=20, choices=FASSUNG_CHOICES)
    toploader = models.CharField(max_length=20, choices=JA_NEIN_CHOICES, default='Nein')

    def __str__(self):
        if self.preis:
            return f"{self.marke} : {self.fassung}: {self.model} : {self.anzahl} : {self.preis} : {self.toploader}"
        else:
            return f"{self.marke} : {self.fassung}: {self.model} : {self.anzahl} : {self.toploader}"

class Spuelmaschine(BasicInformation):
    BREITE_CHOICESE = [
        ("45 cm", "45 cm"),
        ("60 cm", "60 cm"),
        ("other", "other")
    ]
    ART_CHOICES = [
        ("Vollintegriert", "Vollintegriert"),
        ("Teilintegriert", "Teilintegriert"),
        ("Standgerät", "Standgerät"),
        ("Unterbau", "Unterbau"),
        ("Tischgerät", "Tischgerät"),
        ("other", "other")

    ]
    breite = models.CharField(max_length=100, choices=BREITE_CHOICESE)
    art = models.CharField(max_length=100, choices=ART_CHOICES)

    # def __str__(self):
    #     if self.preis:
    #         return f"{self.marke} : {self.breite}: {self.art} :{self.model} : {self.anzahl} : {self.preis}"
    #     else:
    #         return f"{self.marke} : {self.breite}: {self.art} :{self.model} : {self.anzahl}"


class Kuehlschrank(BasicInformation):
    TYPE_CHOICES = [
        ("Kombi", "Kombi"),
        ("Nur Kuehlen", "Nur Kuehlen"),
        ("Nur Gefrier", "Nur Gefrier"),
        ("Mini Kühlschrank mit Gefrierfach", "Mini Kühlschrank mit Gefrierfach"),
        ("Mini Kühlschrank ohne Gefrierfach", "Mini Kühlschrank ohne Gefrierfach"),
        ("Mini nur Gefrier", "Mini nur Gefrier"),
        ("Gefrierbox", "Gefrierbox"),
        ("Kühlbox","Kühlbox"),
        ("Side-By-Side", "Side-By-Side"),
        ("Truhe","Truhe"),
        ("other", "other"),
    ]
    type = models.CharField(max_length=200, choices=TYPE_CHOICES)
    truhe_groesse = models.CharField(max_length=20,null=True,blank=True)

    # def __str__(self):
    #     if self.preis:
    #         return f"{self.marke} : {self.type} :{self.model} : {self.anzahl} : {self.preis}"
    #     else:
    #         return f"{self.marke} : {self.type} :{self.model} : {self.anzahl}"


class Herdset(BasicInformation):
    induktion = models.CharField(choices=JA_NEIN_CHOICES,default="Nicht sicher", max_length=20)
    pyrolyse = models.CharField(choices=JA_NEIN_CHOICES,default="Nicht sicher", max_length=20)
    umluft = models.CharField(choices=JA_NEIN_CHOICES,default="Nicht sicher", max_length=20)
    Herdplatte_model = models.CharField(null=True, blank=True, max_length=200)
    Anzahl_kochfelder = models.PositiveIntegerField(blank=True,null=True)


class Herdplatte(BasicInformation):
    induktion = models.CharField(choices=JA_NEIN_CHOICES, default="Nicht sicher", max_length=20)
    breite = models.CharField(blank=True,null=True,max_length=100)
    Anzahl_kochfelder = models.PositiveIntegerField(blank=True, null=True)

class Standherd(BasicInformation):
    induktion = models.CharField(choices=JA_NEIN_CHOICES, default="Nicht sicher", max_length=20)
    pyrolyse = models.CharField(choices=JA_NEIN_CHOICES, default="Nicht sicher", max_length=20)
    umluft = models.CharField(choices=JA_NEIN_CHOICES, default="Nicht sicher", max_length=20)
    Herdplatte_model = models.CharField(null=True, blank=True, max_length=200)
    Anzahl_kochfelder = models.PositiveIntegerField(blank=True, null=True)


class Backofen(BasicInformation):
    pyrolyse = models.CharField(choices=JA_NEIN_CHOICES,default="Nicht sicher", max_length=20)
    umluft = models.CharField(choices=JA_NEIN_CHOICES,default="Nicht sicher", max_length=20)


class Trockner(BasicInformation):
    FASSUNG_CHOICES = [
        ("4","4"),("5", "5"), ("6", "6"), ("7", "7"), ("8", "8"), ("9", "9"), ("10", "10"), ("mehr", "mehr"),

    ]
    TROCKNER_ARTEN = [
        ("Kondens", "Kondens"), ("Wärmepumpe", "Wärmepumpe"), ("Ablufttrockner", "Ablufttrockner"), ("other", "other"),

    ]
    art = models.CharField(choices=TROCKNER_ARTEN,default="other", max_length=20)
    fassung = models.CharField(max_length=20, choices=FASSUNG_CHOICES)

class Abzughaube(BasicInformation):
    art = models.CharField(blank=True,null=True,max_length=100)
    breite = models.CharField(blank=True,null=True,max_length=100)

class Sonst(BasicInformation):
    geraet = models.CharField(max_length=100, default=' ')


class Einstellungen(models.Model):
    email_message = models.CharField(max_length=10000, null=True, blank=True)
    rechnung_note = models.CharField(max_length=100, null=True, blank=True,default="Mit 2 Jahre Herstellergarantie")
    bank_name = models.CharField(max_length=100, null=True, blank=True)
    bank_iban = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    absender = models.CharField(max_length=100, null=True, blank=True)

class Verkauf(models.Model):
    CHOICES = [
        ('Ja','Ja'),
        ('Nein','Nein'),
        ('---','---')
    ]
    TYPE_OF_CHOICES = [
        ('Waschmaschine','Waschmaschine'),
        ('Kühlschrank', 'Kühlschrank'),
        ('Spülmaschine','Spülmaschine'),
        ('Spülmaschine', 'Spülmaschine'),
        ('Herdplatte', 'Herdplatte'),
        ('Standherd', 'Standherd'),
        ('Backofen', 'Backofen'),
        ('Trockner', 'Trockner'),
        ('Abzughaube', 'Abzughaube'),
        ('Sonst', 'Sonst'),
        ('gerät','gerät'),

    ]

    verkäufer = models.CharField(max_length=255)
    type_of = models.CharField(max_length=200, choices=TYPE_OF_CHOICES, verbose_name="Gerät")
    menge = models.IntegerField()
    zustand = models.CharField(choices=ZUSTAND_CHOICES, default="Neu", max_length=20)
    zusaetzlich = models.CharField(max_length=100, default="Mit 2 Jahre Herstellergarantie", verbose_name="zusätzlich")
    zahlungsart = models.CharField(max_length=100, choices=ZAHLUNGSART_CHOICES, blank=True, null=True)
    verkaufsdatum = models.DateTimeField(editable=True,default=datetime.now)
    bezahlt = models.CharField(max_length=20, choices=CHOICES, default='---')
    zahlungsdatum = models.DateTimeField(null=True,blank=True)
    marke = models.CharField(max_length=50, null=True, blank=True)
    model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=50, null=True, blank=True)
    artikel_nr = models.CharField(max_length=50, null=True, blank=True)
    preis = models.DecimalField(max_digits=8, decimal_places=2)
    beschreibung = models.TextField(max_length=500, null=True, blank=True)
    rechnungs_nr = models.IntegerField(unique=True)

    kunde_name = models.CharField(max_length=100, null=True, blank=True)
    kunde_strasse = models.CharField(max_length=100, null=True, blank=True)
    kunde_plz = models.CharField(max_length=100, null=True, blank=True)
    kunde_city = models.CharField(max_length=100, null=True, blank=True)
    kunde_email = models.CharField(max_length=100, null=True, blank=True)
    kunde_mobile = models.CharField(max_length=100, null=True, blank=True)


    type_of2 = models.CharField(max_length=200, choices=TYPE_OF_CHOICES, null=True, blank=True, verbose_name="Gerät2")
    menge2 = models.IntegerField(null=True, blank=True)
    marke2 = models.CharField(max_length=50, null=True, blank=True)
    model2 = models.CharField(max_length=100, null=True, blank=True)
    serial_number2 = models.CharField(max_length=50, null=True, blank=True)
    artikel_nr2 = models.CharField(max_length=50, null=True, blank=True)
    preis2 = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    beschreibung2 = models.TextField(max_length=500, null=True, blank=True)
    kapital = models.FloatField(null= True, blank=True, verbose_name="Kauf preis (intern 1.Gerät)")
    kapital2 = models.FloatField(null=True, blank=True, verbose_name="Kauf preis2 (intern 2.Gerät)")

    def calculate_final_preis(self):
        if self.preis:
            preis1 = float(self.preis)
        else:
            preis1= float(0.0)
        if self.preis2:
            preis2 = float(self.preis2)
        else:
            preis2 = float(0.0)
        return float(preis1+preis2)

    def calculate_gewinn(self):
        diff = float(0.0)
        if self.final_preis:
            if self.kapital:
                diff = float(self.final_preis) - float(self.kapital)
                if self.kapital2:
                    diff -= self.kapital2
        return float(diff)


    final_preis = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    gewinn = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    def save(self, *args, **kwargs):
        self.final_preis = self.calculate_final_preis()
        self.gewinn = self.calculate_gewinn()
        super(Verkauf, self).save(*args, **kwargs)


class Storno(models.Model):
    # Metainformation
    zahlungsart = models.CharField(max_length=100, choices=ZAHLUNGSART_CHOICES, blank=True, null=True)
    stornierungsdatum = models.DateTimeField(null=True, blank=True)
    final_erstattung = models.DecimalField(max_digits=8, decimal_places=2) # final preis
    stornierte_rechnung = models.IntegerField(null=True, blank=True)
    nummer = models.IntegerField(unique=True)

    # Kundeninformations
    kunde_name = models.CharField(max_length=100, null=True, blank=True)
    kunde_strasse = models.CharField(max_length=100, null=True, blank=True)
    kunde_plz = models.CharField(max_length=100, null=True, blank=True)
    kunde_city = models.CharField(max_length=100, null=True, blank=True)

    # 1.Artikel
    beschreibung1 = models.TextField(max_length=500, null=True, blank=True)
    preis1 = models.DecimalField(max_digits=8, decimal_places=2)
    erstattung1 = models.DecimalField(max_digits=8, decimal_places=2)
    menge = models.IntegerField(null=True, blank=True)
    artikel_nr = models.CharField(max_length=50, null=True, blank=True)

    # 2.Artikel
    beschreibung2 = models.TextField(max_length=500, null=True, blank=True)
    preis2 = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    erstattung2 = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    artikel_nr2 = models.CharField(max_length=50, null=True, blank=True)



