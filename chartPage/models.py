from django.db import models

# Create your models here.

class Region_Info():
    name = models.CharField(max_length=10)
    data = []

    def __init__(self, id:int, name:str, crime_data:list):
        self.id = id
        self.name = name
        self.data = crime_data
        