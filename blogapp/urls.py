from django.urls import path

from blogapp.apps import BlogConfig
from blogapp import views
from blogapp.views import TitleDetailView

app_name = BlogConfig.name

urlpatterns = [
    path('', views.TitleListView.as_view(), name='index'),
    path('title/<int:pk>', TitleDetailView.as_view(), name='title_detail'),
    path("load_more_news/", views.load_more_news, name="load_more_news"),
    path('about/', views.AboutView.as_view(), name='about'),
    path('premium/', views.PremiumView.as_view(), name='premium'),
]