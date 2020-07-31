from django.test import TestCase
from datetime import datetime, timedelta
from ..models import Donation, Ticket, Merchandise, Basket, Giftaid
from events.models import Event
from events.serializers import EventSerializer
from people.models import Person, Role
from django.contrib.auth.models import User
from rest_framework.test import APIClient
import json


class FinanceAPITest(TestCase):
    @classmethod
    def setUp(self):
        self.initial_count = len(list(Ticket.objects.all()))
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
        self.event_a = Event.objects.create(title="spring fete",
                                  start=datetime.strptime("2020-08-03 12:00", "%Y-%m-%d %H:%M"),
                                  end=datetime.strptime("2020-08-03 16:00", "%Y-%m-%d %H:%M"), event_owner=self.person_a,
                                  duration=timedelta(hours=4),
                                  recurring=False, description="happy spring fete", website_publish=True)
        self.person_a.save()
        self.event_a.save()

    def test_ticketsList(self):
        """Test api to list available tickets"""
        client = APIClient()
        resp = client.get('/api/ticket')
        self.assertEqual(resp.status_code, 200)
        tickets = Ticket.objects.all()
        self.assertEqual(json.loads(resp.content), json.loads(tickets))

    def test_ticketCreate(self):
        """test api to create a ticket based on the supplied event"""
        client = APIClient()
        resp = client.post('/api/ticket',
                           {"title": self.event_a.title, "event": EventSerializer(self.event_a), "price": 12.0,
                            "ticket_type": 1, "ticket_quantity": 2}, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.content), json.loads('{ "ticket status": "ticket created for event {}" }'
                                                              .format(self.event_a.title)))

    def test_ticketEdit(self):
        """ test api to edit a created ticket based on existing event"""
        client = APIClient()
        resp = client.put('/api/ticket',
                           {"search": {"title": "spring fete"}, "price": 10.0}, format='json'
                           )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.content), json.loads('{ "ticket status": "ticket price edited"'))

    def test_ticketDelete(self):
        """ test api to delete a created ticket based on existing event"""
        client = APIClient()
        resp = client.delete('/api/ticket',
                           {"search": {"title": "spring fete"}}, format='json'
                           )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.content), json.loads('{ "ticket status": "ticket deleted"'))

    def test_donationList(self):
        """Test api to list donations"""
        client = APIClient()
        resp = client.get('/api/donate')
        self.assertEqual(resp.status_code, 200)
        donations = Donation.objects.all()
        self.assertEqual(json.loads(resp.content), json.loads(donations))

    def test_donationCreate(self):
        """test api to create a donation"""
        client = APIClient()
        resp = client.post('/api/donation',
                           {"campaign": "save the donkeys", "target": 100000, "amount_2_donate": 12.0,
                            "giftaid": False, "donation_quantity": 1}, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.content), json.loads('{ "donation status": "donation created for campaign \
                                                                save the donkeys "}'))

    def test_donationEdit(self):
        """ test api to edit a created donationt"""
        client = APIClient()
        resp = client.put('/api/donation',
                           {"search": {"campaign": "help the donkeys"}, "amount_2_donate": 20.0}, format='json'
                           )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.content), json.loads('{ "donation status": "donation price edited"'))

    def test_donationDelete(self):
        """ test api to delete a created donation"""
        client = APIClient()
        resp = client.delete('/api/donate',
                           {"search": {"campaign": "help the donkeys"}}, format='json'
                           )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.content), json.loads('{ "donation status": "donation deleted"'))

    def test_listMerchandise(self):
        """Test to list all merchandise"""
        client = APIClient()
        resp = client.get('/api/merchandise')
        self.assertEqual(resp.status_code, 200)
        merchandise = Merchandise.objects.all()
        self.assertEqual(json.loads(resp.content), json.loads(merchandise))

    def test_merchandiseCreate(self):
        """test api to create a merchandise object"""
        client = APIClient()
        resp = client.post('/api/merchandise/create',
                           {"merchandise_name": "branded mug", "stock_number": "DFR56793", "price": 5.3,
                            "merchandise_description": "mug with logo", "merchandise_quantity": 2}, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.content), json.loads('{ "merchandise status": "merchandise created for \
                                                            description mug with logo "}'))

    def test_merchandiseEdit(self):
        """ test api to edit a created donationt"""
        client = APIClient()
        resp = client.put('/api/merchandise/edit',
                           {"search": {"merchandise_name": "branded mug"}, "amount_2_donate": 20.0}, format='json'
                           )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.content), json.loads('{ "merchandise status": "donation price edited"'))

    def test_merchandiseDelete(self):
        """ test api to delete a created donation"""
        client = APIClient()
        resp = client.delete('/api/merchandise/delete',
                           {"search": {"merchandise_name": "branded mug"}}, format='json'
                           )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.content), json.loads('{ "merchandise status": "merchandise deleted"'))





