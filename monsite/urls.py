from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('site_cmds.urls')),  # Inclure les URLs de l'application
]

# Configurer la vue 404 personnalisée
handler404 = 'site_cmds.views.custom_404'
