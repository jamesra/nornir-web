# Create your views here.

import os

from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.views import generic

from . import models


class DatasetIndexView(generic.ListView):

    template_name = os.path.join('volume_server', 'index.html')
    context_object_name = 'datasets'

    def get_queryset(self):
        return models.Dataset.objects.order_by('name')


def get_bounds(request, dataset_name, coordspace_name):
    db_dataset = get_object_or_404(models.Dataset, name=dataset_name)
    db_coordspace = get_object_or_404(models.CoordSpace, dataset=db_dataset, name=coordspace_name)

    bounds = db_coordspace.GetBounds()
    context = {'dataset_name': dataset_name,
               'bounds': bounds}
    return render(request, 'volume_server/bounds.html', context)