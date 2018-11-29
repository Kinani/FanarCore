from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileSerializer
import subprocess
# from .fanar_cv import find_face

class FileView(APIView):
  parser_classes = (MultiPartParser, FormParser)
  def post(self, request, *args, **kwargs):
    file_serializer = FileSerializer(data=request.data)
    if file_serializer.is_valid():
      file_serializer.save()
      # print(file_serializer.data['file'])
      # cv_status = find_face(file_serializer.data['file'])
      # cv_status_json = {"status":"{0}".format(cv_status)}
      completed = subprocess.run(
        ['python', 'face-find.py', "."+file_serializer.data['file']],
        stdout=subprocess.PIPE,
      )
      result = completed.stdout.decode('ascii').strip()
      print(result)

      if result != "Found encodings":
        completed2 = subprocess.run(
        ['python', 'face-add.py', "."+file_serializer.data['file']],
        stdout=subprocess.PIPE,
        )
        result = completed2.stdout.decode('ascii').strip()
        print(result)

      # completed = subprocess.run(
      #   ['pwd'],
      #   stdout=subprocess.PIPE,
      # )
      # file_serializer.data['cv_result'] = completed.stdout.decode('utf-8')
      # return Response(cv_status_json, status=status.HTTP_201_CREATED)
      return Response(result, status=status.HTTP_201_CREATED)
    else:
      return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
