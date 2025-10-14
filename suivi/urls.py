from django.urls import path

from suivi.views import SuiviPTBAProjetView, UpdateTacheView, ajouter_decaissements, AddDecaissementView, \
    delete_decaissement, update_state, ActivitiesListView, CreateTDRView, update_tdr_state, delete_tdr, \
    TDRLocalListView, TDRTechniqueListView, download_tdr, TDRCoordinationListView, get_tdr_stats, cancel_tdr, \
    CreateTDRProgrammeView, update_tdrprogram_state, download_tdr_programme, cancel_tdr_programme, delete_tdr_programme, UpdateTDRProgrammeView, UpdateTDRView, \
    UpdateTDRCoordinationView, UpdateTDRProgrammeCoordinationView, FinalizeTDRView, updateTDRCoordinationView, stats_view

from suivi.comsumer import TDRConsumer



app_name = 'suivi'

urlpatterns = [
    path('ptba-projet', SuiviPTBAProjetView.as_view(), name='ptba-projet'),
    path('update-tache/<int:pk>', UpdateTacheView.as_view(), name='update_tache'),
    path('add-decaissement-projet/<int:pk>', AddDecaissementView.as_view(), name='add-decaissement-projet'),
    path('delete-decaissement/<int:pk>', delete_decaissement, name='delete-decaissement'),
    path('update-state/<int:pk>', update_state, name='update_state'),
    path('activites/', ActivitiesListView.as_view(), name='list_activities'),
    path('tdr/create', CreateTDRView.as_view(), name='create_tdr'),
    path('tdr-programme/create', CreateTDRProgrammeView.as_view(), name='create_tdr_programme'),
    path('update-tdr-state/<int:pk>/', update_tdr_state, name='update-tdr-state'),
    path('update-tdrprogram-state/<int:pk>/', update_tdrprogram_state, name='update-tdrprogram-state'),
    path('tdr/<int:pk>/delete', delete_tdr, name='delete_tdr'),
    path('tdr-local/', TDRLocalListView.as_view(), name='tdr_local'),
    path('tdr-technique/', TDRTechniqueListView.as_view(), name='tdr_technique'),
    path('tdr-coordination/', TDRCoordinationListView.as_view(), name='tdr_coordination'),
    path('tdr-download/<int:pk>', download_tdr, name='tdr_download'),
    path('tdr-get-stats', get_tdr_stats, name='get_tdr_stats'),
    path('tdr-cancel/<int:pk>', cancel_tdr, name='cancel_tdr'),
    path('ws/tdr/', TDRConsumer.as_asgi(), name='tdr_consumer'),
    path('tdr-programme-download/<int:pk>', download_tdr_programme, name='tdr_programme_download'),
    path('tdr-programme-cancel/<int:pk>', cancel_tdr_programme, name='cancel_tdr_programme'),
    path('tdr-programme/<int:pk>/delete', delete_tdr_programme, name='delete_tdrprogram'),
    path('tdr-programme/<int:pk>/update', UpdateTDRProgrammeView.as_view(), name='update_tdrprogram'),
    path('tdr/<int:pk>/update', UpdateTDRView.as_view(), name='update_tdr'),
    path('tdr-programme-coordination/<int:pk>/update', UpdateTDRProgrammeCoordinationView.as_view(), name='update_tdrprogram_coordination'),
    path('tdr-coordination/<int:pk>/update', updateTDRCoordinationView, name='update_tdr_coordination'),
    path('tdr-finalize/<int:pk>/update', FinalizeTDRView.as_view(), name='finalize_tdr'),
    path('stats/', stats_view, name='stats'),

]