"""
URL configuration for prsep project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import urls as auth_urls
import core.views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include(auth_urls)),
    path('', core.views.HomePageView.as_view(), name='home'),
    path('seed-compte', core.views.seed_compte, name='seed-compte'),
    path('cartographie/', core.views.CartigraphieView.as_view(), name='cartographie'),
    path('analyse/', core.views.AnalyseView.as_view(), name='analyse'),
    path('planification/', include('planification.urls', namespace='plan',)),
    path('rapportage/', include('rapportage.urls', namespace='rapport')),
    path('suivi/', include('suivi.urls', namespace='suivi')),
    path('create-user/', core.views.create_user_view, name='create_user'),
    path('delete-user/<int:pk>', core.views.delete_user_view, name='delete_user'),
    path('deconnexion/', core.views.logout_view, name='deconnexion'),
    path('parametres/', include('setting.urls', namespace='setting')),
    path('test/', core.views.test_import, name='test'),
    path('programme/', include('programme.urls', namespace='programme')),
    path('setting/', include('setting.urls', namespace='setting')),
    path('change-password/', core.views.change_password, name='change_password'),
    path('update-exercice', core.views.update_current_exercice, name='update_current_exercice'),
    path('exercices', core.views.ExerciceListView.as_view(), name='exercices_list'),
    path('exercices-create', core.views.ExerciceCreateView.as_view(), name='exercices_create'),
]

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls
    urlpatterns  += debug_toolbar_urls()
