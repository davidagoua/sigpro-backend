from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.http import HttpResponse, FileResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils.timezone import now
from django.views import generic
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.shortcuts import resolve_url
from planification.forms import UpdateTacheForm, DecaissementFormSet
from planification.models import SousComposantProjet, ComposantProjet, Tache, Decaissement, Exercice, Indicateur
from programme.models import Activite
from .forms import CancelTDRForm
from .models import TDR, TDRProgramme
from core.models import Departement
from suivi.models import Drf


class SuiviPTBAProjetView(generic.TemplateView):
    template_name = 'suivi/ptba-projet.html'

    def get_context_data(self, **kwargs):

        return kwargs | {
            'updatetacheform': UpdateTacheForm,
            'composants': ComposantProjet.objects.all().order_by('pk'),
            'exercices': Exercice.objects.all(),
            'year': now().year
        }


class UpdateTacheView(SingleObjectTemplateResponseMixin, generic.FormView):
    form_class = UpdateTacheForm
    template_name = 'suivi/update_tache.html'

    def get_queryset(self):
        return Tache.objects.all()

    def get_context_data(self, **kwargs):
        object = Tache.objects.get(pk=self.kwargs['pk'])
        return kwargs | {
            'updatetacheform': UpdateTacheForm(instance=object),
            'object': object
        }




class AddDecaissementView(generic.DetailView):

    template_name = 'suivi/add-decaissement-projet.html'
    model = Tache

    def get_success_url(self):
        return resolve_url('suivi:add-decaissement-projet', pk=self.get_object().pk)

    def get_context_data(self, **kwargs):
        return kwargs | {
            'drfs': Drf.objects.all()
        }

    def post(self, request, *args, **kwargs):
        tache = self.get_object()
        try:
            montant_engage = int(request.POST.get('montant_engage'))
            paiement = int(request.POST.get('paiement'))

            if montant_engage < 0:
                raise ValueError("Le montant engagé ne peut pas être négatif.")

            if paiement > 0:
                Decaissement(montant=paiement, user=request.user, in_drf=True, tache=tache, drf__pk=request.POST.get('drf')).save()

            tache.montant_engage = montant_engage
            tache.save()
            messages.success(request, "Le montant engagé a été mis à jour avec succès.")
            return redirect(self.get_success_url())
        except (ValueError, TypeError) as e:
            messages.error(request, e.__dict__)
            return redirect(self.get_success_url())
        except Exception as e:
            messages.error(request, f"Une erreur s'est produite: {e}")
            return redirect(self.get_success_url())


def ajouter_decaissements(request, pk):
    tache = get_object_or_404(Tache, pk=pk)
    if request.method == 'POST':
        formset = DecaissementFormSet(request.POST, instance=tache)
        if formset.is_valid():
            formset.save()
            return redirect('nom_de_votre_vue_liste_taches')  # Redirige vers la liste des tâches
    else:
        formset = DecaissementFormSet(instance=tache)
    return render(request, 'ajouter_decaissements.html', {'formset': formset, 'tache': tache})


def delete_decaissement(request, pk):
    d = get_object_or_404(Decaissement, pk=pk)
    tache = d.tache
    d.delete()
    return redirect('suivi:add-decaissement-projet', pk=tache.pk)


def update_state(request, pk):
    tache = get_object_or_404(
        Tache,
        pk=pk)
    tache.status_execution = request.GET.get('status')
    tache.save()
    return redirect(resolve_url('plan:tache_detail', pk=tache.pk))



