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
        self.comms_grp = CommsGroup.objects.create(group_name="fete group", group_purpose="support summer fete")
        self.comms_grp.save()

    def test_get_Events(self):
        """Test api to list events"""
        client = APIClient()
        resp = client.put('/api/event')
        self.assertEqual(resp.status_code, 200)
        events = Event.objects.all()
        self.assertEqual(json.loads(resp.content), json.loads(events))

    def test_newEvent(self):
        """Test api to create new event"""
        client = APIClient()
        resp = client.post('/api/event',
            {"event_owner": '{}', "title": "PCC", "start": datetime.strptime("2020-06-24 19:00", "%Y-%m-%d %H:%M"),
              "end":datetime.strptime("1985-06-21 21:00", "%Y-%m-%d %H:%M"), "duration": timedelta(hours=2),
            "invites": self.comms_grp, "recurring": False, "description": "PCC meeting",
        "website_publish": False}, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.content), json.loads('{ "event status": "event created", "title": "PCC", '
                                                   '"start": {}, "user", {} }'.format(
            datetime.strptime("2020-06-24 19:00", "%Y-%m-%d %H:%M"), self.user)))

    def test_editEvent(self):
        """Test api to edit an event"""
        client = APIClient()
        resp = client.put('/api/event',
            { "search": {"title": "PCC meeting"}, "start": datetime.strptime("2020-06-24 20:00", "%Y-%m-%d %H:%M"),
            "end": datetime.strptime("1985-06-21 22:00", "%Y-%m-%d %H:%M")}, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.content), json.loads('{ "event status": "event edit complete", "event_title": title,'
                                                   '"user", userid }'))

    def test_deleteEvent(self):
        """Test api to delete an event"""
        client = APIClient()
        resp = client.put('/api/event',
            { "search": {"title": "PCC meeting"}}, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.content), json.loads('{ "event status": "event delete complete"}'))
