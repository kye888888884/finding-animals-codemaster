from django.apps import AppConfig
from .deepmodel import DeepModel
import pandas as pd

init_db = True
load_path = "main/data/"

class MainConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "main"
    haircolors = {
        'colorWhite': "흰색",
        'colorBlack': "검은색",
        'colorBrown': "갈색",
        'colorYellow': "황색",
        'colorGray': "회색",
        'colorOther': "기타",
    }
    feature_dog = pd.read_csv(load_path + "feature_dog.csv")
    feature_cat = pd.read_csv(load_path + "feature_cat.csv")
    deepModel = DeepModel()