class ActivitiesListView(LoginRequiredMixin, generic.ListView):

    template_name = 'suivi/list_activities.html'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Tache.objects.select_related("indicateur").all()
        return Tache.objects.filter(responsable=self.request.user.departement.name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['indicateurs'] = Indicateur.objects.all()
        context['directions'] = Departement.objects.all()
        return context


class TDRLocalListView(LoginRequiredMixin, generic.ListView):
    template_name = "suivi/local_list_activities.html"
    state = 10

    def get_queryset(self):
        if self.request.user.is_staff:
            return Tache.objects.filter(
                Q(pk__in=[tdr.activity.pk for tdr in TDR.objects.filter(state=20)])
            )
        return Tache.objects.filter(responsable=self.request.user.departement.name).filter(
            Q(pk__in=[tdr.activity.pk for tdr in TDR.objects.filter(state=20)])
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_staff:
            context['object_list'] = Tache.objects.filter(
                Q(pk__in=[tdr.activity.pk for tdr in TDR.objects.filter(state=self.state)])
            )
        else:
            context['object_list'] = Tache.objects.filter(responsable=self.request.user.departement.name).filter(
                Q(pk__in=[tdr.activity.pk for tdr in TDR.objects.filter(state=self.state)])
            )

        return context | {
            'state': self.state + 10
        }



class TDRTechniqueListView(LoginRequiredMixin, generic.ListView):
    template_name = "suivi/technique_list_activities.html"
    state = 20

    def get_queryset(self):
        return Tache.objects.filter(responsable=self.request.user.departement.name).filter(
            Q(pk__in=[tdr.activity.pk for tdr in TDR.objects.filter(state=self.state)])
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_staff:
            context['object_list'] = Tache.objects.filter(
                Q(pk__in=[tdr.activity.pk for tdr in TDR.objects.filter(state__gt=0)])
            )
        else:
            context['object_list'] = Tache.objects.filter(responsable=self.request.user.departement.name).filter(
                Q(pk__in=[tdr.activity.pk for tdr in TDR.objects.filter(state__gt=0)])
            )

        return context | {
            'state': self.state + 10
        }


class TDRCoordinationListView(LoginRequiredMixin, generic.ListView):
    template_name = "suivi/coordination_list_activities.html"

    def get_queryset(self):
        return Tache.objects.filter(responsable=self.request.user.departement.name).filter(
            Q(pk__in=[tdr.activity.pk for tdr in TDR.objects.filter(state=30)])
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_staff:
            context['object_list'] = Tache.objects.filter(
                Q(pk__in=[tdr.activity.pk for tdr in TDR.objects.filter(state=30)])
            )
        else:
            context['object_list'] = Tache.objects.filter(responsable=self.request.user.departement.name).filter(
                Q(pk__in=[tdr.activity.pk for tdr in TDR.objects.filter(state=30)])
            )

        return context | {
            'state': self.state + 10
        }



def delete_tdr(request, pk):
    tdr = get_object_or_404(TDR, pk=pk)
    tdr.delete()
    messages.success(request, "TDR annulée")
    return redirect('suivi:list_activities')


class CreateTDRView(LoginRequiredMixin, generic.CreateView):
    model = TDR
    fields = ['file','label']

    def get_success_url(self):
        return resolve_url('suivi:list_activities')

    def form_invalid(self, form):
        print(form.errors)


    def form_valid(self, form):
        tdr = form.save(commit=False)
        tdr.user = self.request.user
        tdr.activity = get_object_or_404(Tache, pk=self.request.POST.get('activity_id'))
        tdr.departemnt = tdr.activity.departement
        tdr.save()
        return super().form_valid(form)

class CreateTDRProgrammeView(LoginRequiredMixin, generic.CreateView):
    model = TDRProgramme
    fields = ['file','label']
    required_fields = ['file']

    def get_success_url(self):
        return resolve_url('programme:liste-tache')

    def form_valid(self, form):
        tdr = form.save(commit=False)
        tdr.user = self.request.user
        tdr.activity = Activite.objects.get(pk=self.request.POST.get('activity_id'))
        tdr.save()
        return super().form_valid(form)


class UpdateTDRView(LoginRequiredMixin, generic.UpdateView):
    fields = [
        'file'
    ]
    model = TDR

    def get_success_url(self):
        return resolve_url(self.request.GET['next'])

    def form_valid(self, form):
        tdr = form.save(commit=False)
        tdr.user = self.request.user
        tdr.save()
        return super().form_valid(form)


class UpdateTDRCoordinationView(LoginRequiredMixin, generic.TemplateView):
    fields = [
        'accorder','injonction'
    ]
    model = TDR

    def get_success_url(self):
        messages.success(self.request, "TDR modifiée")
        return resolve_url(self.request.GET['next'])



    def form_valid(self, form):
        tdr = form.save(commit=False)
        tdr.injonction = self.request.POST.get('injonction',True)
        tdr.accorder = self.request.POST.get('accorder',True)
        tdr.save()
        return super().form_valid(form)


def updateTDRCoordinationView(request, pk):
    tdr = get_object_or_404(TDR, pk=pk)
    tdr.injonction = request.POST.get('injonction', True)
    tdr.accorder = request.POST.get('accorder', True)
    tdr.save()
    return redirect(resolve_url(request.GET['next']))



class UpdateTDRProgrammeView(LoginRequiredMixin, generic.UpdateView):
    fields = [
        'file','label'
    ]
    model = TDRProgramme

    def get_success_url(self):
        return resolve_url(self.request.GET['next'])

    def form_valid(self, form):
        tdr = form.save(commit=False)
        tdr.user = self.request.user
        tdr.save()
        return super().form_valid(form)


class UpdateTDRProgrammeCoordinationView(LoginRequiredMixin, generic.UpdateView):
    fields = [
        'accorder','injonction'
    ]
    model = TDRProgramme

    def get_success_url(self):
        return resolve_url(self.request.GET['next'])

    def form_valid(self, form):
        tdr = form.save(commit=False)
        tdr.save()
        return super().form_valid(form)


def update_tdr_state(request, pk):
    tdr = get_object_or_404(TDR, pk=pk)
    tdr.state = request.GET.get('state')
    tdr.save()
    messages.success(request, "TDR modifiée")
    return redirect(request.GET.get('next'))

def update_tdrprogram_state(request, pk):
    tdr = get_object_or_404(TDRProgramme, pk=pk)
    tdr.state = request.GET.get('state')
    if(tdr.state== 10):
        tdr.comments_set.delete()
    tdr.save()
    messages.success(request, "TDR modifiée")
    return redirect(request.GET.get('next'))

def download_tdr(request, pk):
    tdr = get_object_or_404(TDR, pk=pk)
    return FileResponse(open(tdr.file.path, 'rb'), content_type='application/octet-stream')


def download_tdr_programme(request, pk):
    tdr = get_object_or_404(TDRProgramme, pk=pk)
    return FileResponse(open(tdr.file.path, 'rb'), content_type='application/octet-stream')


def get_tdr_stats(request):
    stats = TDR.objects.values('state').annotate(count=Count('state'))
    result = {item['state']: item['count'] for item in stats}
    result['pointFocal'] = TDR.objects.filter(activity__responsable=request.user.departement.name).filter(
        Q(state=0)
    ).count()
    return JsonResponse(result)

def cancel_tdr(request, pk):
    if request.method == 'POST':
        tdr = TDR.objects.get(pk=pk)
        tdr.state = request.GET.get('state')
        tdr.save()
        form = CancelTDRForm(request.POST)
        comment = form.save(commit=False)
        comment.user = request.user
        comment.tdr = tdr
        comment.save()
    return redirect(request.GET.get('next'))



def cancel_tdr_programme(request, pk):
    if request.method == 'POST':
        tdr = TDRProgramme.objects.get(pk=pk)
        tdr.state = request.GET.get('state')
        tdr.save()
        form = CancelTDRForm(request.POST)
        comment = form.save(commit=False)
        comment.user = request.user
        comment.tdr = tdr
        comment.save()
    return redirect(request.GET.get('next'))


def delete_tdr_programme(request, pk):
    tdr = get_object_or_404(TDRProgramme, pk=pk)
    tdr.delete()
    messages.success(request, "TDR annulée")
    return redirect('programme:liste-tache')


class FinalizeTDRView(LoginRequiredMixin, generic.UpdateView):
    model = TDR
    fields = [
        'file_final',
        'lessons',
        'recommendations',
        'risks'
    ]

    def get_success_url(self):
        return resolve_url(self.request.GET.get('next', '/'))

    def form_valid(self, form):
        tdr = TDR.objects.get(pk=self.kwargs['pk'])
        tdr.file_final = form.cleaned_data['file_final']
        tdr.lessons = form.cleaned_data['lessons']
        tdr.recommendations = form.cleaned_data['recommendations']
        tdr.risks = form.cleaned_data['risks']
        tdr.state = 100
        tdr.save()
        return super().form_valid(form)



def stats_view(request):
    # Récupération des stats pour TDR
    tdr_stats = TDR.objects.values('state').annotate(count=Count('id'))

    # Récupération des stats pour TDRProgramme
    tdr_programme_stats = TDRProgramme.objects.values('state').annotate(count=Count('id'))

    # Passer les données au contexte
    context = {
        'tdr_stats': tdr_stats,
        'tdr_programme_stats': tdr_programme_stats,
    }
    return render(request, 'home_stats.html', context)


