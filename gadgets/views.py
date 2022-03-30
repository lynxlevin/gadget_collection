from audioop import reverse
from http.client import HTTPResponse
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views import generic
from gadgets.forms import GadgetForm, GiftForm, PurchaseForm

from gadgets.models import Gadget, Gift, Purchase


class IndexView(generic.ListView):
    template_name = 'gadgets/index.html'
    context_object_name = 'gadget_list'

    def get_queryset(self):
        return Gadget.objects.select_related()


class CreateView(generic.edit.CreateView):
    template_name = 'gadgets/create.html'
    model = Gadget
    form_class = GadgetForm

    def get_success_url(self):
        query = '?gadget=' + str(self.object.id)
        if self.request.POST['acquisition_type'] == 'PC':
            return reverse_lazy('gadgets:new_purchase') + query
        else:
            return reverse_lazy('gadgets:new_gift') + query


class CreatePurchaseView(generic.edit.CreateView):
    template_name = 'gadgets/create_purchase.html'
    model = Purchase
    form_class = PurchaseForm
    success_url = reverse_lazy('gadgets:index')

    def get_initial(self):
        initial = super().get_initial()
        initial['gadget'] = self.request.GET['gadget']
        return initial


class CreateGiftView(generic.edit.CreateView):
    template_name = 'gadgets/create_gift.html'
    model = Gift
    form_class = GiftForm
    success_url = reverse_lazy('gadgets:index')

    def get_initial(self):
        initial = super().get_initial()
        initial['gadget'] = self.request.GET['gadget']
        return initial
