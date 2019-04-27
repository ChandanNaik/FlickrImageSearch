from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='app1-home'),
    path('hiddenHome/', views.home, name='app1-hiddenHome'),
]
