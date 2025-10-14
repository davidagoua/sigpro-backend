from django.urls import path
import setting.views as views

app_name = 'setting'

urlpatterns = [
    path('composantes/', views.ComposanteTemplateView.as_view(), name='composantes'),
    path('vehicules/', views.vehicule_list, name='vehicule_list'),
    path('vehicules/ajouter/', views.vehicule_add, name='vehicule_add'),
    path('vehicules/modifier/<int:pk>/', views.vehicule_edit, name='vehicule_edit'),
    path('vehicules/<int:pk>/delete', views.delete_vehicule, name='delete_vehicule'),
    path('vehicules/<int:pk>', views.VehiculeDetailsView.as_view(), name='vehicule_details'),
    path('emprunts/', views.emprunt_list, name='emprunt_list'),
    path('emprunts/ajouter/', views.emprunt_add, name='emprunt_add'),
    path('emprunts/modifier/<int:pk>/', views.emprunt_edit, name='emprunt_edit'),
]