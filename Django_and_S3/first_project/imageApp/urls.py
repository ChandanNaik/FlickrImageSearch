from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', views.search, name='imageApp-home'),
    path('loading/', views.loading, name='imageApp-loading'),
    path('updateUserTags/', views.updateUserTags, name='imageApp-updateUserTags'),
    path('searchResults/', views.searchResults, name='imageApp-searchResults'),
    path('dumpToBucket/', views.dumpToBucket, name='imageApp-dumpToBucket'),
    path('performDump/', views.performDump, name='imageApp-performDump'),
    path('home/', views.searchPretty, name='imageApp-pretty-home'),
    path('tagUploadedImage/', views.tagUploadedImage, name='imageApp-pretty-tagUpload'),
    path('results/', views.results, name='imageApp-pretty-results'),
    path('about/', views.about, name='imageApp-about'),
    path('gallery/', views.gallery, name='imageApp-gallery')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)