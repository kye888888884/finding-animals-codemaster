from django.apps import AppConfig
from .data import AnimalData

class MainConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "main"
    animal_data = AnimalData("main/data/")
