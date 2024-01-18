from django.core.mail import EmailMessage
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
from django.contrib import messages
import pandas as pd
import io
from decouple import config

@login_required
def inventar_liste(request):
    # geräte = Gerät.objects.all().filter(anzahl__gt=0)
    waschmaschine = Waschmaschine.objects.all().filter(anzahl__gt=0)
    spuelmaschine = Spuelmaschine.objects.all().filter(anzahl__gt=0)
    kuehlschrank = Kuehlschrank.objects.all().filter(anzahl__gt=0)
    herdset = Herdset.objects.all().filter(anzahl__gt=0)
    herdplatte = Herdplatte.objects.all().filter(anzahl__gt=0)
    standherd = Standherd.objects.all().filter(anzahl__gt=0)
    backofen = Backofen.objects.all().filter(anzahl__gt=0)
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
        "backofen":backofen,
        "trockner":trockner,
        "abzughaube":abzughaube,
        "sonst":sonst,
    }

    return render(request, 'inventar_liste.html', context)


@login_required
def storniere_rechnung(request):
    if request.POST:
        if "rechnung_erstellen" in request.POST:
            nummer = Storno.objects.aggregate(Max('nummer'))['nummer__max']
            if not nummer: # for the first time
                nummer = 0
            # nummer +=1 todo
            second_obj = False

            beschreibung1 = request.POST.get("beschreibung1"),
            preis1 = float(request.POST.get("preis1")),
            erstattung1 = float(request.POST.get("erstattung1")),
            menge = float(request.POST.get("menge"))
            artikel_nr = request.POST.get("artikel_nr")

            if request.POST.get("storno_fuer") == "second":
                beschreibung1 = request.POST.get("beschreibung2"),
                preis1 = float(request.POST.get("preis2")),
                erstattung1 = float(request.POST.get("erstattung2")),
                artikel_nr = request.POST.get("artikel_nr2")

            elif request.POST.get("storno_fuer") == "both":
                second_obj = True

            if isinstance(erstattung1, tuple):
                erstattung1 = list(erstattung1)[0]

            if isinstance(preis1, tuple):
                preis1 = list(preis1)[0]
            if isinstance(beschreibung1, tuple):
                beschreibung1 = list(beschreibung1)[0]

            storno_obj = Storno.objects.create(
                zahlungsart=request.POST.get("zahlungsart"),
                stornierungsdatum=request.POST.get("stornierungsdatum"),
                final_erstattung=float(request.POST.get("final_erstattung")),
                stornierte_rechnung=request.POST.get("stornierte_rechnung"),
                nummer=nummer + 1,

                kunde_name=request.POST.get("kunde_name"),
                kunde_strasse=request.POST.get("kunde_strasse"),
                kunde_plz=request.POST.get("kunde_plz"),
                kunde_city=request.POST.get("kunde_city"),

                beschreibung1=beschreibung1,
                preis1=float(preis1),
                erstattung1=float(erstattung1),
                menge=float(menge),
                artikel_nr=artikel_nr

            )
            if second_obj:
                beschreibung2 = request.POST.get("beschreibung2")
                preis2 = float(request.POST.get("preis2"))
                erstattung2 = float(request.POST.get("erstattung2"))

                storno_obj.beschreibung2 = beschreibung2,
                storno_obj.preis2 = preis2,
                storno_obj.erstattung2 = erstattung2,
                storno_obj.artikel_nr2 = request.POST.get("artikel_nr2")

                if isinstance(storno_obj.erstattung2, tuple):
                    storno_obj.erstattung2 = list(storno_obj.erstattung2)[0]

                if isinstance(storno_obj.beschreibung2, tuple):
                    storno_obj.beschreibung2 = list(storno_obj.beschreibung2)[0]

                if isinstance(storno_obj.preis2, tuple):
                    storno_obj.preis2 = list(storno_obj.preis2)[0]
                storno_obj.save()
            c,response = generate_storno_pdf(storno_obj.id, operation_mode='inline')
            c.save()
            return redirect("storno_liste")

        rechnung_nummer = int(request.POST.get("storno_rechnung_nr"))
        rechnung = Verkauf.objects.get(rechnungs_nr=rechnung_nummer)
        final_erstattung = rechnung.final_preis
        kunde_name = rechnung.kunde_name
        kunde_city = rechnung.kunde_city
        kunde_strasse = rechnung.kunde_strasse
        kunde_plz = rechnung.kunde_plz
        beschreibung1 = rechnung.beschreibung
        preis1 = rechnung.preis
        menge = rechnung.menge
        artikel_nr = rechnung.artikel_nr
        beschreibung2 = rechnung.beschreibung2
        preis2 = rechnung.preis2
        artikel_nr2 = rechnung.artikel_nr2


        context = {
            "rechnung_nummer": rechnung_nummer,
            "final_erstattung": final_erstattung,
            "kunde_name": kunde_name,
            "kunde_city": kunde_city,
            "kunde_strasse": kunde_strasse,
            "kunde_plz": kunde_plz,
            "beschreibung1": beschreibung1,
            "preis1": preis1,
            "menge": menge,
            "artikel_nr": artikel_nr,
            "beschreibung2": beschreibung2,
            "preis2": preis2,
            "artikel_nr2": artikel_nr2,
        }
        return render(request, 'storniere_rechnung.html', context)

    return render(request, 'storniere_rechnung.html',{})


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
    elif type == 'backofen':
        type_maschine = get_object_or_404(Backofen, pk=id)
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

        elif type == 'backofen':
            backofen = get_object_or_404(Backofen, pk=id)
            _update_inventar(backofen, request, "Backofen", anzahl)

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
    all_backofen = json.dumps(list(Backofen.objects.all().values()), cls=DjangoJSONEncoder)
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
        'all_backofen': all_backofen,
        'all_trockner': all_trockner,
        'all_abzughaube': all_abzughaube,
        'all_sonst': all_sonst,
    }
    return render(request, 'verkauf.html', context)

