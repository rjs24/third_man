from django.test import TestCase
from django.urls import reverse
from ..models import Event
from people.models import Person, Role
from comms.models import CommsGroup
from django.contrib.auth.models import User
from datetime import datetime, timedelta

class EventViewTest(TestCase):
    @classmethod
    def setUp(self):
        self.user = User(username='emorse2')
        self.user.set_password('password')
        self.user.save()
        self.rogue_user = User(username='jfrost3')
        self.rogue_user.set_password(('12345'))
        self.rogue_user.save()
        self.role = Role.objects.create(role_name="nearly all_things", role_responsibility="make nearly it all work")
        self.role.save()
        self.top_role = Role.objects.create(role_name="all_things", role_responsibility="make it all work")
        self.top_role.save()
        self.person_a = Person.objects.create(userid=self.user, email="joebloggs@email.com", first_name="joe",
                                        second_name="bloggs", date_of_birth=datetime.strptime("1985-06-21", "%Y-%m-%d"),
                                        postcode="S1 9AA", address= "29, Acacia Road, Nuttytown",
                                        organisation_role=self.role, allowed_access=3, notes="likes pizza",
                                        line_manage=self.top_role)
        self.person_a.save()
        self.rogue_employee = Person.objects.create(userid=self.rogue_user, email="jackfrost@email.com", first_name="Jack",
                                        second_name="Frost", date_of_birth=datetime.strptime("1961-09-14", "%Y-%m-%d"),
                                        postcode="G1 0AA", address="4, Brutalistblock avenue", organisation_role=self.role,
                                        allowed_access=1, notes="likes rice", line_manage=self.top_role)
        self.rogue_employee.save()
        self.comms_grp = CommsGroup.objects.create(group_name="fete group", group_purpose="support summer fete")
        self.comms_grp.save()
        self.comms_grp.group_membership.add(self.rogue_employee)
        self.event_a = Event.objects.create(title="summer fete",
                                  start=datetime.strptime("2020-07-03 12:00", "%Y-%m-%d %H:%M"),
                                  end=datetime.strptime("2020-07-03 16:00", "%Y-%m-%d %H:%M"), event_owner=self.person_a,
                                  duration=timedelta(hours=4),
                                  recurring=False, description="happy summer fete", website_publish=True)
        self.event_b = Event.objects.create(title="sunday service",
                                  start=datetime.strptime("2020-03-08 10:00", "%Y-%m-%d %H:%M"),
                                  end=datetime.strptime("2020-03-08 11:00","%Y-%m-%d %H:%M"), event_owner=self.person_a,
                                  duration=timedelta(hours=1),
                                  recurring=True, description="regular Sunday 10 am service", website_publish=False)

        self.event_a.save()
        self.event_b.save()
        self.event_b.invites.add(self.comms_grp)

    def test_url_exists(self):
        """test response from url"""
        response = self.client.get('/events')
        self.assertEqual(response.status_code, 200)

    def test_url_by_name(self):
        """test endpoint through reverse"""
        response = self.client.get(reverse('events'))
        self.assertEqual(response.status_code, 200)

    def test_event_customised_visibility_for_rogue_employee(self):
        """A user should only be able to see events that they are the event_owner for or are in the invites group"""
        person_a_login = self.client.login(username=self.rogue_user, password='12345')
        response = self.client.get(reverse('events'))
        self.assertEqual(str(response.context['user']). self.rogue_user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(isinstance(response.context['events']['invites'], CommsGroup))
        self.assertIn(self.rogue_employee, response.context['events']['invites']['group_membership'])




