from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import TextPresentation, TextPresentationParagrapth, TextPresentationSpecialization, OsteopathyAbout,\
    OsteopathyCase, OsteopathyHistory, AppointmentsDescription, AccountInformation, OsteopathyAdvantages,\
    PediatricOstepathy, PediatricOstepathyReasons, Opinion, AppointmentGeneralInformation, AppointmentsImportantNotes
from .backend import GoogleCalendar, Gmail
import datetime

APPOINTMENT_DURATION_MIN = 60


def home_page(request):
    presentation_text = get_object_or_404(TextPresentation)
    paragraphs = TextPresentationParagrapth.objects.all()
    specializations = TextPresentationSpecialization.objects.all()
    opinions = Opinion.objects.filter(is_valid=True)
    context = {
        "presentation_text": presentation_text,
        "paragraphs": paragraphs,
        "specializations": specializations,
        "opinions": opinions
    }

    return render(request=request, template_name='eso/index.html', context=context)


def osteopathy_about_page(request):
    osteopathy_about = get_object_or_404(OsteopathyAbout)
    osteopathy_advantages = OsteopathyAdvantages.objects.all()
    context = {
        "osteopathy_about": osteopathy_about,
        "osteopathy_advantages": osteopathy_advantages}

    return render(request=request, template_name='eso/osteopathy_about_page.html', context=context)


def osteopathy_cases_page(request):
    osteopathy_cases = OsteopathyCase.objects.all() #Later change this to filter by valid cases only
    context = {"osteopathy_cases": osteopathy_cases}

    return render(request=request, template_name='eso/osteopathy_cases_page.html', context=context)


def osteopathy_history_page(request):
    osteopathy_history = get_object_or_404(OsteopathyHistory)
    context = {"osteopathy_history": osteopathy_history}

    return render(request=request, template_name='eso/osteopathy_history_page.html', context=context)


def scheduling_page(request):
    appointments_descriptions = AppointmentsDescription.objects.all()
    appointments_important_notes = AppointmentsImportantNotes.objects.all()
    appointments_general_information = get_object_or_404(AppointmentGeneralInformation)
    context = {
        "appointments_descriptions": appointments_descriptions,
        "appointments_important_notes": appointments_important_notes,
        "appointments_general_information": appointments_general_information
    }

    if request.method == "POST" and request.POST.get("form") == 'appointment':
        try:
            summary = "Consulta: " + request.POST.get("name") + " - " + request.POST.get("phone")
            date_requested = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            description = "Nome: " + request.POST.get("name") + "\nTel: " + request.POST.get("phone") + "\nEmail: " + request.POST.get("email") + "\nSubmetido a: " + date_requested + "\nRazão: " + request.POST.get("description")
            start_datetime = datetime.datetime(int(request.POST.get("year")), int(request.POST.get("month")), int(request.POST.get("day")), int(request.POST.get("hour")), int(request.POST.get("minutes")))
            end_datetime = start_datetime + datetime.timedelta(minutes=APPOINTMENT_DURATION_MIN)

            google_calendar = GoogleCalendar(api_version="v3")
            google_calendar.insert_event(summary=summary, description=description, location="Clinica",
                                         start_datetime=start_datetime, end_datetime=end_datetime,
                                         attendee_emails=["jmoutinho94@gmail.com"])
            account_information = get_object_or_404(AccountInformation)

            gmail = Gmail(account_email=account_information.google_account_email,
                          account_password=account_information.google_account_password)
            gmail.send_email(emails_to=[account_information.email_to], subject="Pedido de Agendamento",
                             body=description)

            return JsonResponse({"status": "successful"}, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({"status": "failed"}, status=200)

    return render(request=request, template_name='eso/scheduling_page.html', context=context)


def opinion_page(request):
    if request.method == "POST" and request.POST.get("form") == 'opinion':
        try:
            opinion = Opinion(author=request.POST.get("name"), post=request.POST.get("opinion"),
                              date=datetime.datetime.now(), is_valid=False)

            opinion.save()

            account_information = get_object_or_404(AccountInformation)
            body = f"""
                Nome: {request.POST.get("name")}
                Opinião: {request.POST.get("opinion")}
            """

            gmail = Gmail(account_email=account_information.google_account_email,
                          account_password=account_information.google_account_password)
            gmail.send_email(emails_to=[account_information.email_to], subject="Opinião",
                             body=body)

            return JsonResponse({"status": "successful"}, status=200)
        except Exception:
            return JsonResponse({"status": "failed"}, status=200)

    return render(request=request, template_name='eso/opinion_page.html')


def pediatric_osteopathy_page(request):
    pediatric_osteopathy = get_object_or_404(PediatricOstepathy)
    pediatric_osteopathy_reasons = PediatricOstepathyReasons.objects.all()

    context = {
        "pediatric_osteopathy": pediatric_osteopathy,
        "pediatric_osteopathy_reasons": pediatric_osteopathy_reasons}

    return render(request=request, template_name='eso/pediatric_osteopathy.html', context=context)

