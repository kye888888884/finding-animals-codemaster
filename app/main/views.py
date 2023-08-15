import json
from django.shortcuts import render
from django.http import JsonResponse
from .apps import MainConfig
import pandas as pd
import numpy as np

# Create your views here.
def index(request):
    hair = MainConfig.animal_data.data_haircolor
    hair = hair["hairColor"].to_list()

    context = {
        "haircolor": hair,
    }

    return render(request, "main/index.html", context)

def search(request):
    if request.method == "POST":
        params = json.loads(request.body)
        data, count, total_count = MainConfig.animal_data.search(params)
        return JsonResponse({"result": data, "count": count, "total_count": total_count}, safe=False)