

from core.models import Exercice


class ExerciceMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.exercices = Exercice.objects.all()
        request.current_exercice = request.exercices[0]
        response = self.get_response(request)
        return response