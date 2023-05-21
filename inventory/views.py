from django.shortcuts import render, redirect, get_object_or_404
from inventory.models import *

def inventar_liste(request):
    geräte = Gerät.objects.all().filter(anzahl__gt=0)
    waschmaschine = Waschmaschine.objects.all().filter(anzahl__gt=0)
    spuelmaschine = Spuelmaschine.objects.all().filter(anzahl__gt=0)
    kuehlschrank = Kuehlschrank.objects.all().filter(anzahl__gt=0)
    context = {
        'geräte': geräte,
        'waschmaschine':  waschmaschine,
        'spuelmaschine': spuelmaschine,
        'kuehlschrank': kuehlschrank,}

    return render(request, 'inventar_liste.html', context)

def verkauf(request, id, type):
    type_maschine = None
    if request.method == 'POST':
        anzahl = request.POST.get('anzahl')
        anzahl = int(anzahl)
        if type == 'geraete':
            gerät = get_object_or_404(Gerät, pk=id)
            type_maschine = gerät
            if anzahl > gerät.anzahl:
                return redirect('inventar_liste')
            elif anzahl == gerät.anzahl:
                verkauf = Verkauf.objects.create(gerät=gerät, verkäufer=request.user.username)
                gerät.delete()
            else:
                gerät.anzahl -= anzahl
                verkauf = Verkauf.objects.create(gerät=gerät, verkäufer=request.user.username)
                gerät.save()
            return redirect('verkauf_liste')

        elif type == 'waschmaschine':
            waschmaschine = get_object_or_404(Waschmaschine, pk=id)
            type_maschine = waschmaschine
            if anzahl > waschmaschine.anzahl:
                return redirect('inventar_liste')
            elif anzahl == waschmaschine.anzahl:
                verkauf = Verkauf.objects.create(waschmaschine=waschmaschine, verkäufer=request.user.username)
                waschmaschine.delete()
            else:
                waschmaschine.anzahl -= anzahl
                verkauf = Verkauf.objects.create(waschmaschine=waschmaschine, verkäufer=request.user.username)
                waschmaschine.save()
            return redirect('verkauf_liste')

        elif type == 'kuehlschrank':
            kuehlschrank = get_object_or_404(Kuehlschrank, pk=id)
            type_maschine = kuehlschrank
            if anzahl > kuehlschrank.anzahl:
                return redirect('inventar_liste')
            elif anzahl == kuehlschrank.anzahl:
                verkauf = Verkauf.objects.create(kuhlschrank=kuehlschrank, verkäufer=request.user.username)
                kuehlschrank.delete()
            else:
                kuehlschrank.anzahl -= anzahl
                verkauf = Verkauf.objects.create(kuhlschrank=kuehlschrank, verkäufer=request.user.username)
                kuehlschrank.save()
            return redirect('verkauf_liste')

        elif type == 'spuelmaschine':
            spuelmaschine = get_object_or_404(Spuelmaschine, pk=id)
            type_maschine = spuelmaschine
            if anzahl > spuelmaschine.anzahl:
                return redirect('inventar_liste')
            elif anzahl == spuelmaschine.anzahl:
                verkauf = Verkauf.objects.create(spuelmaschine=spuelmaschine, verkäufer=request.user.username)
                spuelmaschine.delete()
            else:
                spuelmaschine.anzahl -= anzahl
                verkauf = Verkauf.objects.create(spuelmaschine=spuelmaschine, verkäufer=request.user.username)
                spuelmaschine.save()
            return redirect('verkauf_liste')

    context = {'gerät': type_maschine}
    return render(request, 'verkauf.html', context)

def verkaufliste(request):
    verkauf_list = Verkauf.objects.all()
    return render(request, 'verkauf_liste.html', {'verkauf_list': verkauf_list})


