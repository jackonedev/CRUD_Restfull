from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..application_package.get_query_params import get_query_params

from ..models import Profile
from .serializers import ProfileSerializer

log = False

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
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def get_put_delete_profile(request, pk):
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
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


