from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import home_page, osteopathy_about_page, osteopathy_cases_page, osteopathy_history_page, scheduling_page,\
    opinion_page


urlpatterns = [
    path('', home_page, name='home_page'),
    path('osteopatia_sobre/', osteopathy_about_page, name='osteopathy_about_page'),
    path('osteopatia_casos/', osteopathy_cases_page, name='osteopathy_cases_page'),
    path('osteopatia_historia/', osteopathy_history_page, name='osteopathy_history_page'),
    path('marcacoes/', scheduling_page, name='scheduling_page'),
    path('opiniao/', opinion_page, name='opinion_page')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
