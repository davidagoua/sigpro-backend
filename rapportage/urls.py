from django.urls import path

from rapportage.views import (RapportMensuelProjetView, update_state,upload_file,
                              RapportAnnuelView, RapportSemestrielView, RapportTrimestrielProjetView, RapportTrimestrielProgrammeView, RapportMensuelProgrammeView,
                              RapportCirconstancierView, wopi_file_info, wopi_file_contents)
from rapportage.views import update_file_and_label, download_file, delete_rapport

app_name = "analyse"
urlpatterns = [
    path('rapport-mensuel-projet/', RapportMensuelProjetView.as_view(), name='rapport-mensuel-projet'),
    path('rapport-trimestriel-projet/', RapportTrimestrielProjetView.as_view(), name='rapport-trimestriel-projet'),
    path('rapport-semestriel/', RapportSemestrielView.as_view(), name='rapport-semestriel'),
    path('rapport-annuel/', RapportAnnuelView.as_view(), name='rapport-annuel'),
    path('rapport-mensuel-programme/', RapportMensuelProgrammeView.as_view(), name='rapport-mensuel-programme'),
    path('rapport-trimestriel-programme/', RapportTrimestrielProgrammeView.as_view(), name='rapport-trimestriel-programme'),
    path('rapport-circonstancier/', RapportCirconstancierView.as_view(), name='rapport-circonstancier'),
    path('update-state/<int:pk>', update_state, name='update_state'),
    path('upload-file/<int:pk>', upload_file, name='upload_file'),
    path('update-file-and-label/<int:pk>', update_file_and_label, name='update_file_and_label'),
    path('download-file/<int:pk>', download_file, name='download_file'),
    path('wopi/files/<str:file_id>', wopi_file_info, name='wopi_file_info'),
    path('wopi/files/<str:file_id>/contents', wopi_file_contents, name='wopi_file_contents'),
    path('delete-rapport/<int:pk>', delete_rapport, name='delete_rapport'),
]