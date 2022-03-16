from datetime import date
from django.db import models
from django.contrib.auth.models import User


class Gadget(models.Model):

    class AcquisitionType(models.TextChoices):
        PURCHASE = 'PC', 'Purchase'
        GIFT = 'GF', 'Gift'

    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255, null=True)
    brand = models.CharField(max_length=255, null=True)
    acquisition_type = models.CharField(
        max_length=2,
        choices=AcquisitionType.choices,
        default=AcquisitionType.PURCHASE
    )
    free_form = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def acquisition(self):
        if self.acquisition_type == 'PC':
            return self.purchase
        else:
            return self.gift


class Purchase(models.Model):
    date = models.DateField()
    price_ati = models.IntegerField(default=0)
    shop = models.CharField(max_length=255, null=True)
    gadget = models.OneToOneField(
        Gadget, on_delete=models.CASCADE, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.gadget.acquisition_type = 'PC'
        self.gadget.save()
        super().save(*args, **kwargs)

    def param1(self):
        return self.date

    def param2(self):
        return self.price_ati

    def param3(self):
        return self.shop


class Gift(models.Model):
    date = models.DateField()
    sender = models.CharField(max_length=255)
    reason = models.CharField(max_length=255)
    gadget = models.OneToOneField(
        Gadget, on_delete=models.CASCADE, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.gadget.acquisition_type = 'GF'
        self.gadget.save()
        super().save(*args, **kwargs)

    def param1(self):
        return self.date

    def param2(self):
        return self.sender

    def param3(self):
        return self.reason


class Catalogue(models.Model):
    url = models.URLField()
    gadget = models.ForeignKey(Gadget, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CustomUser(User):
    class Meta:
        proxy = True

    def get_gadgets_with_relations(self):
        return Gadget.objects.select_related().filter(user=self)
