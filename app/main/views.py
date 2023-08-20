import json
from django.shortcuts import render
from django.http import JsonResponse
from .apps import MainConfig
import pandas as pd
import numpy as np
from .data import AnimalData
import base64
import io
from PIL import Image
from .models import Animals, Species

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

# Create your views here.
def process_image(imageFile):
    imageFile = base64.b64decode(imageFile.split(",")[1])
    img = Image.open(io.BytesIO(imageFile))
    img = np.array(img, dtype="float32")
    img = img[:,:,:3]
    img = img.reshape(224, 224, 3)
    return img

def upload(request):
    if request.method == "POST":
        imageFile = request.POST.get("image_data", "")
        classification = request.POST.get("classification", "")

        if classification != "1" and classification != "2":
            return JsonResponse({"result": {}}, safe=False)
        
        # Process image
        img = process_image(imageFile)
        print(img.shape)

        result = MainConfig.deepModel.predictRank(img, is_cat=(classification == "2"))

        df = pd.DataFrame(result, columns=["name"])
        
        # Eng to Kor
        # species = Species.objects.all().values()
        # df_species = pd.DataFrame(species)
        # df_species = df_species[["name", "name_kr"]]
        # dict_species = df_species.set_index("name").to_dict()["name_kr"]
        # df["name"] = df["name"].map(dict_species)

        # dataframe to list
        result = df["name"].tolist()

        # list to dict
        # result = dict(zip(range(len(result)), result))

        return JsonResponse({"result": result, "classification": classification}, safe=False)
