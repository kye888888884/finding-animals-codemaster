from django.shortcuts import render
from .apps import MainConfig
import pandas as pd
import numpy as np

# Create your views here.
def index(request):
    data = MainConfig.animal_data.data
    species = data["kindCd"].unique()
    context = {"hi": "hello world"}
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
        return render(request, "main/search.html", params)
