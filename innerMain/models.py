from django.db import models
from django.urls import reverse

# Create your models here.

class NewsData(models.Model):

    title = models.CharField(max_length=255, blank=True)
    image = models.CharField(max_length=255)
    summary = models.CharField(max_length=255)
    link = models.CharField(max_length=255)

    class Meta:
        verbose_name = "NewsData"
        verbose_name_plural = "NewsDatas"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("NewsData_detail", kwargs={"pk": self.pk})