@login_required
def verkaufliste(request):
    if request.POST:


        operation_mode = 'attachment'
        if 'anzeigen' in request.POST:
            operation_mode = 'inline'

        verkauf_id = request.POST.get('verkauf_id')

        if 'anzeigen' in request.POST or 'herunterladen' in request.POST:
            c,response = generate_pdf(verkauf_id, operation_mode)
            c.save()
            print("PDF saved successfully!")
            return response

        if request.POST.get("send_email"):
            request.session['verkauf_id'] = verkauf_id
            return redirect("send_email")

        if request.POST.get("submit_bezahlt"):
            verk_obj = Verkauf.objects.get(id=verkauf_id)
            verk_obj.bezahlt = request.POST.get("bezahlt")
            if request.POST.get("bezahlt") == "Nein" or request.POST.get("bezahlt") == "---":
                verk_obj.zahlungsdatum = None
            verk_obj.save()

        if request.POST.get("submit_zahlungsdatum"):
            verk_obj = Verkauf.objects.get(id=verkauf_id)
            if datetime.strptime(request.POST.get("zahlungsdatum"), "%Y-%m-%d") > datetime.now():
                messages.error(request, "Wrong date, you can not pay in the future")
            else:
                verk_obj.zahlungsdatum = request.POST.get("zahlungsdatum")
                verk_obj.bezahlt = "Ja"
                verk_obj.save()


    verkauf_list = Verkauf.objects.all()
    return render(request, 'verkauf_liste.html', {'verkauf_list': verkauf_list})


@login_required
def stornoliste(request):

    if request.POST:
        operation_mode = 'attachment'
        if 'anzeigen' in request.POST:
            operation_mode = 'inline'
        storno_id = request.POST.get('storno_id')

        if 'anzeigen' in request.POST or 'herunterladen' in request.POST:
            c,response = generate_storno_pdf(request.POST.get("storno_id"), operation_mode)
            c.save()
            print("PDF saved successfully!")
            return response

        if request.POST.get("send_email"):
            request.session['storno_id'] = storno_id
            return redirect("send_email")



    storno_list = Storno.objects.all()
    return render(request, 'storno_liste.html', {'storno_list': storno_list})

