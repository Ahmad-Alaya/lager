from django.db import models
from django.shortcuts import render

JA_NEIN_CHOICES = [
    ('Ja','Ja'), ('Nein','Nein')
]

class BasicInformation(models.Model):
    marke = models.CharField(max_length=50)
    model = models.CharField(max_length=100)
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


class Gerät(models.Model):
    marke = models.CharField(max_length=50)
    anzahl = models.IntegerField()
    seriennummer = models.CharField(max_length=50)
    artikelnummer = models.CharField(max_length=50)
    preis = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.marke

class Waschmaschine(BasicInformation):
    FASSUNG_CHOICES = [
        ("5", "5"),("6", "6"),("7", "7"),("8", "8"),("9", "9"),("10", "10"),("mehr", "mehr"),

    ]
    fassung = models.CharField(max_length=20, choices=FASSUNG_CHOICES)
    toploader = models.CharField(max_length=5, choices=JA_NEIN_CHOICES, default='Nein')

    # def __str__(self):
    #     if self.preis:
    #         return f"{self.marke} : {self.fassung}: {self.model} : {self.anzahl} : {self.preis} : {self.toploader}"
    #     else:
    #         return f"{self.marke} : {self.fassung}: {self.model} : {self.anzahl} : {self.toploader}"

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
        ("other", "other"),
    ]
    type = models.CharField(max_length=200, choices=TYPE_CHOICES)

    # def __str__(self):
    #     if self.preis:
    #         return f"{self.marke} : {self.type} :{self.model} : {self.anzahl} : {self.preis}"
    #     else:
    #         return f"{self.marke} : {self.type} :{self.model} : {self.anzahl}"


class Verkauf(models.Model):
    gerät = models.ForeignKey(Gerät, on_delete=models.SET_NULL, null=True, blank=True)
    waschmaschine = models.ForeignKey(Waschmaschine, on_delete=models.SET_NULL, null=True, blank=True)
    kuhlschrank = models.ForeignKey(Kuehlschrank, on_delete=models.SET_NULL, null=True, blank=True)
    spuelmaschine= models.ForeignKey(Spuelmaschine, on_delete=models.SET_NULL, null=True, blank= True)
    verkaufsdatum = models.DateTimeField(auto_now_add=True)
    verkäufer = models.CharField(max_length=255)
    marke = models.CharField(max_length=50, null=True, blank=True)
    seriennummer = models.CharField(max_length=50, null=True, blank=True)
    artikelnummer = models.CharField(max_length=50, null=True, blank=True)
    preis = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)


