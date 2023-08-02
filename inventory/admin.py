from django.contrib import admin
from .models import *

# Register your models here.
basic_field=['marke', 'anzahl','preis','']

class WaschmaschineAdmin(admin.ModelAdmin):
    search_fields = ['marke', 'model', 'fassung', 'preis',]
    list_display = ['marke', 'fassung', 'anzahl', 'model','toploader','preis']


class SpuelmaschineAdmin(admin.ModelAdmin):
    search_fields = ['marke', 'model', 'breite', 'art']
    list_display = ["marke", "breite", 'art', 'anzahl',  'model', 'preis']

class KuehlschrankAdmin(admin.ModelAdmin):
    search_fields = ['marke', 'model', 'type']
    list_display = ['marke', 'type', 'anzahl',  'model', 'preis']

class HerdsetAdmin(admin.ModelAdmin):
    search_fields = ['marke', 'model', 'type',]
    list_display = ['marke', 'anzahl',  'model', 'preis','induktion','pyrolyse', 'Anzahl_kochfelder','umluft']

class HerdplatteAdmin(admin.ModelAdmin):
    search_fields = ['marke', 'model', 'type',]
    list_display = ['marke', 'breite', 'anzahl',  'model', 'preis','induktion', 'Anzahl_kochfelder']

class StandherdAdmin(admin.ModelAdmin):
    search_fields = ['marke', 'model', 'type',]
    list_display = ['marke', 'anzahl',  'model', 'preis','induktion','pyrolyse', 'Anzahl_kochfelder','umluft']


class TrocknerAdmin(admin.ModelAdmin):
    search_fields = ['marke', 'model', 'fassung', 'preis',]
    list_display = ['marke', 'fassung', 'anzahl', 'model','art','preis']

class AbzughaubeAdmin(admin.ModelAdmin):
    search_fields = ['marke', 'model', 'fassung', 'preis',]
    list_display = ['marke', 'anzahl', 'model','art','preis', 'breite']

class SonstAdmin(admin.ModelAdmin):
    search_fields = ['marke', 'model', 'fassung', 'preis',]
    list_display = ['geraet','marke', 'anzahl', 'model','preis',]

class VerkaufAdmin(admin.ModelAdmin):
    search_fields = ['marke','rechnungs_nr', 'verkaufsdatum', 'preis']
    list_display = ['marke', 'rechnungs_nr', 'verkaufsdatum', 'preis', 'kunde_name']


# Register your models here.
# admin.site.register(Gerät)
admin.site.register(Verkauf,VerkaufAdmin)
admin.site.register(Waschmaschine,WaschmaschineAdmin)
admin.site.register(Kuehlschrank,KuehlschrankAdmin)
admin.site.register(Spuelmaschine,SpuelmaschineAdmin)
admin.site.register(Herdset,HerdsetAdmin)
admin.site.register(Herdplatte,HerdplatteAdmin)
admin.site.register(Standherd,StandherdAdmin)
admin.site.register(Trockner,TrocknerAdmin)
admin.site.register(Abzughaube,AbzughaubeAdmin)
admin.site.register(Sonst,SonstAdmin)