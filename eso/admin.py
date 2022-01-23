from django.contrib import admin
from .models import TextPresentation, Opinion, OsteopathyAbout, OsteopathyCase, OsteopathyHistory, Appointment,\
    AppointmentsDescription, AccountInformation

admin.site.register(TextPresentation)
admin.site.register(Opinion)
admin.site.register(OsteopathyAbout)
admin.site.register(OsteopathyCase)
admin.site.register(OsteopathyHistory)
admin.site.register(Appointment)
admin.site.register(AppointmentsDescription)
admin.site.register(AccountInformation)
