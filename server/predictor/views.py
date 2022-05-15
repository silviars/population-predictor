from django.http import JsonResponse
from rest_framework.decorators import api_view
from .predictor import expected_population, top_n_populated


@api_view(['GET'])
def country_population(request):
    query_params = request.query_params.dict()

    country = query_params['name']
    year = int(query_params['year'])

    result = expected_population(country, year)

    if result:
        return JsonResponse(result.__dict__, safe=False)
    else:
        return JsonResponse({"message": f"{country} is not present in the dataset."})


@api_view(['GET'])
def top_populated_countries(request):
    query_params = request.query_params.dict()

    year = int(query_params['year'])

    result = top_n_populated(year)

    return JsonResponse(result, safe=False)
