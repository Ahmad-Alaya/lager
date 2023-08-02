from django.shortcuts import render, redirect, get_object_or_404
from inventory.models import *
from django.http import HttpResponse
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
from django.db.models import Max
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.contrib.auth.decorators import login_required



@login_required
def inventar_liste(request):
    # geräte = Gerät.objects.all().filter(anzahl__gt=0)
    waschmaschine = Waschmaschine.objects.all().filter(anzahl__gt=0)
    spuelmaschine = Spuelmaschine.objects.all().filter(anzahl__gt=0)
    kuehlschrank = Kuehlschrank.objects.all().filter(anzahl__gt=0)
    herdset = Herdset.objects.all().filter(anzahl__gt=0)
    herdplatte = Herdplatte.objects.all().filter(anzahl__gt=0)
    standherd = Standherd.objects.all().filter(anzahl__gt=0)
    trockner = Trockner.objects.all().filter(anzahl__gt=0)
    abzughaube = Abzughaube.objects.all().filter(anzahl__gt=0)
    sonst = Sonst.objects.all().filter(anzahl__gt=0)


    context = {
        # 'geräte': geräte,
        'waschmaschine':  waschmaschine,
        'spuelmaschine': spuelmaschine,
        'kuehlschrank': kuehlschrank,
        "herdset": herdset,
        "herdplatte":herdplatte,
        "standherd":standherd,
        "trockner":trockner,
        "abzughaube":abzughaube,
        "sonst":sonst,
    }

    return render(request, 'inventar_liste.html', context)

@login_required
def verkauf(request, id, type):
    type_maschine = None
    if type == 'geraete':
        type_maschine = get_object_or_404(Gerät, pk=id)
    elif type == 'waschmaschine':
        type_maschine = get_object_or_404(Waschmaschine, pk=id)
    elif type == 'kuehlschrank':
        type_maschine = get_object_or_404(Kuehlschrank, pk=id)
    elif type == 'spuelmaschine':
        type_maschine = get_object_or_404(Spuelmaschine, pk=id)
    elif type == 'herdset':
        type_maschine = get_object_or_404(Herdset, pk=id)
    elif type == 'herdplatte':
        type_maschine = get_object_or_404(Herdplatte, pk=id)
    elif type == 'standherd':
        type_maschine = get_object_or_404(Standherd, pk=id)
    elif type == 'trockner':
        type_maschine = get_object_or_404(Trockner, pk=id)
    elif type == 'abzughaube':
        type_maschine = get_object_or_404(Abzughaube, pk=id)
    elif type == 'sonst':
        type_maschine = get_object_or_404(Sonst, pk=id)


    if request.method == 'POST':
        anzahl = request.POST.get('anzahl')
        anzahl = int(anzahl)
        if type == 'geraete':
            gerät = get_object_or_404(Gerät, pk=id)
            type_maschine = gerät
            if anzahl > gerät.anzahl:
                return redirect('inventar_liste')
            elif anzahl == gerät.anzahl:
                verkauf = Verkauf.objects.create(gerät=gerät, verkäufer=request.user.username, type_of="gerät", menge=anzahl)
                gerät.delete()
            else:
                gerät.anzahl -= anzahl
                verkauf = Verkauf.objects.create(gerät=gerät, verkäufer=request.user.username,type_of="gerät", menge=anzahl)
                gerät.save()
            return redirect('verkauf_liste')

        elif type == 'waschmaschine':
            waschmaschine = get_object_or_404(Waschmaschine, pk=id)
            _update_inventar(waschmaschine, request, "Waschmaschine", anzahl)

        elif type == 'kuehlschrank':
            kuehlschrank = get_object_or_404(Kuehlschrank, pk=id)
            _update_inventar(kuehlschrank, request, "Kühlschrank", anzahl)

        elif type == 'spuelmaschine':
            spuelmaschine = get_object_or_404(Spuelmaschine, pk=id)
            _update_inventar(spuelmaschine, request, "Spülmaschine", anzahl)

        elif type == 'herdset':
            herdset = get_object_or_404(Herdset, pk=id)
            _update_inventar(herdset, request, "Herdset", anzahl)

        elif type == 'herdplatte':
            herdplatte = get_object_or_404(Herdplatte, pk=id)
            _update_inventar(herdplatte, request, "Herdplatte", anzahl)

        elif type == 'standherd':
            standherd = get_object_or_404(Standherd, pk=id)
            _update_inventar(standherd, request, "Standherd", anzahl)

        elif type == 'trockner':
            trockner = get_object_or_404(Trockner, pk=id)
            _update_inventar(trockner, request, "Trockner", anzahl)

        elif type == 'abzughaube':
            abzughaube = get_object_or_404(Abzughaube, pk=id)
            _update_inventar(abzughaube, request, "Abzughaube", anzahl)

        elif type == 'sonst':
            sonst = get_object_or_404(Sonst, pk=id)
            _update_inventar(sonst, request, "Sonst", anzahl)
        return redirect('verkauf_liste')

    rechnungs_nr = Verkauf.objects.aggregate(Max('rechnungs_nr'))['rechnungs_nr__max']  #todo send a list and check in html if value is unique

    all_waschmaschinen= json.dumps(list(Waschmaschine.objects.all().values()),cls=DjangoJSONEncoder)
    all_kuelschrank = json.dumps(list(Kuehlschrank.objects.all().values()), cls=DjangoJSONEncoder)
    all_spuelmaschinen = json.dumps(list(Spuelmaschine.objects.all().values()), cls=DjangoJSONEncoder)
    all_herdset = json.dumps(list(Herdset.objects.all().values()), cls=DjangoJSONEncoder)
    all_herdplatte = json.dumps(list(Herdplatte.objects.all().values()), cls=DjangoJSONEncoder)
    all_standherd = json.dumps(list(Standherd.objects.all().values()), cls=DjangoJSONEncoder)
    all_trockner = json.dumps(list(Trockner.objects.all().values()), cls=DjangoJSONEncoder)
    all_abzughaube = json.dumps(list(Abzughaube.objects.all().values()), cls=DjangoJSONEncoder)
    all_sonst = json.dumps(list(Sonst.objects.all().values()), cls=DjangoJSONEncoder)

    if not rechnungs_nr:
        rechnungs_nr = 0
    context = {
        'gerät': type_maschine,
        'rechnungsNr': int(rechnungs_nr)+1,
        'all_waschmaschinen':all_waschmaschinen,
        'all_kuelschrank':all_kuelschrank,
        'all_spuelmaschinen':all_spuelmaschinen,
        'all_herdset': all_herdset,
        'all_herdplatte': all_herdplatte,
        'all_standherd': all_standherd,
        'all_trockner': all_trockner,
        'all_abzughaube': all_abzughaube,
        'all_sonst': all_sonst,
    }
    return render(request, 'verkauf.html', context)

