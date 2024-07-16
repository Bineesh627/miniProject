from django.db import models

# Create your models here.
class upload1(models.Model):
    uid = models.CharField(max_length=50)
    recipe_name = models.CharField(max_length=50)
    total_time = models.IntegerField()
    dishType = models.CharField(max_length=20)
    description = models.CharField(max_length=255)
    photo_video = models.FileField(upload_to='pictures')
    instruction = models.CharField(max_length=1500)
    class Meta:
        db_table = "recp"