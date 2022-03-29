from django.http import HttpRequest, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views import generic
from gadgets.forms import GadgetForm

from gadgets.models import Gadget


class IndexView(generic.ListView):
    template_name = 'gadgets/index.html'
    context_object_name = 'gadget_list'

    def get_queryset(self):
        return Gadget.objects.select_related()


class CreateView(generic.edit.CreateView):
    template_name = 'gadgets/create.html'
    model = Gadget
    form_class = GadgetForm
    success_url = reverse_lazy('gadgets:index')
