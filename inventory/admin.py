from django.contrib import admin
from .models import *

# Register your models here.

class WaschmaschineAdmin(admin.ModelAdmin):
    search_fields = ['marke', 'model', 'fassung', 'preis',]
    list_display = ['marke', 'fassung', 'anzahl', 'model']


class SpuelmaschineAdmin(admin.ModelAdmin):
    search_fields = ['marke', 'model', 'breite', 'art']
    list_display = ["marke", "breite", 'art', 'anzahl',  'model']

class KuehlschrankAdmin(admin.ModelAdmin):
    search_fields = ['marke', 'model', 'type']
    list_display = ['marke', 'type', 'anzahl',  'model']

class VerkaufAdmin(admin.ModelAdmin):
    search_fields = ['gerät', 'verkaufsdatum', 'marke', 'preis']
    list_display = ['gerät', 'verkaufsdatum', 'marke', 'preis']

# Register your models here.
admin.site.register(Gerät)
admin.site.register(Verkauf,VerkaufAdmin)
admin.site.register(Waschmaschine,WaschmaschineAdmin)
admin.site.register(Kuehlschrank,KuehlschrankAdmin)
admin.site.register(Spuelmaschine,SpuelmaschineAdmin)