@login_required
def send_email(request):
    verkauf_id = request.session.get('verkauf_id')
    if request.POST:

        kunde_email = str(request.POST.get('email'))
        message = request.POST.get('message')
        subject = request.POST.get('subject')
        # Handle the uploaded PDF file

        # pdf_file = request.FILES.get('pdf_file')
        # pdf_content = pdf_file.read()
        c, pdf_response = generate_pdf(verkauf_id, operation_mode='attachment')
        c.save()
        if request.POST.get('kopie_mail') == 'on':
            reciver_mail = [kunde_email,'sarahhandel@web.de']
        else:
            reciver_mail = [kunde_email]
        email_obj = EmailMessage(subject, message, config('EMAIL_HOST_USER'), reciver_mail)
        # witz :) ersetze erste param to 'Rechnung'
        email_obj.attach(pdf_response.headers._store.get('content-disposition')[1].split("=")[1], pdf_response.content, 'application/pdf')
        try:
            # Attempt to send the email
            success_count = email_obj.send(fail_silently=False)

            if success_count > 0:
                messages.success(request, 'Email sent successfully!')
            else:
                messages.error(request, 'Failed to send email. Please try again later.')

            return redirect('verkauf_liste')

        except Exception as e:
            messages.error(request, f'An error occurred while sending the email: {str(e)}')
            return redirect('verkauf_liste')


    else:

        verkauf_obj = Verkauf.objects.get(id=verkauf_id)
        kunde_email = verkauf_obj.kunde_email
        if not kunde_email:
            kunde_email = " "
        message = "BITTE ANTWORTEN SIE NICHT AUF DIESE EMAIL\n" \
                  "Sehr geehrte Damen und Herren,\n\nvielen Dank für Ihren Einkauf.\n\n" \
                  "Anbei finden Sie die Rechnung für Ihren Einkauf.\n\n" \
                  "Bitte zögern Sie nicht, sich bei uns zu melden, falls Sie Fragen oder Anmerkungen haben." \
                  " Wir stehen Ihnen gerne zur Verfügung, um Ihnen weiterzuhelfen.\n\n" \
                  "Wir freuen uns auf Ihre Bewertung und hoffen, Sie bald wieder bei uns begrüßen zu dürfen.\n\n" \
                  "https://maps.app.goo.gl/jgxZXcNxKi3G23M8A\n\n" \
                  "Mit freundlichen Grüßen\n" \
                  "Sarahhandel UG\n" \
                  "für Rückfragen schreiben Sie uns bitte auf sarahhandel@web.de"

        subject = "Rechnung"
    context = {
        'subject': subject,
        'message': message,
        'email': kunde_email,
        'rechnung_pdf': 'pdf_response',
    }
    return render(request, 'email_preview.html',context)

