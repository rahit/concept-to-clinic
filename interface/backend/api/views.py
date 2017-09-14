import os

from backend.api import serializers
from backend.cases.models import (
    Case,
    Candidate,
    Nodule,
)
from rest_framework.views import APIView 
from backend.images.models import ImageSeries
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView


class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = serializers.CaseSerializer


class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = serializers.CandidateSerializer


class NoduleViewSet(viewsets.ModelViewSet):
    queryset = Nodule.objects.all()
    serializer_class = serializers.NoduleSerializer


class ImageSeriesViewSet(viewsets.ModelViewSet):
    queryset = ImageSeries.objects.all()
    serializer_class = serializers.ImageSeriesSerializer


class ImageAvailableApiView(APIView):
    """
    View list of images from dataset directory
    """

    def __init__(self, *args, **kwargs):
        super(ImageAvailableApiView, self).__init__(**kwargs)
        self.fss = FileSystemStorage(settings.DATASOURCE_DIR)

    def walk(self, location, dir_name='root'):
        """
        Recursively walkthrough directories and files
        """
        list_dirs = self.fss.listdir(location)
        tree = {
            'name': dir_name,
            'children': [],
        }
        tree['children'] = sorted(list_dirs[1])
        for dirname in sorted(list_dirs[0]):
            tree['children'].append(self.walk(os.path.join(location, dirname), dirname))
        return tree

    def get(self, request):
        """
        Return a sorted(by name) list of files and folders
        in dataset in the form
        {'directories': [
            {
                'name': directory_name1,
                'children': [
                    file_name1,
                    file_name2,
                    {
                        'name': 'nested_dir_1',
                        'children': [
                            'file_name_1',
                            'file_name_2',
                            ....
                        ]
                    }
                    ... ]
            }, ... ]
        }
        """
        tree = self.walk(settings.DATASOURCE_DIR)
        return Response({'directories': tree})


@api_view(['GET'])
def candidate_mark(request, candidate_id):
    return Response({'response': "Candidate {} was marked".format(candidate_id)})


@api_view(['GET'])
def candidate_dismiss(request, candidate_id):
    return Response({'response': "Candidate {} was dismissed".format(candidate_id)})
