from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

from gadgets.models import Gadget


class IndexView(generic.ListView):
    template_name = 'gadgets/index.html'
    context_object_name = 'gadget_list'

    def get_queryset(self):
        return Gadget.objects.select_related()
