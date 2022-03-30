from datetime import datetime, timedelta, timezone, date
from unittest import mock
from django.test import TestCase

from gadgets.models import Gadget, Gift, Purchase, CustomUser


def create_valid_user():
    user = CustomUser()
    user_count = CustomUser.objects.count()
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


def timezone_utc():
    return timezone(timedelta(), 'UTC')


class GadgetModelTests(TestCase):
    def test_default_values(self):
        mock_date = datetime(2022, 3, 12, 11, 38, 10, 0, timezone_utc())
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = mock_date
            user = create_valid_user()
            gadget = create_default_gadget(user)

        self.assertEqual(gadget.name, 'test')
        self.assertEqual(gadget.model, None)
        self.assertEqual(gadget.brand, None)
        self.assertEqual(gadget.acquisition_type.value, 'PC')
        self.assertEqual(gadget.acquisition_type.name, 'PURCHASE')
        self.assertEqual(gadget.acquisition_type.label, 'Purchase')
        self.assertEqual(gadget.free_form, None)
        self.assertEqual(gadget.user, user)
        self.assertEqual(gadget.created_at, mock_date)
        self.assertEqual(gadget.updated_at, mock_date)

    def test_updated_at(self):
        mock_date = datetime(2022, 3, 12, 11, 38, 10, 0, timezone_utc())
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = mock_date
            user = create_valid_user()
            gadget = create_default_gadget(user)

        mock_update_date = datetime(2022, 3, 13, 11, 38, 10, 0, timezone_utc())
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = mock_update_date
            gadget.name = 'test2'
            gadget.save()

        self.assertEqual(gadget.created_at, mock_date)
        self.assertEqual(gadget.updated_at, mock_update_date)

    def test_acquisition_returns_purchase(self):
        user = create_valid_user()
        gadget = create_default_gadget(user)
        purchase = create_default_purchase(gadget)
        result = gadget.acquisition()
        self.assertEqual(result, purchase)

    def test_acquisition_returns_gift(self):
        user = create_valid_user()
        gadget = create_default_gadget(user)
        gadget.acquisition_type = 'GF'
        gadget.save()
        gift = create_default_gift(gadget)
        result = gadget.acquisition()
        self.assertEqual(result, gift)


class PurchaseModelTests(TestCase):
    def test_default_values(self):
        mock_date = datetime(2022, 3, 12, 11, 38, 10, 0, timezone_utc())
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
        mock_date = datetime(2022, 3, 12, 11, 38, 10, 0, timezone_utc())
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = mock_date
            user = create_valid_user()
            gadget = create_default_gadget(user)
            purchase = create_default_purchase(gadget)

        mock_update_date = datetime(2022, 3, 13, 11, 38, 10, 0, timezone_utc())
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = mock_update_date
            purchase.price_ati = 11000
            purchase.save()

        self.assertEqual(purchase.created_at, mock_date)
        self.assertEqual(purchase.updated_at, mock_update_date)

    def test_gadget_acquisition_updated_on_save_purchase(self):
        user = create_valid_user()
        gadget = create_default_gadget(user)
        create_default_purchase(gadget)

        self.assertEqual(gadget.acquisition_type, 'PC')
        self.assertNotEqual(gadget.created_at, gadget.updated_at)


class GiftModelTests(TestCase):
    def test_default_values(self):
        mock_date = datetime(2022, 3, 12, 11, 38, 10, 0, timezone_utc())
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
        mock_date = datetime(2022, 3, 12, 11, 38, 10, 0, timezone_utc())
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = mock_date
            user = create_valid_user()
            gadget = create_default_gadget(user)
            gift = create_default_gift(gadget)

        mock_update_date = datetime(2022, 3, 13, 11, 38, 10, 0, timezone_utc())
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = mock_update_date
            gift.price_ati = 11000
            gift.save()

        self.assertEqual(gift.created_at, mock_date)
        self.assertEqual(gift.updated_at, mock_update_date)

    def test_gadget_acquisition_updated_on_save_gift(self):
        user = create_valid_user()
        gadget = create_default_gadget(user)
        create_default_gift(gadget)

        self.assertEqual(gadget.acquisition_type, 'GF')
        self.assertNotEqual(gadget.created_at, gadget.updated_at)


class UserModelTests(TestCase):
    def test_get_gadgets_with_relations(self):
        user = create_valid_user()
        gadget1_1 = create_default_gadget(user)
        purchase1_1 = create_default_purchase(gadget1_1)
        gadget1_2 = create_default_gadget(user)
        purchase1_2 = create_default_purchase(gadget1_2)

        result = user.get_gadgets_with_relations()
        self.assertEqual(result[0], gadget1_1)
        self.assertEqual(result[0].purchase, purchase1_1)
        self.assertEqual(result[1], gadget1_2)
        self.assertEqual(result[1].purchase, purchase1_2)
        self.assertEqual(result.count(), 2)


