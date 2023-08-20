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

# 유기동물 검색
def search(request):
    if request.method == "POST":
        animalData = AnimalData(MainConfig.haircolors)
        params = json.loads(request.body)

        data, count, total_count, sim_count = animalData.search(params)
        return JsonResponse({"result": data, "count": count, "total_count": total_count, "sim_count": sim_count} , safe=False)

# 이미지 전처리
def process_image(imageFile):
    imageFile = base64.b64decode(imageFile.split(",")[1])
    img = Image.open(io.BytesIO(imageFile))
    img = np.array(img, dtype="float32")
    img = img[:,:,:3]
    img = img.reshape(224, 224, 3)
    return img

# 업로드된 이미지 처리
def upload(request):
    if request.method == "POST":
        imageFile = request.POST.get("image_data", "")
        classification = request.POST.get("classification", "")

        if classification != "1" and classification != "2":
            return JsonResponse({"result": {}}, safe=False)
        
        # Process image
        img = process_image(imageFile)
        # print(img.shape)

        # Get prediction
        pred = MainConfig.deepModel.predict(img, is_cat=(classification == "2"))

        # Get list of rank
        ranks = MainConfig.deepModel.get_rank(pred, is_cat=(classification == "2"))

        # dataframe to list
        df = pd.DataFrame(ranks, columns=["name"])
        ranks = df["name"].tolist()

        pred = pred[1][0].tolist()

        return JsonResponse({"ranks": ranks, "predict": pred, "classification": classification}, safe=False)
