from django.urls import path

from authapp import views
from authapp.apps import AuthappConfig

app_name = AuthappConfig.name

urlpatterns = [
    path(
        'register/', views.CustomRegisterView.as_view(), name='register'
    ),
    path(
        'login/', views.CustomLoginView.as_view(), name='login'
    ),
    path(
        'logout/', views.CustomLogoutView.as_view(), name='logout'
    ),
]
