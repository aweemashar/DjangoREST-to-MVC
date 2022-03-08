from django.urls import re_path, path, include
from rest_framework_nested import routers
from .views import ClinicAPIView, DoctorAPIView, AppointmentAPIView, PatientAPIView


urlpatterns = [
    path('clinic', ClinicAPIView.as_view()),
    path('clinic/<int:pk>', ClinicAPIView.as_view()),
    path('doctor', DoctorAPIView.as_view()),
    path('doctor/<int:pk>', DoctorAPIView.as_view()),
    path('doctor/appointment/upcoming_available/<int:doctor_pk>', AppointmentAPIView.as_view()),
    path('clinic/patient/appointments', PatientAPIView.as_view()),


]