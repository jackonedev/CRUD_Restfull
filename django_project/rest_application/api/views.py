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
    if "ManageAssert" in request.headers:
        if request.headers["ManageAssert"] == "True":
            serializer = ProfileSerializer(data=request.data)
            if serializer.is_valid():
                pass
            if request.method == "GET":
                data = get_query_params(request, Profile)
                if data == "not found":
                    return Response({"errors": {"Database": ["Profile not found"]}})
                elif data == "bad request":
                    return Response({"errors": {"Database": ["Bad request"]}})

                return Response({"errors": {"errorWHY": ["ERROR VER ESTO"]}})
                
            elif request.method == "POST":
                return Response({"errors": serializer.errors})

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
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def get_put_delete_profile(request, pk):

    if "ManageAssert" in request.headers:
        if request.headers["ManageAssert"] == "True":
            if not pk.isdigit():
                return Response({"errors": {"personal_id": ["ID must be a number"]}})
            
            elif request.method == "PUT":
                serializer = ProfileSerializer(data=request.data)
                if serializer.is_valid():
                    print ('something goes wrong')
                return Response({"errors": serializer.errors})
            
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
        print ('\nDENTRO DEL PUT\n')
        print (request.data)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            data["personal_id"] = data["personal_id"].replace("-", "").replace(".", "")
            data["name"] = data["name"].title()
            data["last_name"] = data["last_name"].title()
            if serializer.is_valid():
                serializer.save()
                if pk != data["personal_id"]:
                    profile = Profile.objects.get(pk=pk)
                    profile.delete()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def download_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="download-profiles.csv"'
    writer = csv.writer(response)
    writer.writerow(["personal_id", "name", "last_name", "age"])

    profiles = get_query_params(request, Profile)

    if "ManageAssert" in request.headers:
        if request.headers["ManageAssert"] == "True":
            return Response({"errors": {"response status code": [profiles]}})

    if profiles == "not found":
        return Response(status=status.HTTP_404_NOT_FOUND)

    elif profiles == "bad request":
        return Response(status=status.HTTP_400_BAD_REQUEST)

    for row in profiles:
        writer.writerow([row.personal_id, row.name, row.last_name, row.age])
    return response
