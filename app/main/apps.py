from django.apps import AppConfig
from .deepmodel import DeepModel

init_db = True

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
    deepModel = None#DeepModel()