class CreateViewTests(TestCase):
    def test_create_gadget_with_purchase(self):
        create_valid_user()
        gadget_form = {
            'name': 'test create view',
            'model': 'test01',
            'brand': 'create view',
            'free_form': 'free form',
            'acquisition_type': 'PC',
        }
        response = self.client.post('/gadgets/separate/new', gadget_form)
        gadget = Gadget.objects.last()
        self.assertEqual(gadget.name, 'test create view')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response['location'], '/gadgets/separate/purchase?gadget=' + str(gadget.id))

    def test_create_with_only_required_param_with_purchase(self):
        create_valid_user()
        gadget_form = {
            'name': 'test create view with only required param',
            'acquisition_type': 'PC',
        }
        response = self.client.post('/gadgets/separate/new', gadget_form)
        gadget = Gadget.objects.last()
        self.assertEqual(gadget.name,
                         'test create view with only required param')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response['location'], '/gadgets/separate/purchase?gadget=' + str(gadget.id))

    def test_create_fails_without_required_params(self):
        create_valid_user()
        gadget_form = {
            'model': 'test01',
            'brand': 'create view',
            'free_form': 'free form',
        }
        response = self.client.post('/gadgets/separate/new', gadget_form)
        self.assertEqual(Gadget.objects.last(), None)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required')

    def test_create_gadget_with_gift(self):
        create_valid_user()
        gadget_form = {
            'name': 'test create view',
            'model': 'test01',
            'brand': 'create view',
            'free_form': 'free form',
            'acquisition_type': 'GF',
        }
        response = self.client.post('/gadgets/separate/new', gadget_form)
        gadget = Gadget.objects.last()
        self.assertEqual(gadget.name, 'test create view')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response['location'], '/gadgets/separate/gift?gadget=' + str(gadget.id))

    def test_create_with_only_required_param_with_gift(self):
        create_valid_user()
        gadget_form = {
            'name': 'test create view with only required param',
            'acquisition_type': 'GF',
        }
        response = self.client.post('/gadgets/separate/new', gadget_form)
        gadget = Gadget.objects.last()
        self.assertEqual(gadget.name,
                         'test create view with only required param')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response['location'], '/gadgets/separate/gift?gadget=' + str(gadget.id))
    # def test_authorized_user_is_used(self):


class CreatePurchaseViewTests(TestCase):
    def test_create_purchase(self):
        user = create_valid_user()
        gadget = create_default_gadget(user)
        purchase_form = {
            'date': '2022-03-29',
            'price_ati': 1000,
            'shop': 'test shop',
            'gadget': gadget.id,
        }
        response = self.client.post(
            '/gadgets/separate/purchase?gadget=' + str(gadget.id), purchase_form)
        self.assertEqual(Purchase.objects.last().date, date(2022, 3, 29))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/gadgets/')

    def test_create_with_only_required_params(self):
        user = create_valid_user()
        gadget = create_default_gadget(user)
        purchase_form = {
            'date': '2022-03-29',
            'price_ati': 1000,
            'gadget': gadget.id,
        }
        response = self.client.post(
            '/gadgets/separate/purchase?gadget=' + str(gadget.id), purchase_form)
        self.assertEqual(Purchase.objects.last().date, date(2022, 3, 29))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/gadgets/')

    def test_create_fails_without_required_params(self):
        user = create_valid_user()
        gadget = create_default_gadget(user)
        purchase_form = {
            'shop': 'test shop',
            'gadget': gadget.id,
        }
        response = self.client.post(
            '/gadgets/separate/purchase?gadget=' + str(gadget.id), purchase_form)
        self.assertEqual(Purchase.objects.last(), None)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required')


class CreateGiftViewTests(TestCase):
    def test_create_gift(self):
        user = create_valid_user()
        gadget = create_default_gadget(user)
        gift_form = {
            'date': '2022-03-29',
            'sender': 'John',
            'reason': 'birthday present',
            'gadget': gadget.id,
        }
        response = self.client.post(
            '/gadgets/separate/gift?gadget=' + str(gadget.id), gift_form)
        self.assertEqual(Gift.objects.last().date, date(2022, 3, 29))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/gadgets/')

    def test_create_fails_without_required_params(self):
        user = create_valid_user()
        gadget = create_default_gadget(user)
        gift_form = {
            'gadget': gadget.id,
        }
        response = self.client.post(
            '/gadgets/separate/gift?gadget=' + str(gadget.id), gift_form)
        self.assertEqual(Gift.objects.last(), None)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required')
