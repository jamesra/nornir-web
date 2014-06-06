# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
import volume_importer.models as models

def index(request):
    Volumes = list(models.GetVolumes())
    context = {'volume_list' : list(Volumes)}
    return render(request, 'volumelist.html', context)

class IndexView(generic.ListView):
    template_name = 'volume_importer/volumelist.html'
    context_object_name = 'volume_list'

    def get_queryset(self):
        return list(models.GetVolumes())