@login_required
def statistic(request):
    context = {}

    if request.POST:
        date_from = datetime.strptime(request.POST.get("dateFrom"), "%Y-%m-%d")
        date_to = datetime.strptime(request.POST.get("dateTo"), "%Y-%m-%d")
        date_to = date_to.replace(hour=23, minute=59, second=59)
        payment_type = request.POST.get("paymentType")

        if payment_type == "Bar":
            verkauf_queryset = Verkauf.objects.filter(
                verkaufsdatum__range=(date_from, date_to),
                zahlungsart="Bar"
            )
        elif payment_type == "Beide":
            verkauf_queryset = Verkauf.objects.filter(
                verkaufsdatum__range=(date_from, date_to),
            )
        else:
            verkauf_queryset = Verkauf.objects.filter(
                verkaufsdatum__range=(date_from, date_to),
                zahlungsart__in=["Karte", "Überweisung"]
            )

        data = []
        summe_rechnungen = 0
        for verkauf in verkauf_queryset:
            summe_rechnungen += verkauf.final_preis

            formatted_date = verkauf.verkaufsdatum.strftime('%d.%m.%Y')
            formatted_betrag = "{:,.2f}".format(verkauf.final_preis).replace('.', ',')

            data.append({
                'Beleg-Nr.': verkauf.rechnungs_nr,
                'Datum': formatted_date,
                'Text': "",
                "Vorsteur": "",
                'Betrag': formatted_betrag
            })

        df = pd.DataFrame(data)

        context["summe"] = "{:,.2f}".format(summe_rechnungen)
        context["stk"] = len(verkauf_queryset)

        # Check if "Show Me Detail" button was clicked
        if 'show_detail' in request.POST:
            # Generate the table from the df dataframe
            table_headers = df.columns.tolist()
            table_data = df.values.tolist()
            context['table'] = {
                'headers': table_headers,
                'data': table_data
            }

        # Check if "Export to Excel" button was clicked
        if 'export_excel' in request.POST:
            # Convert DataFrame to Excel
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Sheet1')
            output.seek(0)

            # Serve the Excel file as a response
            response = HttpResponse(output.read(),
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="bericht.xlsx"'
            return response

    return render(request, 'statistic.html', context)


@login_required
# not implemented yet
def inventar_rechner(request):
    waschmaschienen = Waschmaschine.objects.all()
    kuehlschraenke = Kuehlschrank.objects.all()
    trockner = Trockner.objects.all()
    herdsets = Herdset.objects.all()
    herdplatte = Herdplatte.objects.all()
    backofen = Backofen.objects.all()
    standherd = Standherd.objects.all()
    spuelmaschine = Spuelmaschine.objects.all()
    sonst = Sonst.objects.all()
    abzughaube = Abzughaube.objects.all()
    Kategorien = [waschmaschienen, kuehlschraenke, trockner, herdsets, herdplatte, backofen, standherd, spuelmaschine,
                  sonst,
                  abzughaube]

    statistic_dict = {}
    missing_data = []
    for Kategorie in Kategorien:
        category_name = Kategorie.model._meta.model_name
        statistic_dict[category_name] = {}

        for obj in Kategorie:
            model_name = str(obj.model)
            if obj.Kauf_preis:
                kauf_preis = obj.Kauf_preis
                anzahl = obj.anzahl
                statistic_dict[category_name][model_name] = {'kauf_preis': kauf_preis,
                                                             'anzahl': anzahl,
                                                             'total_preis': float(kauf_preis) * float(anzahl)}
            else:
                link = f"/admin/inventory/{Kategorie.model._meta.model_name}/{obj.id}/change/"
                missing_data.append((Kategorie.model._meta.model_name, model_name, obj, link))

    total_all_total_preis = 0
    total_all_total_amount = 0
    for category, models in statistic_dict.items():
        total_preis = sum(model_data['total_preis'] for model_data in models.values())
        total_amount = sum(model_data['anzahl'] for model_data in models.values())
        models['total_preis'] = round(total_preis, 2)
        models['total_amount'] = total_amount
        total_all_total_preis += total_preis
        total_all_total_amount += total_amount

    context = {'statistic_dict': statistic_dict,
               'total_all_total_preis': round(total_all_total_preis, 2),
               'total_all_total_amount': total_all_total_amount,
               'missing_data': missing_data,
               }
    return render(request, 'inventar_rechner.html', context)

def generate_storno_pdf(id:int, operation_mode: str = 'attachment'):
    storno_obj = Storno.objects.get(id=id)
    second_obj = False
    if storno_obj.beschreibung2:
        second_obj = True

    buyer_name = storno_obj.kunde_name
    buyer_street =storno_obj.kunde_strasse
    buyer_city =storno_obj.kunde_city
    buyer_zip =storno_obj.kunde_plz
    stornierungsdatum = storno_obj.stornierungsdatum
    if isinstance(stornierungsdatum, str):
        stornierungsdatum = datetime.strptime(stornierungsdatum, '%Y-%m-%d')
    stornierungsdatum = stornierungsdatum.strftime('%d.%m.%Y')
    stornierte_rechnung = storno_obj.stornierte_rechnung
    zahlungsart = storno_obj.zahlungsart
    beschreibung1 = storno_obj.beschreibung1
    menge = storno_obj.menge
    artikel_nr = storno_obj.artikel_nr

    einzel_preis, einzel_preis_german = _two_decimal_german((-1*float(storno_obj.erstattung1)) / 1.19)
    end_preis, end_preis_german = _two_decimal_german(-1*float(storno_obj.erstattung1))

    if second_obj:
        beschreibung2 = storno_obj.beschreibung2
        artikel_nr2 = storno_obj.artikel_nr2

        if isinstance(storno_obj.erstattung2, tuple):
            einzel_preis2, einzel_preis_german2 = _two_decimal_german((-1*float(storno_obj.erstattung2[0])) / 1.19)
            end_preis2, end_preis_german2 = _two_decimal_german(-1* float(storno_obj.erstattung2[0]))
        else:
            einzel_preis2, einzel_preis_german2 = _two_decimal_german((-1 * float(storno_obj.erstattung2)) / 1.19)
            end_preis2, end_preis_german2 = _two_decimal_german(-1 * float(storno_obj.erstattung2))


        sum_einzel_preis, sum_einzel_preis_german = _two_decimal_german(einzel_preis + einzel_preis2)
        sum_end_preis, sum_end_preis_german = _two_decimal_german(end_preis + end_preis2)

    # Create PDF
    file_name = "Stornorechnung" + str(storno_obj.nummer) + ".pdf"
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'{operation_mode}; filename={file_name}'

    # pdf_name = f"{os.getcwd()}/invoice.pdf"
    c = canvas.Canvas(response, pagesize=letter)

    logo_path = f"{os.getcwd()}/lager/logo.png"
    try:
        c.drawImage(logo_path, 440, 640, width=2 * inch, height=2 * inch)
    except:
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
    c.setFont("Helvetica-Bold", 16)
    c.drawString(23, 460, "Stornorechnung")
    c.setFont("Helvetica", 10)
    # c.drawString(23, 445, zusaetzlich)

    if not buyer_street:
        buyer_street = ' '
    c.drawString(45, 564, buyer_street)
    if not buyer_city:
        buyer_city = ' '
    if not buyer_zip:
        buyer_zip = ' '
    adress = buyer_zip + ' ' + buyer_city
    c.drawString(45, 550, adress)
    #
    # # Add invoice number and date
    # c.setFont("Helvetica-Bold", 14)
    c.drawString(393, 628, f"Stornonummer            : St-{storno_obj.nummer}")
    c.drawString(394, 616, f"Stornierungsdatum     : {stornierungsdatum}")
    c.drawString(394, 604, f"Stornierterechnung     : {stornierte_rechnung}")
    c.drawString(393, 592, f"Zahlungsart                 : {zahlungsart}")
    #
    # # Define the table data and its specifications
    # if two object are available
    if second_obj:
        data = [
            ["Beschreibung", "Menge", "Artikel-Nr", "Einzelpreis", "USt. %", "Betrag"],
            [beschreibung1, f"{int(menge)} Stk", artikel_nr, f"{einzel_preis_german}€", "19,00 %", f"{end_preis_german}€"],
            [beschreibung2, f"{1} Stk", artikel_nr2, f"{einzel_preis_german2}€", "19,00 %", f"{end_preis_german2}€"],
        ]
    else:
        data = [
            ["Beschreibung", "Menge", "Artikel-Nr", "Einzelpreis", "USt. %", "Betrag"],
            [beschreibung1, f"{menge} Stk",
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

    # draw a line between the table and the total amount

    neunzehn_prozent, neunzehn_prozent_german = _two_decimal_german(end_preis - einzel_preis)

    if second_obj:
        neunzehn_prozent2, neunzehn_prozent_german2 = _two_decimal_german(end_preis2 - einzel_preis2)
        sum_neunzehn_prozent, sum_neunzehn_prozent_german = _two_decimal_german(neunzehn_prozent + neunzehn_prozent2)

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

    # draw a line obve the payment information
    c.line(45, 66, 585, 66)
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
    return c, response



def generate_pdf(verkauf_id, operation_mode: str = 'attachment'):
    second_obj = False
    verkauf_obj = Verkauf.objects.get(id=verkauf_id)
    buyer_name = verkauf_obj.kunde_name
    buyer_street = verkauf_obj.kunde_strasse
    buyer_city = verkauf_obj.kunde_city
    buyer_zip = verkauf_obj.kunde_plz
    rechnungsnummer = verkauf_obj.rechnungs_nr
    rechnungsdatum = (verkauf_obj.verkaufsdatum).strftime('%d.%m.%Y')
    falligkeitsdatum = "Sofort"
    menge = verkauf_obj.menge
    artikel_nr = verkauf_obj.artikel_nr
    serial_nr = verkauf_obj.serial_number
    preis = float(verkauf_obj.preis)
    zusaetzlich = verkauf_obj.zusaetzlich

    einzel_preis, einzel_preis_german = _two_decimal_german(preis / 1.19)
    end_preis, end_preis_german = _two_decimal_german(preis)

    zahlungsart = verkauf_obj.zahlungsart
    if str(serial_nr):
        beschreibung_SN = verkauf_obj.beschreibung + " SN:" + str(serial_nr)
    else:
        beschreibung_SN = verkauf_obj.beschreibung
    beschreibung_SN = _wrap_text(beschreibung_SN, max_length=58)

    if verkauf_obj.beschreibung2:
        second_obj = True
        artikel_nr2 = verkauf_obj.artikel_nr2
        serial_nr2 = verkauf_obj.serial_number2
        preis2 = float(verkauf_obj.preis2)
        einzel_preis2, einzel_preis_german2 = _two_decimal_german(preis2 / 1.19)
        end_preis2, end_preis_german2 = _two_decimal_german(preis2)

        sum_einzel_preis, sum_einzel_preis_german = _two_decimal_german(einzel_preis + einzel_preis2)
        sum_end_preis, sum_end_preis_german = _two_decimal_german(end_preis + end_preis2)

        if str(serial_nr2):
            beschreibung_SN2 = verkauf_obj.beschreibung2 + " SN:" + str(serial_nr2)
        else:
            beschreibung_SN2 = verkauf_obj.beschreibung2

        beschreibung_SN2 = _wrap_text(beschreibung_SN2, max_length=58)

    # Create PDF
    file_name = "Rechnungsnr_" + str(rechnungsnummer) + ".pdf"
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'{operation_mode}; filename={file_name}'

    # pdf_name = f"{os.getcwd()}/invoice.pdf"
    c = canvas.Canvas(response, pagesize=letter)

    logo_path = f"{os.getcwd()}/lager/logo.png"
    try:
        c.drawImage(logo_path, 440, 640, width=2 * inch, height=2 * inch)
    except:
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
    c.setFont("Helvetica-Bold", 16)
    c.drawString(23, 460, "Rechnung")
    c.setFont("Helvetica", 10)
    c.drawString(23, 445, zusaetzlich)

    if not buyer_street:
        buyer_street = ' '
    c.drawString(45, 564, buyer_street)
    if not buyer_city:
        buyer_city = ' '
    if not buyer_zip:
        buyer_zip = ' '
    adress = buyer_zip + ' ' + buyer_city
    c.drawString(45, 550, adress)
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

    # draw a line between the table and the total amount

    neunzehn_prozent, neunzehn_prozent_german = _two_decimal_german(end_preis - einzel_preis)

    if second_obj:
        neunzehn_prozent2, neunzehn_prozent_german2 = _two_decimal_german(end_preis2 - einzel_preis2)
        sum_neunzehn_prozent, sum_neunzehn_prozent_german = _two_decimal_german(neunzehn_prozent + neunzehn_prozent2)

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

    # draw a line obve the payment information
    c.line(45, 66, 585, 66)
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

    return c, response


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

    return "\n".join(lines)

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

            elif type2 == 'backofen':
                backofen = get_object_or_404(Backofen, pk=id2)
                _update_inventar_2_product(verkauf, backofen, request, "Backofen", anzahl)

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

            elif type2 == 'backofen':
                backofen = get_object_or_404(Backofen, pk=id2)
                _update_inventar_2_product(verkauf, backofen, request, "Backofen", 1)

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
    try:
        kauf_preis = model_obj.Kauf_preis
    except:
        kauf_preis = float(0.0)
    verkauf_obj = Verkauf.objects.create(

                    type_of=type_maschine,
                    menge=anzahl,
                    verkäufer=request.user.username,
                    zahlungsart=request.POST.get('zahlungsart'),
                    verkaufsdatum=request.POST.get('verkaufsdatum'),
                    marke=request.POST.get('marke'),
                    model=request.POST.get('model'),
                    serial_number=request.POST.get('seriennummer'),
                    artikel_nr=request.POST.get('artikelnummer'),
                    preis=float(request.POST.get('preis'))*float(anzahl),
                    beschreibung=request.POST.get('beschreibung'),
                    rechnungs_nr=request.POST.get('rechnungs_nr'),
                    kunde_name=request.POST.get('kunde_name'),
                    kunde_strasse=request.POST.get('kunde_strasse'),
                    kunde_plz=request.POST.get('kunde_plz'),
                    kunde_city=request.POST.get('kunde_city'),
                    kunde_email=request.POST.get('kunde_email'),
                    kunde_mobile=request.POST.get('kunde_mobile'),
                    kapital = kauf_preis,
                    zusaetzlich=request.POST.get('zusätzlich'),
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
    try:
        kauf_preis2 = model_obj.Kauf_preis
        verkauf_obj.kapital2 = kauf_preis2
    except:
        kauf_preis2 = float(0.0)
        verkauf_obj.kapital2 = kauf_preis2

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


    if request.POST.get('preis2'):
        verkauf_obj.preis2 = request.POST.get('preis2')
        verkauf_obj.final_preis = float(verkauf_obj.preis) + float(verkauf_obj.preis2)

    if not request.POST.get('preis2'):
        verkauf_obj.preis2 = float(0.0)
        verkauf_obj.final_preis = float(verkauf_obj.preis) + float(verkauf_obj.preis2)

    return verkauf_obj


def _two_decimal_german(float_number):
    x = f"{float_number:.2f}"
    two_decimal = float(x)
    german_format = x.replace(".", ",")
    return two_decimal, german_format