@login_required
def verkaufliste(request):
    if request.POST:

        verkauf_id = request.POST.get('verkauf_id')
        verkauf_obj = Verkauf.objects.get(id=verkauf_id)
        buyer_name = verkauf_obj.kunde_name
        buyer_street = verkauf_obj.kunde_strasse
        buyer_city = verkauf_obj.kunde_city
        rechnungsnummer = verkauf_obj.rechnungs_nr
        rechnungsdatum = (verkauf_obj.verkaufsdatum).strftime('%d.%m.%Y')
        falligkeitsdatum = "Sofort"
        menge = verkauf_obj.menge
        artikel_nr = verkauf_obj.artikel_nr
        serial_nr = verkauf_obj.serial_number
        preis = float(verkauf_obj.preis)


        einzel_preis, einzel_preis_german = _two_decimal_german(preis/1.19)
        end_preis, end_preis_german = _two_decimal_german(preis)

        zahlungsart = verkauf_obj.zahlungsart
        beschreibung = _wrap_text(verkauf_obj.beschreibung, max_length=58)
        beschreibung_SN = beschreibung + " SN: " + str(serial_nr)


        if verkauf_obj.beschreibung2:
            second_obj = True
            artikel_nr2 = verkauf_obj.artikel_nr2
            serial_nr2 = verkauf_obj.serial_number2
            preis2 = float(verkauf_obj.preis2)
            einzel_preis2, einzel_preis_german2 = _two_decimal_german(preis2 / 1.19)
            end_preis2, end_preis_german2 = _two_decimal_german(preis2)

            sum_einzel_preis, sum_einzel_preis_german  = _two_decimal_german(einzel_preis + einzel_preis2)
            sum_end_preis, sum_end_preis_german = _two_decimal_german(end_preis+end_preis2)

            beschreibung2 = _wrap_text(verkauf_obj.beschreibung2, max_length=58)
            beschreibung_SN2 = beschreibung2 + " SN: " + str(serial_nr2)



        # Create PDF
        file_name = "Sarahhandel_Rechnungsnr_" + str(rechnungsnummer) + ".pdf"
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename={file_name}'

        # pdf_name = f"{os.getcwd()}/invoice.pdf"
        c = canvas.Canvas(response, pagesize=letter)

        logo_path = f"{os.getcwd()}/logo.png"
        c.drawImage(logo_path, 440, 640, width=2 * inch, height=2 * inch)

        c.setFont("Helvetica-Bold", 18)
        c.drawString(45, 720, "Sarah Handel UG")
        c.setFont("Helvetica", 10)
        c.drawString(45, 698, "Dr. Maher Hababa")
        c.drawString(45, 684, "Carl-Troll-Straße 65, 53115 Bonn")
        #
        # # Add buyer information
        if not buyer_name:
            buyer_name = 'Bonn Kunde'
        c.setFont("Helvetica-Bold", 12)
        c.drawString(45, 578, buyer_name)
        c.setFont("Helvetica", 10)
        if not buyer_street:
            buyer_street = ' '
        c.drawString(45, 564, buyer_street)
        if not buyer_city:
            buyer_city = ' '
        c.drawString(45, 550, buyer_city)
        #
        # # Add invoice number and date
        # c.setFont("Helvetica-Bold", 14)
        c.drawString(394, 628, f"Rechnungsnummer : {rechnungsnummer}")
        c.drawString(395, 616, f"Rechnungsdatum    : {rechnungsdatum}")
        c.drawString(395, 604, f"Fälligkeitsdatum      : {falligkeitsdatum}")
        c.drawString(394, 592, f"Zahlungsart              : {zahlungsart}")
        #
        # # Define the table data and its specifications
        # if two object are available
        if second_obj:
            data = [
                ["Beschreibung", "Menge", "Artikel-Nr", "Einzelpreis", "USt. %", "Betrag"],
                [beschreibung_SN, f"{menge} Stk", artikel_nr, f"{einzel_preis_german}€", "19,00 %", f"{end_preis_german}€"],
                [beschreibung_SN2, f"{1} Stk", artikel_nr2, f"{einzel_preis_german2}€", "19,00 %", f"{end_preis_german2}€"],
            ]
        else:
            data = [
                ["Beschreibung", "Menge", "Artikel-Nr", "Einzelpreis", "USt. %", "Betrag"],
                [beschreibung_SN, f"{menge} Stk",
                 artikel_nr, f"{einzel_preis_german}€", "19,00 %", f"{end_preis_german}€"],
            ]

        story = []
        t = Table(data, colWidths=[312, 40, 55, 58, 55, 50])

        # Add table styles
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), '#0b5bb4'),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),  # added VALIGN attribute
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), "#cfe5f2"),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),  # added VALIGN attribute
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ])

        # Apply table style and draw the table
        t.setStyle(style)
        story.append(t)
        # Get table height and width
        table_width, table_height = t.wrap(0, 0)

        # Draw table on canvas
        x = (c._pagesize[0] - table_width) / 2
        y = (c._pagesize[1] - table_height) / 2
        t.drawOn(c, x, y)

        # todo draw a line between the table and the total amount

        neunzehn_prozent, neunzehn_prozent_german = _two_decimal_german(end_preis-einzel_preis)

        if second_obj:
            neunzehn_prozent2, neunzehn_prozent_german2 = _two_decimal_german(end_preis2 - einzel_preis2)
            sum_neunzehn_prozent, sum_neunzehn_prozent_german = _two_decimal_german(neunzehn_prozent+neunzehn_prozent2)

        # Draw total amount
        c.setFont("Helvetica-Bold", 10)
        c.drawRightString(500, 340, "Gesamt (netto):")
        c.drawRightString(500, 326, "19% USt.:")

        c.drawRightString(500, 312, "Gesamt (brutto):")
        if second_obj:
            c.drawRightString(590, 340, f"{sum_einzel_preis_german} €")
            c.drawRightString(590, 326, f"{sum_neunzehn_prozent_german} €")
            c.drawRightString(590, 312, f"{sum_end_preis_german} €")
        else:
            c.drawRightString(590, 340, f"{einzel_preis_german} €")
            c.drawRightString(590, 326, f"{neunzehn_prozent_german} €")
            c.drawRightString(590, 312, f"{end_preis_german} €")

        # todo draw a line obve the payment information
        c.line(45,66,585,66)
        # Draw payment information
        c.setFont("Helvetica-Bold", 10)
        c.drawString(45, 54, "Zahlungsinformationen:")
        c.setFont("Helvetica", 10)
        c.drawString(45, 42, "Bank: Kreissparkasse Köln")
        c.drawString(45, 30, "IBAN: DE43 3705 0299 0046 0246 84")
        c.drawString(45, 18, "BIC: COKSDE33XXX")

        c.setFont("Helvetica-Bold", 10)
        c.drawString(400, 54, "Kontaktinformation:")
        c.setFont("Helvetica", 10)
        c.drawString(400, 42, "E-Mail: sarahhandel@web.de")
        c.drawString(400, 30, "Mobile: 015736622934")
        c.drawString(400, 18, "Adresse: Carl-Troll-Str. 65, 53115 Bonn")

        c.save()
        print("PDF saved successfully!")
        return response


    verkauf_list = Verkauf.objects.all()
    return render(request, 'verkauf_liste.html', {'verkauf_list': verkauf_list})


