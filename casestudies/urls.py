from django.urls import path
from . import views

app_name = 'casestudies'

urlpatterns = [
    path('', views.home, name='home'),
    path('cases/', views.all_case_studies, name='case_study_list'),
    path('<slug:slug>/', views.case_study_detail, name='case_study_detail'),
] 