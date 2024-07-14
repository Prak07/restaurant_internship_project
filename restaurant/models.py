from django.db import models

# Create your models here.
class Restaurant(models.Model):
    id=models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255,null=True)
    items = models.JSONField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    full_details = models.JSONField(null=True)
    
    def __str__(self):
        return self.name