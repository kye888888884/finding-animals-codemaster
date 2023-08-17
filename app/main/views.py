import json
from django.shortcuts import render
from django.http import JsonResponse
from .apps import MainConfig
import pandas as pd
import numpy as np
from .data import AnimalData

# Create your views here.
def index(request):
    context = {
        "haircolors": MainConfig.haircolors,
    }

    return render(request, "main/index.html", context)

def search(request):
    if request.method == "POST":
        animalData = AnimalData(MainConfig.haircolors)
        params = json.loads(request.body)
        data, count, total_count = animalData.search(params)
        return JsonResponse({"result": data, "count": count, "total_count": total_count}, safe=False)
