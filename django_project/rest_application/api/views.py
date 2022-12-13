import csv, json

from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status

from ..application_package.get_query_params import get_query_params

from ..models import Profile
from .serializers import ProfileSerializer


class MyPagination(PageNumberPagination):
    page_size = 5


@api_view(["GET", "POST"])
def get_post_profile(request):
    if request.method == "GET":
        try:
            profiles = get_query_params(request, Profile)
            if profiles == "not found":
                return Response(status=status.HTTP_404_NOT_FOUND)
            elif profiles == "bad request":
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            profiles = Profile.objects.all()
        pagination_class = MyPagination()
        paginated_queryset = pagination_class.paginate_queryset(profiles, request)
        serializer = ProfileSerializer(paginated_queryset, many=True)
        return pagination_class.get_paginated_response(serializer.data)

    elif request.method == "POST":
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            data["personal_id"] = data["personal_id"].replace("-", "").replace(".", "")
            data["name"] = data["name"].title()
            data["last_name"] = data["last_name"].title()
            serializer = ProfileSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if "ManageAssert" in request.headers:
            if request.headers["ManageAssert"] == "True":
                return Response({"errors": serializer.errors})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def get_put_delete_profile(request, pk):

    if "ManageAssert" in request.headers:
        if request.headers["ManageAssert"] == "True":
            if not pk.isdigit():
                return Response({"errors": {"personal_id": ["ID must be a number"]}})
            else:
                return Response({"errors": {"personal_id": ["ID not found"]}})

    if not pk.isdigit():
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        profile = Profile.objects.get(pk=pk)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            data["personal_id"] = data["personal_id"].replace("-", "").replace(".", "")
            serializer = ProfileSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        profile.delete()
        # if 'ManageAssert' in request.headers:
        #     return Response({'status': 'deleted'})
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def download_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="download-profiles.csv"'
    writer = csv.writer(response)
    writer.writerow(["personal_id", "name", "last_name", "age"])

    profiles = get_query_params(request, Profile)

    for row in profiles:
        writer.writerow([row.personal_id, row.name, row.last_name, row.age])
    return response
