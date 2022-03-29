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
    # success_url = reverse_lazy('gadgets:new_purchase')

    def get_success_url(self):
        if self.request.POST['acquisition_type'] == 'PC':
            return reverse_lazy('gadgets:new_purchase')
        else:
            return reverse_lazy('gadgets:new_gift')


class CreatePurchaseView(generic.edit.CreateView):
    template_name = 'gadgets/create_purchase.html'
    model = Purchase
    form_class = PurchaseForm
    success_url = reverse_lazy('gadgets:index')

    def form_valid(self, form):
        form.instance.gadget_id = self.request.POST['gadget_id']
        return super().form_valid(form)


class CreateGiftView(generic.edit.CreateView):
    template_name = 'gadgets/create_purchase.html'
    model = Gift
    form_class = GiftForm
    success_url = reverse_lazy('gadgets:index')
