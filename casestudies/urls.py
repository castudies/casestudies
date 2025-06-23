from django.urls import path
from . import views

app_name = 'casestudies'

urlpatterns = [
    path('', views.home, name='home'),
    path('cases/', views.all_case_studies, name='case_study_list'),
    path('about/', views.about, name='about'),
    path('send-case-study/', views.send_case_study, name='send_case_study'),
    path('terms/', views.terms_of_service, name='terms'),
    path('privacy/', views.privacy_policy, name='privacy'),
    path('socials/', views.socials, name='socials'),
    path('acknowledgements/', views.acknowledgements, name='acknowledgements'),
    path('<slug:slug>/', views.case_study_detail, name='case_study_detail'),

] 