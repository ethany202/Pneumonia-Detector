from django.db import models

class SaliencyImage(models.Model):
    image = models.ImageField(upload_to='images/')