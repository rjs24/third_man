from django.test import TestCase
from datetime import datetime, timedelta
from people.models import Person, Role
from comms.models import CommsGroup
from events.models import Event
from django.contrib.auth.models import User
from rest_framework.test import APIClient
import json


class EventAPITest(TestCase):

    @classmethod
    def setUp(self):
        self.user = User(username='emorse2')
        self.user.set_password('password')
        self.user.save()
        self.role = Role.objects.create(role_name="nearly all_things", role_responsibility="make it nearly all work")
        self.role.save()
        self.top_role = Role.objects.create(role_name="all_things", role_responsibility="make it all work")
        self.top_role.save()
        self.person_a = Person.objects.create(userid=self.user, email="joebloggs@email.com", first_name="joe",
                                        second_name="bloggs", date_of_birth=datetime.strptime("1985-06-21", "%Y-%m-%d"),
                                        postcode="S1 9AA", address= "29, Acacia Road, Nuttytown", organisation_role=self.role,
                                        allowed_access=3, notes="likes pizza", line_manage=self.top_role)
        self.person_a.save()
        self.comms_grp = CommsGroup.objects.create(group_name="fete group", group_purpose="support summer fete",
                                                   group_owner=self.person_a)
        self.comms_grp.save()
        self.event_a = Event.objects.create(title="summer fete",
                                            start=datetime.strptime("2020-07-03 12:00", "%Y-%m-%d %H:%M"),
                                            end=datetime.strptime("2020-07-03 16:00", "%Y-%m-%d %H:%M"),
                                            event_owner=self.person_a,
                                            duration=timedelta(hours=4),
                                            recurring=False, description="happy summer fete", website_publish=True)
        self.event_a.save()
        self.event_a.invites.add(self.comms_grp)
        self.event_a.save()

    def test_get_Events(self):
        """Test api to list events"""
        client = APIClient()
        client.login(username='emorse2', password='password')
        resp = client.get('/api/event')
        self.assertEqual(resp.status_code, 200)
        events = Event.objects.all()
        for event in events:
            self.assertEqual(event.title, resp.json()[0]['title'])

    def test_newEvent(self):
        """Test api to create new event"""
        client = APIClient()
        client.login(username='emorse2', password='password')
        resp = client.post('/api/event',
            {"event_owner": self.person_a.id, "title": "PCC",
            "start": datetime.strptime("2020-06-24 19:00", "%Y-%m-%d %H:%M"),
            "end": datetime.strptime("1985-06-21 21:00", "%Y-%m-%d %H:%M"), "duration": timedelta(hours=2),
            "invites": [self.comms_grp.group_name], "recurring": False, "description": "PCC meeting",
            "website_publish": False}, format='json')
        self.assertEqual(resp.status_code, 201)

    def test_editEvent(self):
        """Test api to edit an event"""
        client = APIClient()
        client.login(username='emorse2', password='password')
        resp = client.put('/api/event/summer-fete',
            data={"event_owner": self.person_a.id, "title": "summer fete",
            "start": datetime.strptime("2020-07-03 12:00", "%Y-%m-%d %H:%M"),
            "end": datetime.strptime("2020-07-03 16:00", "%Y-%m-%d %H:%M"), "duration": timedelta(hours=4),
            "invites": [self.comms_grp.group_name], "recurring": False, "description": "the main money raiser",
            "website_publish": False}, format='json')
        self.assertEqual(resp.status_code, 200)
        query = Event.objects.get(title="summer fete")
        self.assertEqual(query.description, "the main money raiser")

    def test_deleteEvent(self):
        """Test api to delete an event"""
        client = APIClient()
        client.login(username='emorse2', password='password')
        query1 = Event.objects.all()
        self.assertEqual(query1.count(), 1)
        resp = client.delete('/api/event/summer-fete', format='json')
        self.assertEqual(resp.status_code, 204)
        query2 = Event.objects.all()
        self.assertEqual(query2.count(), 0)


