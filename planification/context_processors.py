from core.models import  Exercice


def exercice_params(request):
    try:
        exercice = Exercice.objects.get(pk=request.session.get('current_exercice',1))
        print(exercice)
        return {
            'exercice_list': Exercice.objects.all(),
            'current_exercice': f"{exercice.date_debut} - {exercice.date_fin}",
        }
    except Exception as e:
        raise e

    finally:
        return {}