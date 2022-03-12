from datetime import date
from django.db import models
from django.contrib.auth.models import User


class Gadget(models.Model):

    class AquisitionType(models.TextChoices):
        PURCHASE = 'PC', 'Purchase'
        GIFT = 'GF', 'Gift'

    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255, null=True)
    brand = models.CharField(max_length=255, null=True)
    aquisition_type = models.CharField(
        max_length=2,
        choices=AquisitionType.choices,
        default=AquisitionType.PURCHASE
    )
    free_form = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Purchase(models.Model):
    date = models.DateField()
    price_ati = models.IntegerField(default=0)
    shop = models.CharField(max_length=255, null=True)
    gadget = models.ForeignKey(Gadget, on_delete=models.CASCADE)


class Gift(models.Model):
    date = models.DateField()
    sender = models.CharField(max_length=255)
    reason = models.CharField(max_length=255)
    gadget = models.ForeignKey(Gadget, on_delete=models.CASCADE)


class Catalogue(models.Model):
    url = models.URLField()
    gadget = models.ForeignKey(Gadget, on_delete=models.CASCADE)
