from django.shortcuts import render, resolve_url, get_object_or_404
from django.views import generic
from pathlib import Path
from django.http import FileResponse

from planification.forms import TacheForm
from planification.models import PPM, Tache, Exercice, ComposantProjet
from programme.models import TacheProgram, ComposantesProgram, SousDomainResult


class PlanPTBAProjet(generic.TemplateView):
    template_name = 'plan/ptba-projet.html'

    def get_queryset(self):
        return Tache.objects.all()

    def get_context_data(self, **kwargs):
        current_exercice = Exercice.objects.last()
        IldCreateForm = TacheForm
        activites = Tache.objects.filter(
            departement=self.request.user.departement,
            exercice=current_exercice,
        )
        composants = ComposantProjet.objects.all()
        return kwargs | locals()

    def get(self, request, *args, **kwargs):
        if (action := request.GET.get('action', None)) is not None:
            if action == 'soumettre':
                self.get_queryset().update(status_validation=request.GET.get('status', 10))
        return super().get(request, *args, **kwargs)


class PlanPTBAProgramme(generic.TemplateView):
    template_name = "plan/ptba-programme.html"

    def get_context_data(self, **kwargs):
        current_exercice = Exercice.objects.last()
        composants = ComposantesProgram.objects.all()
        sousdomaines = SousDomainResult.objects.all()
        return kwargs | locals()


class TacheCreateFormView(generic.FormView):
    form_class = TacheForm

    def form_valid(self, form):
        activite = form.save(commit=False)
        activite.user = self.request.user
        activite.departement = self.request.user.departement
        activite.save()
        return super().form_valid(form)

    def get_success_url(self):
        return resolve_url('plan:ptba-projet')


class PPMListView(generic.ListView):
    template_name = 'plan/ppm.html'
    queryset = PPM.objects.all()


def tache_detail(request, id):
    # Récupérer la tâche ou renvoyer une page 404 si elle n'existe pas
    tache = get_object_or_404(Tache, id=id)
    return render(request, 'plan/details_tache.html', {'tache': tache})


def upload_ptba_template(request):
    template_file = Path(__file__).resolve().parent.parent / 'templates/models/ptba-projet.xlsx'
    return FileResponse(open(template_file, 'rb'), as_attachment=True, filename='ptba-projet.xlsx')
