from platform import release
from django.db import models

from accounts.models import CustomUser
# Create your models here.
class Anime(models.Model):
    user            = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="animes")
    title           = models.CharField(max_length=256)
    overview        = models.TextField()
    release_date    = models.DateField()
    vote_average    = models.FloatField()
    vote_count      = models.IntegerField()
    data_created_at = models.DateTimeField(auto_now_add=True)
    data_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title