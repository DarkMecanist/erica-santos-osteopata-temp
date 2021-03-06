from django.contrib import admin
from .models import TextPresentation, Opinion, OsteopathyAbout, OsteopathyCase, OsteopathyHistory,\
    AppointmentsDescription, AccountInformation, OsteopathyAdvantages, PediatricOstepathy, PediatricOstepathyReasons,\
    TextPresentationParagrapth, TextPresentationSpecialization, AppointmentGeneralInformation,\
    AppointmentsImportantNotes

admin.site.register(TextPresentation)
admin.site.register(Opinion)
admin.site.register(OsteopathyAbout)
admin.site.register(OsteopathyCase)
admin.site.register(OsteopathyHistory)
admin.site.register(AppointmentsDescription)
admin.site.register(AccountInformation)
admin.site.register(OsteopathyAdvantages)
admin.site.register(PediatricOstepathy)
admin.site.register(PediatricOstepathyReasons)
admin.site.register(TextPresentationParagrapth)
admin.site.register(TextPresentationSpecialization)
admin.site.register(AppointmentGeneralInformation)
admin.site.register(AppointmentsImportantNotes)

