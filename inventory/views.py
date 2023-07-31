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
from datetime import datetime

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
    if type == 'geraete':
        type_maschine = get_object_or_404(Gerät, pk=id)
    elif type == 'waschmaschine':
        type_maschine = get_object_or_404(Waschmaschine, pk=id)
    elif type == 'kuehlschrank':
        type_maschine = get_object_or_404(Kuehlschrank, pk=id)
    elif type == 'spuelmaschine':
        type_maschine = get_object_or_404(Spuelmaschine, pk=id)


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
            type_maschine = waschmaschine
            if anzahl > waschmaschine.anzahl:
                return redirect('inventar_liste')
            elif anzahl == waschmaschine.anzahl:
                verkauf = Verkauf.objects.create(
                    waschmaschine=waschmaschine,
                    type_of="Waschmaschine",
                    menge=anzahl,
                    verkäufer=request.user.username,
                    zahlungsart=request.POST.get('zahlungsart'),
                    verkaufsdatum=request.POST.get('verkaufsdatum'),
                    marke=request.POST.get('marke'),
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
                waschmaschine.delete()
                verkauf.save()
            else:
                waschmaschine.anzahl -= anzahl
                verkauf = Verkauf.objects.create(
                    waschmaschine=waschmaschine,
                    type_of="Waschmaschine",
                    menge=anzahl,
                    verkäufer=request.user.username,
                    zahlungsart=request.POST.get('zahlungsart'),
                    verkaufsdatum=request.POST.get('verkaufsdatum'),
                    marke= request.POST.get('marke'),
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
                waschmaschine.save()
                verkauf.save()
            return redirect('verkauf_liste')

        elif type == 'kuehlschrank':
            kuehlschrank = get_object_or_404(Kuehlschrank, pk=id)
            type_maschine = kuehlschrank
            if anzahl > kuehlschrank.anzahl:
                return redirect('inventar_liste')
            elif anzahl == kuehlschrank.anzahl:
                verkauf = Verkauf.objects.create(
                    kuhlschrank=kuehlschrank,
                    type_of="Kühlschrank",
                    menge=anzahl,
                    verkäufer=request.user.username,
                    zahlungsart=request.POST.get('zahlungsart'),
                    verkaufsdatum=request.POST.get('verkaufsdatum'),
                    marke=request.POST.get('marke'),
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
                kuehlschrank.delete()
                verkauf.save()
            else:
                kuehlschrank.anzahl -= anzahl
                verkauf = Verkauf.objects.create(
                    kuhlschrank=kuehlschrank,
                    type_of="Kühlschrank",
                    menge=anzahl,
                    verkäufer=request.user.username,
                    zahlungsart=request.POST.get('zahlungsart'),
                    verkaufsdatum=request.POST.get('verkaufsdatum'),
                    marke=request.POST.get('marke'),
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
                kuehlschrank.save()
                verkauf.save()
            return redirect('verkauf_liste')

        elif type == 'spuelmaschine':
            spuelmaschine = get_object_or_404(Spuelmaschine, pk=id)
            type_maschine = spuelmaschine
            if anzahl > spuelmaschine.anzahl:
                return redirect('inventar_liste')
            elif anzahl == spuelmaschine.anzahl:
                verkauf = Verkauf.objects.create(
                    spuelmaschine=spuelmaschine,
                    type_of="Spülmaschine",
                    menge=anzahl,
                    verkäufer=request.user.username,
                    zahlungsart=request.POST.get('zahlungsart'),
                    verkaufsdatum=request.POST.get('verkaufsdatum'),
                    marke=request.POST.get('marke'),
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
                spuelmaschine.delete()
                verkauf.save()
            else:
                spuelmaschine.anzahl -= anzahl
                verkauf = Verkauf.objects.create(
                    spuelmaschine=spuelmaschine,
                    type_of="Spülmaschine",
                    menge=anzahl,
                    verkäufer=request.user.username,
                    zahlungsart=request.POST.get('zahlungsart'),
                    verkaufsdatum=request.POST.get('verkaufsdatum'),
                    marke=request.POST.get('marke'),
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
                spuelmaschine.save()
                verkauf.save()
            return redirect('verkauf_liste')

    rechnungs_nr = Verkauf.objects.aggregate(Max('rechnungs_nr'))['rechnungs_nr__max']
    if not rechnungs_nr:
        rechnungs_nr = 0
    context = {'gerät': type_maschine, 'rechnungsNr': int(rechnungs_nr)+1}
    return render(request, 'verkauf.html', context)

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
        betrag = float(verkauf_obj.preis)
        einzel_preis_tmp = betrag/1.19  # todo use , instaed .
        einzel_preis = f"{einzel_preis_tmp:.2f}"
        einzel_preis_formatted = str(einzel_preis).replace(".",",")

        betrag_foramatted = f"{betrag:.2f}".replace(".",",")
        zahlungsart = verkauf_obj.zahlungsart
        # "Item 1 WAMA Beko FSM 67320 Edelstahl 60 cm Item 1 WAMA Beko FSM\n 67320 Edelstahl 60 cm"
        beschreibung = _wrap_text(verkauf_obj.beschreibung, max_length=58)
        beschreibung_SN = beschreibung + " SN: " + str(serial_nr)

        # Create PDF
        file_name = "Sarahhandel_Rechnungsnr_" + str(rechnungsnummer) + ".pdf"
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename={file_name}'

        # pdf_name = f"{os.getcwd()}/invoice.pdf"
        c = canvas.Canvas(response, pagesize=letter)

        logo_path = f"{os.getcwd()}/logo.png"
        c.drawImage(logo_path, 240, 660, width=2 * inch, height=2 * inch)

        c.setFont("Helvetica-Bold", 12)
        c.drawString(45, 650, "Sarah Handel UG")
        c.setFont("Helvetica", 10)
        c.drawString(45, 638, "Dr. Maher Hababa")
        c.drawString(45, 628, "Carl-Troll-Straße 65, 53115 Bonn")
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
        data = [
            ["Beschreibung", "Menge", "Artikel-Nr", "Einzelpreis", "USt. %", "Betrag"],
            [beschreibung_SN, f"{menge} Stk",
             artikel_nr, f"{einzel_preis_formatted}€", "19,00 %", f"{betrag_foramatted}€"],
        ]
        story = []
        t = Table(data, colWidths=[312, 40, 55, 58, 55, 50])

        # Add table styles
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), '#9099ab'),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),  # added VALIGN attribute
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), "#cae3d8"),
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
        # german format
        neunzehn_prozent = betrag - float(einzel_preis)
        neunzehn_prozent = f"{neunzehn_prozent:.2f}"
        neunzehn_prozent_formatted = neunzehn_prozent.replace(".",",")

        # Draw total amount
        c.setFont("Helvetica-Bold", 10)
        c.drawRightString(500, 340, "Gesamt (netto):")
        c.drawRightString(500, 326, "19% USt.:")
        c.drawRightString(500, 312, "Gesamt (brutto):")

        c.drawRightString(590, 340, f"{einzel_preis_formatted} €")
        c.drawRightString(590, 326, f"{neunzehn_prozent_formatted} €")
        c.drawRightString(590, 312, f"{betrag_foramatted} €")

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


