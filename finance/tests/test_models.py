from django.test import TestCase
from events.models import Event
from people.models import Role, Person
from ..models import Donation, Giftaid, Merchandise, Basket, Ticket
from datetime import datetime, timedelta
from django.contrib.auth.models import User


class FinanceTest(TestCase):
    """Test ticket module"""
    @classmethod
    def setUp(self):
        self.initial_ticket_count = len(list(Ticket.objects.all()))
        self.initial_merchandise_count = len(list(Merchandise.objects.all()))
        self.user = User(username='emorse2')
        self.user.save()
        self.role = Role.objects.create(role_name="nearly all_things", role_responsibility="make nearly it all work")
        self.role.save()
        self.top_role = Role.objects.create(role_name="all_things", role_responsibility="make it all work")
        self.top_role.save()
        self.person_a = Person.objects.create(userid=self.user, email="joebloggs@email.com", first_name="joe",
                                        second_name="bloggs", date_of_birth=datetime.strptime("1985-06-21", "%Y-%m-%d"),
                                        postcode="S1 9AA", address= "29, Acacia Road, Nuttytown", organisation_role=self.role,
                                        allowed_access=3, notes="likes pizza", line_manage=self.top_role)
        self.event_a = Event.objects.create(title="summer fete",
                                  start=datetime.strptime("2020-07-03 12:00", "%Y-%m-%d %H:%M"),
                                  end=datetime.strptime("2020-07-03 16:00", "%Y-%m-%d %H:%M"), event_owner=self.person_a,
                                  duration=timedelta(hours=4),
                                  recurring=False, description="happy summer fete", website_publish=True)
        self.person_a.save()
        self.event_a.save()

        self.couple_ticket = Ticket(event=self.event_a, price=12.0, ticket_type=1, ticket_quantity=2)
        self.family_ticket = Ticket(event=self.event_a, price=30.5, ticket_type=3, ticket_quantity=1)
        self.oap_ticket = Ticket(event=self.event_a, price=8.5, ticket_type=4, ticket_quantity=2)
        self.student_ticket = Ticket(event=self.event_a, price=9.0, ticket_type=5, ticket_quantity=1)
        self.couple_ticket.save()
        self.family_ticket.save()
        self.oap_ticket.save()
        self.student_ticket.save()
        self.mug = Merchandise(merchandise_name='branded mug', stock_number="XS254789",
                        merchandise_description="mug with charity branding", price=5.5, merchandise_quantity=1)
        self.mug.save()
        self.t_shirt = Merchandise(merchandise_name='branded t-shirt', stock_number="XS255478",
                        merchandise_description="tshirt with charity branding", price=10.6, merchandise_quantity=1)
        self.t_shirt.save()
        self.initial_donation_count = len(list(Donation.objects.all()))
        self.giftaid_a = Giftaid(name="Joe Bloggs", first_line_address="12, Anywhere street, Newtown", city="Cardiff",
                                 postcode="CF120UX",country="Wales",phone_number="00000000000")
        self.giftaid_a.save()
        self.donation1 = Donation(campaign="help the donkeys", target=100.5,
                                amount_2_donate=10.2, giftaid=True, giftaid_detail=self.giftaid_a,
                                donation_quantity=1)
        self.donation1.save()

    def test_ticket_created_number(self):
        """Check that all the tickets instantiated in setUp have been created"""
        new_count = len(list(Ticket.objects.all()))
        self.assertNotEqual(self.initial_ticket_count, new_count)
        self.assertEqual(4, new_count)

    def test_ticket_content(self):
        """Ensure tickets created with right content"""
        ticket1 = Ticket.objects.get(price=12.0)
        self.assertEqual(ticket1, self.couple_ticket)
        ticket2 = Ticket.objects.get(price=30.5)
        self.assertEqual(ticket2, self.family_ticket)

    def test_merchandise_created_number_and_content(self):
        """test to see if merchandise objects have been added to db"""
        merchandise1 = Merchandise.objects.get(merchandise_name="branded mug")
        self.assertEqual(merchandise1.stock_number, "XS254789")
        self.assertEqual(merchandise1.price, 5.5)
        self.assertEqual(merchandise1.merchandise_quantity, 1)
        second_count = len(list(Merchandise.objects.all()))
        self.assertNotEqual(self.initial_merchandise_count, second_count)
        self.assertEqual(second_count, 2)

    def test_donation_is_created(self):
        """Test the number of donations has gone up by 1"""
        new_count = len(list(Donation.objects.all()))
        self.assertNotEqual(self.initial_donation_count, new_count)
        self.assertEqual(new_count, 1)

    def test_donation_content(self):
        """test donation has saved everything to database"""
        self.assertEqual(self.donation1.campaign, "help the donkeys")
        self.assertIn(self.giftaid_a.first_line_address, self.donation1.giftaid_detail.first_line_address)
        self.assertEqual(self.donation1.giftaid_detail.name, "Joe Bloggs")
        self.assertEqual(self.donation1.giftaid_detail.city, "Cardiff")
        self.assertEqual(self.donation1.giftaid_detail.postcode, "CF120UX")

    def test_counting_items_in_basket(self):
        """assess if donation, ticket and merchandise have been added to basket"""
        basket_collection = Basket(basket_id="TYR4567", paid=False, total_cost=0, date=datetime.now())
        basket_collection.save()
        basket_collection.ticket.add(self.couple_ticket)
        basket_collection.donation.add(self.donation1)
        basket_collection.merchandise.add(self.t_shirt)
        basket_collection.save()
        self.assertIn(self.couple_ticket, basket_collection.ticket)
        self.assertIn(self.donation1, basket_collection.donation)
        self.assertIn(self.t_shirt, basket_collection.merchandise)

    def test_check_total_cost_of_basket(self):
        """test if the calculated total cost method works"""
        basket_collection = Basket(basket_id="TYR4567", paid=False, total_cost=0)
        basket_collection.save()
        basket_collection.ticket.add(self.couple_ticket)
        basket_collection.donation.add(self.donation1)
        basket_collection.merchandise.add(self.t_shirt)
        basket_collection.save()
        total = basket_collection.get_total_cost()
        self.assertEqual(total, 44.8)





