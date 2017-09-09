import os
from backend.api import serializers
from backend.cases.models import (
    Case,
    Candidate,
    Nodule,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from backend.images.models import ImageSeries
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.views import APIView
from django.core.files.storage import FileSystemStorage


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

    def get(self, request):
        """
        Return a sorted(by name) list of files and folders 
        in dataset in the form
        {'directories': [
            {
                'name': directory_name1,
                'children': [ file_name1, file_name2, ... ]
            }, ... ]
        }
        
        TODO Dynamically fetch deeper directories
        """
        # example source:
        # /images/LIDC-IDRI-0001/1.3.6.1.4.1.14519.5.2.1.6279.6001.298806137288633453246975630178
        src_dir = os.environ.get('IMAGE_SOURCE', '/images')
        fss = FileSystemStorage(src_dir)
        list_dirs = fss.listdir(src_dir)
        dirs = sorted(list_dirs[0])
        tree = []
        if dirs:
            for dirname in dirs:
                dir_contents = fss.listdir(os.path.join(src_dir, dirname))
                filenames = sorted(dir_contents[1])
                dir_node = {
                    'name': dirname,
                    'children': filenames
                }   
                tree.append(dir_node)
        return JsonResponse({'directories': tree})


def candidate_mark(request, candidate_id):
    return JsonResponse({'response': "Candidate {} was marked".format(candidate_id)})


def candidate_dismiss(request, candidate_id):
    return JsonResponse({'response': "Candidate {} was dismissed".format(candidate_id)})
