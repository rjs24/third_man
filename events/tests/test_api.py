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
        self.comms_grp = CommsGroup.objects.create(group_owner=self.person_a,
                                                   group_name="fete group", group_purpose="support summer fete")
        self.comms_grp.save()

    def test_get_Events(self):
        """Test api to list events"""
        event_a = Event.objects.create(title="christmas party",
                                            start=datetime.strptime("2020-12-03 12:00", "%Y-%m-%d %H:%M"),
                                            end=datetime.strptime("2020-12-03 16:00", "%Y-%m-%d %H:%M"),
                                            event_owner=self.person_a,
                                            duration=timedelta(hours=4),
                                            recurrence_interval=0, description="happy christmas party", website_publish=True)
        event_a.invites.add(self.comms_grp)
        event_a.save()
        event_b = Event.objects.create(title="Spring clean",
                                            start=datetime.strptime("2020-04-03 09:00", "%Y-%m-%d %H:%M"),
                                            end=datetime.strptime("2020-04-03 16:00", "%Y-%m-%d %H:%M"),
                                            event_owner=self.person_a,
                                            duration=timedelta(hours=7),
                                            recurrence_interval=0, description="get the church clean", website_publish=True)
        event_b.invites.add(self.comms_grp)
        event_b.save()
        client = APIClient()
        resp = client.get('/api/events')
        self.assertEqual(resp.status_code, 200)
        events = Event.objects.all()
        self.assertEqual(events[0].title, json.loads(resp.content)[1]['title'])
        self.assertEqual(events[1].title, json.loads(resp.content)[0]['title'])

    def test_newEvent(self):
        """Test api to create new event"""
        client = APIClient()
        data = {"event_owner": self.person_a.id, "title": "PCC",
                "start": datetime.strptime("2020-06-24 19:00", "%Y-%m-%d %H:%M"),
                "end": datetime.strptime("1985-06-21 21:00", "%Y-%m-%d %H:%M"), "duration": timedelta(hours=2),
                "recurrence_interval": 3, "invites": [self.comms_grp.group_name], "description": "PCC meeting",
                "website_publish": False}
        resp = client.post('/api/events', data=data, format='json')
        self.assertEqual(resp.status_code, 201)
        query = Event.objects.get(title="PCC")
        self.assertEqual(data['title'], query.title)

    def test_editEvent(self):
        """Test api to edit an event"""
        event_a = Event.objects.create(title="Christmas meal",
                                            start=datetime.strptime("2020-12-03 12:00", "%Y-%m-%d %H:%M"),
                                            end=datetime.strptime("2020-12-03 16:00", "%Y-%m-%d %H:%M"),
                                            event_owner=self.person_a,
                                            duration=timedelta(hours=4),
                                            recurrence_interval=0, description="happy christmas party", website_publish=True)
        event_a.invites.add(self.comms_grp)
        event_a.save()
        client = APIClient()
        update_data = {"event_owner": self.person_a.pk, "title": "Christmas meal", "start":
            datetime.strptime("2020-12-07 12:00", "%Y-%m-%d %H:%M"),
            "end": datetime.strptime("2020-12-07 16:00", "%Y-%m-%d %H:%M"), "duration": timedelta(hours=4),
                "invites": [self.comms_grp.pk], "recurrence_interval": 0, "description": "Christmas party yahoo",
                       "website_publish": False}
        resp = client.put('/api/events/christmas-meal', data=update_data, format='json')
        self.assertEqual(resp.status_code, 200)
        event_check = Event.objects.get(title="Christmas meal")
        self.assertEqual(event_check.description, "Christmas party yahoo")

    def test_deleteEvent(self):
        """Test api to delete an event"""
        event_a = Event.objects.create(title="christmas party",
                                            start=datetime.strptime("2020-12-03 12:00", "%Y-%m-%d %H:%M"),
                                            end=datetime.strptime("2020-12-03 16:00", "%Y-%m-%d %H:%M"),
                                            event_owner=self.person_a,
                                            duration=timedelta(hours=4),
                                            recurrence_interval=0, description="happy christmas party", website_publish=True)
        event_a.invites.add(self.comms_grp)
        event_a.save()
        client = APIClient()
        resp = client.delete('/api/events/christmas-party',
            { "search": {"title": "christmas party"}}, format='json')
        self.assertEqual(resp.status_code, 204)
