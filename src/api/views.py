from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import VacationsModel
from .models import VacationSerializer

@api_view(["GET", "POST"])
def get_vacations(request):
    if request.method == 'GET':
        try:
            vacations = VacationsModel.objects.all()
            serializer = VacationSerializer(vacations, many=True)
            return Response(serializer.data)
        except Exception as err:
            json = {"error": str(err)}
            return Response(json, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'POST':
        serializer = VacationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
