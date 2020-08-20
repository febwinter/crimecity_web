from django.db import models

# Create your models here.

class NewsData():
    title = models.CharField(max_length=255, blank=True)
    image = models.CharField(max_length=255)
    summary = models.CharField(max_length=255)
    link = models.CharField(max_length=255)

    def __init__(self, title, image, summary, link):
        self.title = title
        self.image = image
        self.summary = summary
        self.link = link
