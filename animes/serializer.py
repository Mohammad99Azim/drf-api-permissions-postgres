
from rest_framework.serializers import (ModelSerializer,CharField,PrimaryKeyRelatedField,CurrentUserDefault)


from .models import Anime



class AnimeSerializer(ModelSerializer):
    user_name = CharField(source = 'user.username' , read_only=True)
    user = PrimaryKeyRelatedField(read_only=True, default=CurrentUserDefault())
   
    class Meta:
        model = Anime
        fields = ['id','user','user_name','title','overview','release_date','vote_average','vote_count','data_created_at','data_updated_at']