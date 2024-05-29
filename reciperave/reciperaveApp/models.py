from django.db import models

# Create your models here.
class upload(models.Model):
    recipe_name = models.CharField(max_length=50)
    total_time = models.IntegerField()
    dishType = models.CharField(max_length=20)
    description = models.CharField(max_length=255)
    photo_video = models.FileField(upload_to='picture')
    instruction = models.CharFiels(max_length=1500)
    class Meta:
        db_table = "upload"