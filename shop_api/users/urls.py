from django.urls import path

from . import views


urlpatterns = [
    path('registration/', views.UserRegistrationAPIView.as_view()),
    path('authorization/', views.UserAuthorizationAPIView.as_view()),
    path('confirm/', views.UserConfirmAPIView.as_view()),
]
