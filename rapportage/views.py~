from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse, JsonResponse
from django.shortcuts import render, redirect, reverse, resolve_url, get_object_or_404
from django.views import generic
from django.views.generic import FormView, ListView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectTemplateResponseMixin
from django.views.generic.edit import FormMixin, CreateView
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
import jwt, datetime
from django.conf import settings
from rapportage.forms import RapportForm
from rapportage.models import TypeRapport, Rapport




def generate_access_token(user):
    payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),  # Expiration du jeton
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token


class RapportMensuelProjetView(LoginRequiredMixin, FormView):
    template_name = 'rapportage/mensuel.html'
    form_class = RapportForm
    type_rapport = 'Mensuel-Projet'


    def form_valid(self, form):
        rapport = form.save(commit=False)
        rapport.user = self.request.user
        rapport.type = self.type_rapport
        rapport.save()
        messages.success(self.request, "Rapport enregistré")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Le formulaire est invalide.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return resolve_url(self.request.POST.get('next'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['access_token'] = generate_access_token(self.request.user)
        if self.request.user.is_staff:
            context['rapport_consolides'] = Rapport.objects.filter(type=self.type_rapport, state=10)
            context['object_list'] = Rapport.objects.filter(type=self.type_rapport, state=0)
        else:
            context['rapport_consolides'] = self.request.user.departement.rapport_set.filter(type=self.type_rapport, state=10)
            context['object_list'] = self.request.user.departement.rapport_set.filter(
                type=self.type_rapport, state=0
            )
        return context


class RapportMensuelProgrammeView(LoginRequiredMixin, FormView):
    template_name = 'rapportage/mensuel.html'
    form_class = RapportForm
    type_rapport = 'Mensuel-Programme'


    def form_valid(self, form):
        rapport = form.save(commit=False)
        rapport.user = self.request.user
        rapport.type = self.type_rapport
        rapport.save()
        messages.success(self.request, "Rapport enregistré")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Le formulaire est invalide.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return resolve_url(self.request.POST.get('next'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['access_token'] = generate_access_token(self.request.user)
        if self.request.user.is_staff:
            context['rapport_consolides'] = Rapport.objects.filter(type=self.type_rapport, state=10)
            context['object_list'] = Rapport.objects.filter(type=self.type_rapport, state=0)
        else:
            context['rapport_consolides'] = self.request.user.departement.rapport_set.filter(type=self.type_rapport, state=10)
            context['object_list'] = self.request.user.departement.rapport_set.filter(
                type=self.type_rapport, state=0
            )
        return context


class RapportTrimestrielProjetView(LoginRequiredMixin, FormView):
    template_name = 'rapportage/mensuel.html'
    form_class = RapportForm
    type_rapport = 'Trimestriel-Projet'


    def form_valid(self, form):
        rapport = form.save(commit=False)
        rapport.user = self.request.user
        rapport.type = self.type_rapport
        rapport.save()
        messages.success(self.request, "Rapport enregistré")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Le formulaire est invalide.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return resolve_url(self.request.POST.get('next'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['access_token'] = generate_access_token(self.request.user)
        if self.request.user.is_staff:
            context['rapport_consolides'] = Rapport.objects.filter(type=self.type_rapport, state=10)
            context['object_list'] = Rapport.objects.filter(type=self.type_rapport, state=0)
        else:
            context['rapport_consolides'] = self.request.user.departement.rapport_set.filter(type=self.type_rapport, state=10)
            context['object_list'] = self.request.user.departement.rapport_set.filter(
                type=self.type_rapport, state=0
            )
        return context


class RapportTrimestrielProgrammeView(LoginRequiredMixin, FormView):
    template_name = 'rapportage/mensuel.html'
    form_class = RapportForm
    type_rapport = 'Trimestriel-Programme'


    def form_valid(self, form):
        rapport = form.save(commit=False)
        rapport.user = self.request.user
        rapport.type = self.type_rapport
        rapport.save()
        messages.success(self.request, "Rapport enregistré")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Le formulaire est invalide.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return resolve_url(self.request.POST.get('next'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['access_token'] = generate_access_token(self.request.user)
        if self.request.user.is_staff:
            context['rapport_consolides'] = Rapport.objects.filter(type=self.type_rapport, state=10)
            context['object_list'] = Rapport.objects.filter(type=self.type_rapport, state=0)
        else:
            context['rapport_consolides'] = self.request.user.departement.rapport_set.filter(type=self.type_rapport, state=10)
            context['object_list'] = self.request.user.departement.rapport_set.filter(
                type=self.type_rapport, state=0
            )
        return context


class RapportSemestrielView(LoginRequiredMixin, FormView):
    template_name = 'rapportage/mensuel.html'
    form_class = RapportForm
    type_rapport = 'Semestriel'


    def form_valid(self, form):
        rapport = form.save(commit=False)
        rapport.user = self.request.user
        rapport.type = self.type_rapport
        rapport.save()
        messages.success(self.request, "Rapport enregistré")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Le formulaire est invalide.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return resolve_url(self.request.POST.get('next'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['access_token'] = generate_access_token(self.request.user)
        if self.request.user.is_staff:
            context['rapport_consolides'] = Rapport.objects.filter(type=self.type_rapport, state=10)
            context['object_list'] = Rapport.objects.filter(type=self.type_rapport, state=0)
        else:
            context['rapport_consolides'] = self.request.user.departement.rapport_set.filter(type=self.type_rapport, state=10)
            context['object_list'] = self.request.user.departement.rapport_set.filter(
                type=self.type_rapport, state=0
            )
        return context



class RapportAnnuelView(LoginRequiredMixin, FormView):
    template_name = 'rapportage/mensuel.html'
    form_class = RapportForm
    type_rapport = 'Annuel'


    def form_valid(self, form):
        rapport = form.save(commit=False)
        rapport.user = self.request.user
        rapport.type = self.type_rapport
        rapport.save()
        messages.success(self.request, "Rapport enregistré")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Le formulaire est invalide.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return resolve_url(self.request.POST.get('next'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['access_token'] = generate_access_token(self.request.user)
        if self.request.user.is_staff:
            context['rapport_consolides'] = Rapport.objects.filter(type=self.type_rapport, state=10)
            context['object_list'] = Rapport.objects.filter(type=self.type_rapport, state=0)
        else:
            context['rapport_consolides'] = self.request.user.departement.rapport_set.filter(type=self.type_rapport, state=10)
            context['object_list'] = self.request.user.departement.rapport_set.filter(
                type=self.type_rapport, state=0
            )
        return context


class RapportCirconstancierView(LoginRequiredMixin, FormView):
    template_name = 'rapportage/mensuel.html'
    form_class = RapportForm
    type_rapport = 'Circonstancier'


    def form_valid(self, form):
        rapport = form.save(commit=False)
        rapport.user = self.request.user
        rapport.type = self.type_rapport
        rapport.save()
        # attacher les roles et departements
        
        messages.success(self.request, "Rapport enregistré")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Le formulaire est invalide.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return resolve_url(self.request.POST.get('next'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['access_token'] = generate_access_token(self.request.user)
        if self.request.user.is_staff:
            context['rapport_consolides'] = Rapport.objects.filter(type=self.type_rapport, state=10)
            context['object_list'] = Rapport.objects.filter(type=self.type_rapport, state=0)
        else:
            context['rapport_consolides'] = self.request.user.departement.rapport_set.filter(type=self.type_rapport, state=10)
            context['object_list'] = self.request.user.departement.rapport_set.filter(
                type=self.type_rapport, state=0
            )
        return context

class RapportMensuelProgrammeView(LoginRequiredMixin, FormView):
    template_name = 'rapportage/mensuel.html'
    form_class = RapportForm
    object_list = Rapport.objects.filter(type='Mensuel-Programme')

    def get_queryset(self):
        return Rapport.objects.filter(type='Consolide')

    def form_valid(self, form):
        rapport = form.save(commit=False)
        rapport.user = self.request.user
        rapport.type = 'Consolide'
        rapport.save()
        messages.success(self.request, "Rapport enregistré")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Le formulaire est invalide.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return resolve_url('rapport:rapport-consolide')


def download_file(request, pk):
    rapport = get_object_or_404(Rapport, id=pk)
    return FileResponse(open(rapport.file.path, 'rb'))


def upload_file(request, pk):
    if request.method == 'POST':
        rapport = get_object_or_404(Rapport, id=pk)
        rapport.file = request.FILES['fichier']
        messages.success(request, "Fichier enregistré")
    return redirect(resolve_url(request.GET.get('next')))


def update_file_and_label(request, rapport_id):
    rapport = get_object_or_404(Rapport, id=rapport_id)
    if request.method == 'POST':
        rapport.file = request.FILES.get('file', rapport.file)
        rapport.label = request.POST.get('label', rapport.label)
        rapport.save()
        messages.success(request, "Le fichier et le libellé du rapport ont été mis à jour.")
    else:
        messages.error(request, "Aucune modification n'a été effectuée.")
    return redirect('rapport:mensuel')


def update_state(request, pk):
    rapport = get_object_or_404(
        Rapport,
        pk=pk)
    rapport.state = request.GET.get('status')
    rapport.save()
    return redirect(resolve_url(request.GET.get('next')))



def wopi_file_info(request, file_id):
    try:
        rapport = Rapport.objects.get(id=file_id)  # Récupérer le rapport
        # Vérifier les permissions d'accès
        """
        if not rapport.has_access(request.user):
            return HttpResponseForbidden()"""

        # Préparer les informations du fichier
        file_info = {
            'BaseFileName': rapport.label,
            'Size': rapport.file.size,
            'UserId': str(request.user.username),
            'Version': str(rapport.created),
            'ReadOnly': False,
            "UserCanWrite": True,
            "EnableOwnerTermination": True
        }
        return JsonResponse(file_info)

    except Rapport.DoesNotExist:
        return JsonResponse({}, status=404)



@csrf_exempt  # Désactiver la protection CSRF pour les requêtes WOPI
def wopi_file_contents(request, file_id):
    try:
        rapport = Rapport.objects.get(id=file_id)
        # Vérifier les permissions
        """
        if not rapport.has_access(request.user):
            return HttpResponseForbidden()
        """

        if request.method == 'GET':
            # Télécharger le contenu du fichier
            with rapport.file.open('rb') as f:
                response = HttpResponse(f.read(), content_type='application/octet-stream')
                response['X-WOPI-ItemVersion'] = str(rapport.created)
                return response

        elif request.method == 'POST':
            # Enregistrer les modifications du fichier
            try:
                with open(rapport.file.path, 'wb') as f:
                    f.write(request.body)
            except Exception as e:
                return HttpResponse(status=500)
            rapport.save()
            return HttpResponse(status=200)

        elif request.method == 'PUT':
            # sauvegarder le contenu du body de la requete dans le fichier
            try:
                with open(rapport.file.path, 'wb') as f:
                    f.write(request.body)
            except Exception as e:
                return HttpResponse(status=500)
            rapport.save()
            return HttpResponse(status=200)

    except Rapport.DoesNotExist:
        return HttpResponse(status=404)



def delete_rapport(request, pk):
    rapport = get_object_or_404(Rapport, id=pk)
    rapport.delete()
    return redirect(resolve_url(request.GET.get('next')))

