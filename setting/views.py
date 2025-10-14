from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views import generic
from .models import Vehicule, EmpruntVehicule
from .forms import VehiculeForm, EmpruntVehiculeForm

# Vues pour les composantes

class ComposanteTemplateView(generic.TemplateView):
    template_name = 'settings/composantes.html'

    def get_context_data(self, **kwargs):

        return kwargs | locals()

# Vues pour les véhicules

def vehicule_list(request):
    vehicules = Vehicule.objects.all()
    return render(request, 'settings/vehicule_list.html', {'vehicules': vehicules})

class VehiculeDetailsView(generic.DetailView):
    model = Vehicule
    template_name = 'settings/vehicule_details.html'

def vehicule_add(request):
    if request.method == 'POST':
        form = VehiculeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Véhicule ajouté avec succès')
            return redirect('setting:vehicule_list')
    else:
        form = VehiculeForm()
    return render(request, 'settings/vehicule_form.html', {'form': form, 'title': 'Ajouter un véhicule'})

def vehicule_edit(request, pk):
    vehicule = get_object_or_404(Vehicule, pk=pk)
    if request.method == 'POST':
        form = VehiculeForm(request.POST, instance=vehicule)
        if form.is_valid():
            form.save()
            messages.success(request, 'Véhicule mis à jour avec succès')
            return redirect('setting:vehicule_list')
    else:
        form = VehiculeForm(instance=vehicule)
    return render(request, 'settings/vehicule_form.html', {'form': form, 'title': 'Modifier un véhicule'})

# Vues pour les emprunts de véhicules

def emprunt_list(request):
    emprunts = EmpruntVehicule.objects.all()
    return render(request, 'settings/emprunt_list.html', {'emprunts': emprunts})

def emprunt_add(request):
    if request.method == 'POST':
        form = EmpruntVehiculeForm(request.POST)
        print(request.POST)
        if form.is_valid():
            data = form.save()
            #Vehicule.objects.get(pk=form.vehicule_id).update()
            messages.success(request, 'Emprunt enregistré avec succès')
            return redirect('setting:emprunt_list')
        else:
            print(form.errors)
    else:
        form = EmpruntVehiculeForm()
    return render(request, 'settings/emprunt_form.html', {'form': form, 'title': 'Enregistrer un emprunt',  'is_update': False})

def emprunt_edit(request, pk):
    emprunt = get_object_or_404(EmpruntVehicule, pk=pk)

    form = EmpruntVehiculeForm( instance=emprunt)
    form.fields['km_out'].disabled = True
    form.fields['nom_prenom'].disabled = True
    form.fields['nom_chauffeur'].disabled = True

    if request.method == 'POST':
        form = EmpruntVehiculeForm(request.POST, instance=emprunt)
        if form.is_valid():
            form.save()
            messages.success(request, 'Emprunt mis à jour avec succès')
            return redirect('setting:emprunt_list')
    else:
        form = EmpruntVehiculeForm(instance=emprunt)
    return render(request, 'settings/emprunt_form.html', {'form': form, 'title': 'Modifier un emprunt', 'is_update': True})


def delete_vehicule(request, pk):
    Vehicule.objects.get(pk=pk).delete()
    messages.success(request, "Vehicule supprimé")
    return redirect(request.GET['next'])