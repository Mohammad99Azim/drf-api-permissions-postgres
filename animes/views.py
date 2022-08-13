import imp
from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView , RetrieveUpdateDestroyAPIView
from rest_framework.serializers import ModelSerializer
from rest_framework.permissions import IsAuthenticated
from rest_condition import And, Or

from .permissions import IsOwnerOrAdmin,IsPostMethod,IsSafeMethod,IsAllowedToAdd


from .models import Anime
from .serializer import AnimeSerializer
# Create your views here.

class EventSerializer(ModelSerializer):

    class Meta:
        model = Anime
        exclude = ['user']


class AnimeListView(ListCreateAPIView):
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer
    permission_classes = [
        Or(
            And(IsPostMethod, IsAllowedToAdd),
            And(IsSafeMethod, IsAuthenticated),
        )
    ]
    def post(self, request):
        es = EventSerializer(data=request.data)
        if es.is_valid():
            es.save(user=self.request.user)
            return Response(status=status.HTTP_201_CREATED)
        return Response(data=es.errors, status=status.HTTP_400_BAD_REQUEST)

class AnimeDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer
    permission_classes = [IsOwnerOrAdmin ,IsAuthenticated ]
