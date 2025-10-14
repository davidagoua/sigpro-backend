from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.views import generic
from django.contrib.auth import logout

from core.forms import UserCreationWithRoleForm
from core.models import User
from core.services import upload_ptba
from planification.models import Tache, PTBAProjet, Exercice

from .models import Departement, Role

class HomePageView(LoginRequiredMixin, generic.TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):

        ptba = PTBAProjet.objects.first()

        return kwargs | {
            'nb_projects': Tache.objects.all().count() ,
            'nb_projects_pending': Tache.objects.filter(status_execution=10).count(),
            'nb_projects_completed': Tache.objects.filter(status_execution=20).count() ,
            'nb_projects_upcoming': Tache.objects.filter(status_execution=0).count() ,
            'ptba': ptba,
        }


class CartigraphieView(LoginRequiredMixin, generic.TemplateView):
    template_name = "carto.html"


class AnalyseView(LoginRequiredMixin, generic.TemplateView):
    template_name = "analyse.html"


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecté avec succès.")
    return redirect('login')  # Remplacez 'login' par l'URL nommée ou le chemin de votre page de connexion


@login_required
def create_user_view(request):
    users = User.objects.all()
    if request.method == 'POST':
        form = UserCreationWithRoleForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Utilisateur créé avec succès.')
            return redirect('create_user')  # Redirigez vers la liste des utilisateurs (modifiez selon vos besoins)
    else:
        form = UserCreationWithRoleForm()

    return render(request, 'create_user.html', {'form': form, 'users': users})


@login_required
def delete_user_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    messages.success(request, 'Utilisateur supprimé avec succès.')
    return redirect('create_user')  # Redirigez vers la liste des utilisateurs (modifiez selon vos besoins)



def test_import(request):
    return JsonResponse(upload_ptba(), safe=False)


def seed_compte(request):
    admin = User.objects.get(username='admin')

    admin.departement = Departement.objects.first()
    admin.save()

    return JsonResponse(data={'response': 'ok'})


def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('password')
        new_password = request.POST.get('new_password')

        if request.user.check_password(current_password):
            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, 'Mot de passe modifié avec succès.')
            return redirect(resolve_url(request.GET.get('next')))
        else:
            messages.error(request, 'Mot de passe actuel incorrect.')
            return redirect(resolve_url(request.GET.get('next')))
   
    return render(request, 'change_password.html')


def update_current_exercice(request):
    if request.method == "POST":
        current_exercice = get_object_or_404(Exercice, pk=request.POST.get('exercice'))
        request.session['current_exercice'] = current_exercice.id
        messages.success(request, "Exercice modifié")
    return redirect(request.META.get('HTTP_REFERER', '/'))