def _wrap_text(text, max_length):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + 1 <= max_length:
            current_line += word + " "
        else:
            lines.append(current_line.strip())
            current_line = word + " "

    # Append the last line to the list
    if current_line:
        lines.append(current_line.strip())

    return "\n  ".join(lines)

def _update_inventar(model_obj, request, type_maschine , anzahl):
    type2 = request.POST.get('type2')
    if anzahl > model_obj.anzahl:
        return redirect('inventar_liste')
    elif anzahl == model_obj.anzahl:
        verkauf = _create_verkauf_object(model_obj, request, type_maschine, anzahl)
        model_obj.delete()
        verkauf.save()
        # check if second product exists
        if type2:
            id2 = request.POST.get('Id2')
            if type2 == 'waschmaschine':
                waschmaschine = get_object_or_404(Waschmaschine, pk=id2)
                _update_inventar_2_product(verkauf, waschmaschine, request, "Waschmaschine", anzahl)

            elif type2 == 'kuehlschrank':
                kuehlschrank = get_object_or_404(Kuehlschrank, pk=id2)
                _update_inventar_2_product(verkauf, kuehlschrank, request, "Kühlschrank", anzahl)

            elif type2 == 'spuelmaschine':
                spuelmaschine = get_object_or_404(Spuelmaschine, pk=id2)
                _update_inventar_2_product(verkauf, spuelmaschine, request, "Spülmaschine", anzahl)

            elif type2 == 'herdset':
                herdset = get_object_or_404(Herdset, pk=id2)
                _update_inventar_2_product(verkauf, herdset, request, "Herdset", anzahl)

            elif type2 == 'herdplatte':
                herdplatte = get_object_or_404(Herdplatte, pk=id2)
                _update_inventar_2_product(verkauf, herdplatte, request, "Herdplatte", anzahl)

            elif type2 == 'standherd':
                standherd = get_object_or_404(Standherd, pk=id2)
                _update_inventar_2_product(verkauf, standherd, request, "Standherd", anzahl)

            elif type2 == 'trockner':
                trockner = get_object_or_404(Trockner, pk=id2)
                _update_inventar_2_product(verkauf, trockner, request, "Trockner", anzahl)

            elif type2 == 'abzughaube':
                abzughaube = get_object_or_404(Abzughaube, pk=id2)
                _update_inventar_2_product(verkauf, abzughaube, request, "Abzughaube", anzahl)

            elif type2 == 'sonst':
                sonst = get_object_or_404(Sonst, pk=id2)
                _update_inventar_2_product(verkauf, sonst, request, "Sonst", anzahl)
    else:
        model_obj.anzahl -= anzahl
        verkauf = _create_verkauf_object(model_obj, request, type_maschine, anzahl)
        model_obj.save()
        verkauf.save()
        # check if second product exists
        if type2:
            id2 = request.POST.get('Id2')
            if type2 == 'waschmaschine':
                waschmaschine = get_object_or_404(Waschmaschine, pk=id2)
                _update_inventar_2_product(verkauf, waschmaschine, request, "Waschmaschine", 1)

            elif type2 == 'kuehlschrank':
                kuehlschrank = get_object_or_404(Kuehlschrank, pk=id2)
                _update_inventar_2_product(verkauf, kuehlschrank, request, "Kühlschrank", 1)

            elif type2 == 'spuelmaschine':
                spuelmaschine = get_object_or_404(Spuelmaschine, pk=id2)
                _update_inventar_2_product(verkauf, spuelmaschine, request, "Spülmaschine", 1)

            elif type2 == 'herdset':
                herdset = get_object_or_404(Herdset, pk=id2)
                _update_inventar_2_product(verkauf, herdset, request, "Herdset", 1)

            elif type2 == 'herdplatte':
                herdplatte = get_object_or_404(Herdplatte, pk=id2)
                _update_inventar_2_product(verkauf, herdplatte, request, "Herdplatte", 1)

            elif type2 == 'standherd':
                standherd = get_object_or_404(Standherd, pk=id2)
                _update_inventar_2_product(verkauf, standherd, request, "Standherd", 1)

            elif type2 == 'trockner':
                trockner = get_object_or_404(Trockner, pk=id2)
                _update_inventar_2_product(verkauf, trockner, request, "Trockner", 1)

            elif type2 == 'abzughaube':
                abzughaube = get_object_or_404(Abzughaube, pk=id2)
                _update_inventar_2_product(verkauf, abzughaube, request, "Abzughaube", 1)

            elif type2 == 'sonst':
                sonst = get_object_or_404(Sonst, pk=id2)
                _update_inventar_2_product(verkauf, sonst, request, "Sonst", 1)

    return redirect('verkauf_liste')

