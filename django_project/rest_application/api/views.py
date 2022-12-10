from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status

from ..application_package.get_query_params import get_query_params

from ..models import Profile
from .serializers import ProfileSerializer


class MyPagination(PageNumberPagination):
    page_size = 10

@api_view(['GET', 'POST'])
def get_post_profile(request):
    if request.method == 'GET':
        try:
            profiles = get_query_params(request, Profile)
            if profiles == 'not found':
                return Response(status=status.HTTP_404_NOT_FOUND)
            elif profiles == 'bad request':
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            profiles = Profile.objects.all()
        
        serializer = ProfileSerializer(profiles, many=True)
        



    elif request.method == 'POST':
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            data['personal_id'] = data['personal_id'].replace('-', '').replace('.', '')
            serializer = ProfileSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







@api_view(['GET', 'PUT', 'DELETE'])
def get_put_delete_profile(request, pk):
    if not pk.isdigit():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    try:
        profile = Profile.objects.get(pk=pk)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            data['personal_id'] = data['personal_id'].replace('-', '').replace('.', '')
            serializer = ProfileSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def download_csv(request):
    pass