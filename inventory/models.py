from django.db import models
from datetime import datetime, timedelta, timezone
import pytz

JA_NEIN_CHOICES = [
    ('Ja','Ja'), ('Nein','Nein')
]

JA_NEIN_NS_CHOICES = [
        ('Ja', 'Ja'), ('Nein', 'Nein'), ('Nicht sicher', 'Nicht sicher')
    ]

ZAHLUNGSART_CHOICES = [
    ('Bar','Bar'), ('Überweisung','Überweisung')
]
class BasicInformation(models.Model):
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


class Gerät(BasicInformation):

    def __str__(self):
        return self.marke

class Waschmaschine(BasicInformation):
    FASSUNG_CHOICES = [
        ("5", "5"),("6", "6"),("7", "7"),("8", "8"),("9", "9"),("10", "10"),("mehr", "mehr"),

    ]
    fassung = models.CharField(max_length=20, choices=FASSUNG_CHOICES)
    toploader = models.CharField(max_length=5, choices=JA_NEIN_CHOICES, default='Nein')

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
    induktion = models.CharField(choices=JA_NEIN_NS_CHOICES,default="Nicht sicher", max_length=20)
    pyrolyse = models.CharField(choices=JA_NEIN_CHOICES,default="Nicht sicher", max_length=20)
    umluft = models.CharField(choices=JA_NEIN_CHOICES,default="Nicht sicher", max_length=20)
    Herdplatte_model = models.CharField(null=True, blank=True, max_length=200)
    Anzahl_kochfelder = models.PositiveIntegerField(blank=True,null=True)


class Herdplatte(BasicInformation):
    induktion = models.CharField(choices=JA_NEIN_NS_CHOICES, default="Nicht sicher", max_length=20)
    breite = models.CharField(blank=True,null=True,max_length=100)
    Anzahl_kochfelder = models.PositiveIntegerField(blank=True, null=True)

class Standherd(BasicInformation):
    induktion = models.CharField(choices=JA_NEIN_NS_CHOICES, default="Nicht sicher", max_length=20)
    pyrolyse = models.CharField(choices=JA_NEIN_NS_CHOICES, default="Nicht sicher", max_length=20)
    umluft = models.CharField(choices=JA_NEIN_NS_CHOICES, default="Nicht sicher", max_length=20)
    Herdplatte_model = models.CharField(null=True, blank=True, max_length=200)
    Anzahl_kochfelder = models.PositiveIntegerField(blank=True, null=True)

class Trockner(BasicInformation):
    FASSUNG_CHOICES = [
        ("4","4"),("5", "5"), ("6", "6"), ("7", "7"), ("8", "8"), ("9", "9"), ("10", "10"), ("mehr", "mehr"),

    ]
    TROCKNER_ARTEN = [
        ("Kondens", "Kondens"), ("Wärmepumpe", "Wärmepumpe"), ("other", "other"),

    ]
    art = models.CharField(choices=TROCKNER_ARTEN,default="other", max_length=20)
    fassung = models.CharField(max_length=20, choices=FASSUNG_CHOICES)

class Abzughaube(BasicInformation):
    art = models.CharField(blank=True,null=True,max_length=100)
    breite = models.CharField(blank=True,null=True,max_length=100)

class Sonst(BasicInformation):
    geraet = models.CharField(blank=True,null=True,max_length=100)

class Verkauf(models.Model):
    TYPE_OF_CHOICES = [
        ('Waschmaschine','Waschmaschine'),
        ('Kühlschrank', 'Kühlschrank'),
        ('Spülmaschine','Spülmaschine'),
        ('Spülmaschine', 'Spülmaschine'),
        ('Herdplatte', 'Herdplatte'),
        ('Standherd', 'Standherd'),
        ('Trockner', 'Trockner'),
        ('Abzughaube', 'Abzughaube'),
        ('Sonst', 'Sonst'),
        ('gerät','gerät'),

    ]

    gerät = models.ForeignKey(Gerät, on_delete=models.SET_NULL, null=True, blank=True)
    waschmaschine = models.ForeignKey(Waschmaschine, on_delete=models.SET_NULL, null=True, blank=True)
    kuhlschrank = models.ForeignKey(Kuehlschrank, on_delete=models.SET_NULL, null=True, blank=True)
    spuelmaschine= models.ForeignKey(Spuelmaschine, on_delete=models.SET_NULL, null=True, blank= True)
    verkäufer = models.CharField(max_length=255)
    type_of = models.CharField(max_length=200, choices=TYPE_OF_CHOICES)
    menge = models.IntegerField()

    zahlungsart = models.CharField(max_length=100, choices=ZAHLUNGSART_CHOICES, blank=True, null=True)
    verkaufsdatum = models.DateTimeField(editable=True,default=datetime.now)
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


    type_of2 = models.CharField(max_length=200, choices=TYPE_OF_CHOICES, null=True, blank=True)
    menge2 = models.IntegerField(null=True, blank=True)
    marke2 = models.CharField(max_length=50, null=True, blank=True)
    model2 = models.CharField(max_length=100, null=True, blank=True)
    serial_number2 = models.CharField(max_length=50, null=True, blank=True)
    artikel_nr2 = models.CharField(max_length=50, null=True, blank=True)
    preis2 = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    beschreibung2 = models.TextField(max_length=500, null=True, blank=True)

    def calculate_final_preis(self):
        return (self.preis or 0) + (self.preis2 or 0)

    final_preis = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    def save(self, *args, **kwargs):
        self.final_preis = self.calculate_final_preis()
        super(Verkauf, self).save(*args, **kwargs)