def _create_verkauf_object(model_obj, request, type_maschine, anzahl):
    verkauf_obj = Verkauf.objects.create(
                    waschmaschine=model_obj,
                    type_of=type_maschine,
                    menge=anzahl,
                    verkäufer=request.user.username,
                    zahlungsart=request.POST.get('zahlungsart'),
                    verkaufsdatum=request.POST.get('verkaufsdatum'),
                    marke=request.POST.get('marke'),
                    model=request.POST.get('model'),
                    serial_number=request.POST.get('serial_number'),
                    artikel_nr=request.POST.get('artikel_nr'),
                    preis=float(request.POST.get('preis'))*float(anzahl),
                    beschreibung=request.POST.get('beschreibung'),
                    rechnungs_nr=request.POST.get('rechnungs_nr'),
                    kunde_name=request.POST.get('kunde_name'),
                    kunde_strasse=request.POST.get('kunde_strasse'),
                    kunde_plz=request.POST.get('kunde_plz'),
                    kunde_city=request.POST.get('kunde_city'),
                    kunde_email=request.POST.get('kunde_email'),
                    kunde_mobile=request.POST.get('kunde_mobile'),
                )
    return verkauf_obj

def _update_inventar_2_product(verkauf_obj, model_obj, request, type_maschine , anzahl):
    if anzahl > model_obj.anzahl:
        return redirect('inventar_liste')
    elif anzahl == model_obj.anzahl:
        verkauf = _update_verkauf_for_obj2(verkauf_obj, model_obj, request, type_maschine, anzahl)
        model_obj.delete()
        verkauf.save()
    else:
        model_obj.anzahl -= anzahl
        verkauf = _update_verkauf_for_obj2(verkauf_obj, model_obj, request, type_maschine, anzahl)
        model_obj.save()
        verkauf.save()


def _update_verkauf_for_obj2(verkauf_obj, model_obj, request, type_maschine, anzahl):
    verkauf_obj.type_of2 = type_maschine
    verkauf_obj.menge2 = anzahl

    if request.POST.get('marke2'):
        verkauf_obj.marke2 = request.POST.get('marke2')

    if request.POST.get('model2'):
        verkauf_obj.model2 = request.POST.get('model2')

    if request.POST.get('seriennummer2'):
        verkauf_obj.serial_number2 = request.POST.get('seriennummer2')

    if request.POST.get('artikelnummer2'):
        verkauf_obj.artikel_nr2 = request.POST.get('artikelnummer2')

    if request.POST.get('beschreibung2'):
        verkauf_obj.beschreibung2 = request.POST.get('beschreibung2')

    if not request.POST.get('preis2'):
        verkauf_obj.preis2 = float(0.0)
        verkauf_obj.final_preis = verkauf_obj.preis + verkauf_obj.preis2

    return verkauf_obj


def _two_decimal_german(float_number):
    x = f"{float_number:.2f}"
    two_decimal = float(x)
    german_format = x.replace(".", ",")
    return two_decimal, german_format