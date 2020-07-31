from django.test import TestCase
from django.urls import reverse
from ..models import Event
from people.models import Person, Role
from comms.models import CommsGroup
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import json


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
        self.comms_grp = CommsGroup.objects.create(group_owner=self.person_a,
                                                   group_name="fete group", group_purpose="support summer fete")
        self.comms_grp.save()
        self.comms_grp.group_membership.add(self.rogue_employee)
        self.select_comms_group = CommsGroup.objects.create(group_owner=self.person_a,
                                                            group_name="selected only", group_purpose="special stuff")
        self.select_comms_group.save()
        self.event_a = Event.objects.create(title="summer fete",
                                  start=datetime.strptime("2020-07-03 12:00", "%Y-%m-%d %H:%M"),
                                  end=datetime.strptime("2020-07-03 16:00", "%Y-%m-%d %H:%M"), event_owner=self.person_a,
                                  duration=timedelta(hours=4), recurrence_interval=0,
                                description="happy summer fete", website_publish=True)
        self.event_b = Event.objects.create(title="sunday service",
                                  start=datetime.strptime("2020-03-08 10:00", "%Y-%m-%d %H:%M"),
                                  end=datetime.strptime("2020-03-08 11:00","%Y-%m-%d %H:%M"), event_owner=self.person_a,
                                  duration=timedelta(hours=1),
                                  recurrence_interval=2, description="regular Sunday 10 am service", website_publish=False)

        self.event_a.save()
        self.event_b.save()
        self.event_b.invites.add(self.comms_grp)
        self.event_b.save()
        self.event_a.invites.add(self.select_comms_group)
        self.event_a.save()

    def test_url_exists(self):
        """test response from url"""
        self.client.force_login(User.objects.get_or_create(username='emorse2')[0])
        response = self.client.get('/event/')
        self.assertEqual(response.status_code, 200)

    def test_url_by_name(self):
        """test endpoint through reverse"""
        self.client.force_login(User.objects.get_or_create(username='emorse2')[0])
        response = self.client.get(reverse('event-list'))
        self.assertEqual(response.status_code, 200)

    def test_event_customised_visibility_for_rogue_employee(self):
        """A user should only be able to see events that they are the event_owner for or are in the invites group"""
        self.client.login(username=self.rogue_user, password='12345')
        response = self.client.get(reverse('event-list'))
        self.assertEqual(str(response.context['user']), self.rogue_user.username)
        self.assertEqual(response.status_code, 200)
        for querys in response.context['queryset']:
            self.assertNotEqual(querys.title, "summer fete")
            self.assertEqual(querys.title, "sunday service")
            for attribs in querys.invites.values():
                self.assertNotEqual(attribs['group_name'], "selected only")





