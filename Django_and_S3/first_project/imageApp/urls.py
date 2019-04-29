from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', views.search, name='imageApp-home'),
    path('searchResults/', views.searchResults, name='imageApp-searchResults'),
    path('dumpToBucket/', views.dumpToBucket, name='imageApp-dumpToBucket'),
    path('performDump/', views.performDump, name='imageApp-performDump')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)