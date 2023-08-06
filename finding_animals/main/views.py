from django.shortcuts import render
from .apps import MainConfig
import pandas as pd
import numpy as np

# Create your views here.
def index(request):
    spec = MainConfig.animal_data.data_species
    hair = MainConfig.animal_data.data_haircolor
    spec = spec["species"].to_list()
    hair = hair["hairColor"].to_list()

    context = {
        "species": spec,
        "haircolor": hair,
    }

    return render(request, "main/index.html", context)

def search(request):
    if request.method == "POST":
        params = {
            "classfication": "2",
            "gender": "1",
            "gu": "1",
            "age": "3",
            "weight": "5",
        }
        data = MainConfig.animal_data.search(params)
        return render(request, "main/search.html", params)
