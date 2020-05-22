from django.test import TestCase
from django.urls import reverse
from finance.models import Basket, Donation, Merchandise
from datetime import datetime


class BasketViewTest(TestCase):
    @classmethod
    def setUp(self):
        self.donation = Donation(campaign="help the donkeys", target=100.5, amount_2_donate=10.2, giftaid=True,
                                  giftaid_detail=None, donation_quantity=1)
        self.donation.save()
        self.t_shirt = Merchandise(merchandise_name='branded t-shirt', stock_number="XS255478",
                                   merchandise_description="tshirt with charity branding", price=10.6,
                                   merchandise_quantity=1)
        self.t_shirt.save()
        self.new_basket = Basket(basket_id="DM2405891245", date=datetime.now(), paid=False, total_cost=0)
        self.new_basket.save()
        self.new_basket.add(self.t_shirt)
        self.new_basket.add(self.donation)
        self.new_basket.save()

    def test_url_exists(self):
        """test response from url"""
        response = self.client.get('/basket')
        self.assertEqual(response.status_code, 200)

    def test_url_by_name(self):
        """test endpoint through reverse"""
        response = self.client.get(reverse('basket'))
        self.assertEqual(response.status_code, 200)

    def test_basket_contents(self):
        """See if basket was creeated successfully"""
        self.assertEqual(self.new_basket.basket_id, "DM2405891245")
        self.assertEqual(self.new_basket.total_cost, 20.8)
