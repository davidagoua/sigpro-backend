from planification.models import  Exercice


def exercice_params(request):
    exercice = Exercice.objects.get(pk=request.session.get('current_exercice',1))

    return {
        'exercice_list': Exercice.objects.all(),
        'current_exercice': f"{exercice.date_debut} - {exercice.date_fin}",
    }