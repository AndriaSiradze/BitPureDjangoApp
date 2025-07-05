from django.urls import path

from blogapp.apps import BlogConfig
from blogapp import views
from blogapp.views import TitleDetailView

app_name = BlogConfig.name
urlpatterns = [
    path('', views.TitleListView.as_view(), name='index'),
    path('title/<int:pk>', TitleDetailView.as_view(), name='title_detail'),
]
