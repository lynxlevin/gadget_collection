from datetime import datetime
from datetime import date
from unittest import mock
from django.test import TestCase
from django.contrib.auth.models import User

from gadgets.models import Gadget, Gift, Purchase


def create_valid_user():
    user = User()
    user_count = User.objects.count()
    user.username = 'test_user' + str(user_count)
    user.first_name = 'test'
    user.last_name = 'user'
    user.email = 'test@test'
    user.save()
    return user


def create_default_gadget(user):
    gadget = Gadget()
    gadget.name = 'test'
    gadget.user = user
    gadget.save()
    return gadget


def create_default_purchase(gadget):
    purchase = Purchase()
    purchase.date = date(2022, 3, 11)
    purchase.price_ati = 10000
    purchase.gadget = gadget
    purchase.save()
    return purchase


def create_default_gift(gadget):
    gift = Gift()
    gift.date = date(2022, 3, 11)
    gift.sender = 'Fred'
    gift.reason = 'Birthday Present'
    gift.gadget = gadget
    gift.save()
    return gift


class GadgetModelTests(TestCase):
    def test_default_values(self):
        mock_date = datetime(2022, 3, 12, 11, 38, 10, 0)
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = mock_date
            user = create_valid_user()
            gadget = create_default_gadget(user)

        self.assertEqual(gadget.name, 'test')
        self.assertEqual(gadget.model, None)
        self.assertEqual(gadget.brand, None)
        self.assertEqual(gadget.aquisition_type.value, 'PC')
        self.assertEqual(gadget.aquisition_type.name, 'PURCHASE')
        self.assertEqual(gadget.aquisition_type.label, 'Purchase')
        self.assertEqual(gadget.free_form, None)
        self.assertEqual(gadget.user, user)
        self.assertEqual(gadget.created_at, mock_date)
        self.assertEqual(gadget.updated_at, mock_date)

    def test_updated_at(self):
        mock_date = datetime(2022, 3, 12, 11, 38, 10, 0)
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = mock_date
            user = create_valid_user()
            gadget = create_default_gadget(user)

        mock_update_date = datetime(2022, 3, 13, 11, 38, 10, 0)
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = mock_update_date
            gadget.name = 'test2'
            gadget.save()

        self.assertEqual(gadget.created_at, mock_date)
        self.assertEqual(gadget.updated_at, mock_update_date)


class PurchaseModelTests(TestCase):
    def test_default_values(self):
        mock_date = datetime(2022, 3, 12, 11, 38, 10, 0)
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = mock_date
            user = create_valid_user()
            gadget = create_default_gadget(user)
            purchase = create_default_purchase(gadget)

        self.assertEqual(purchase.date, date(2022, 3, 11))
        self.assertEqual(purchase.price_ati, 10000)
        self.assertEqual(purchase.gadget, gadget)
        self.assertEqual(purchase.created_at, mock_date)
        self.assertEqual(purchase.updated_at, mock_date)

    def test_updated_at(self):
        mock_date = datetime(2022, 3, 12, 11, 38, 10, 0)
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = mock_date
            user = create_valid_user()
            gadget = create_default_gadget(user)
            purchase = create_default_purchase(gadget)

        mock_update_date = datetime(2022, 3, 13, 11, 38, 10, 0)
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = mock_update_date
            purchase.price_ati = 11000
            purchase.save()

        self.assertEqual(purchase.created_at, mock_date)
        self.assertEqual(purchase.updated_at, mock_update_date)


class GiftModelTests(TestCase):
    def test_default_values(self):
        mock_date = datetime(2022, 3, 12, 11, 38, 10, 0)
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = mock_date
            user = create_valid_user()
            gadget = create_default_gadget(user)
            gift = create_default_gift(gadget)

        self.assertEqual(gift.date, date(2022, 3, 11))
        self.assertEqual(gift.sender, 'Fred')
        self.assertEqual(gift.reason, 'Birthday Present')
        self.assertEqual(gift.gadget, gadget)
        self.assertEqual(gift.created_at, mock_date)
        self.assertEqual(gift.updated_at, mock_date)

    def test_updated_at(self):
        mock_date = datetime(2022, 3, 12, 11, 38, 10, 0)
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = mock_date
            user = create_valid_user()
            gadget = create_default_gadget(user)
            gift = create_default_gift(gadget)

        mock_update_date = datetime(2022, 3, 13, 11, 38, 10, 0)
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = mock_update_date
            gift.price_ati = 11000
            gift.save()

        self.assertEqual(gift.created_at, mock_date)
        self.assertEqual(gift.updated_at, mock_update_date)
