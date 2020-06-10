from django.test import TestCase
from rest_framework.test import APIClient
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
        self.comms_grp = CommsGroup.objects.create(group_owner=self.person_a, group_name="fete group",
                                                   group_purpose="support summer fete")
        self.comms_grp.save()
        self.sunday_comms = CommsGroup.objects.create(group_owner=self.person_a, group_name="Sunday service",
                                                   group_purpose="comms to all for Sunday service")
        self.sunday_comms.save()
        self.sunday_comms.group_membership.add(self.rogue_employee)
        self.sunday_comms.save()
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
        self.event_a.invites.add(self.comms_grp)
        self.event_b.invites.add(self.sunday_comms)
        self.event_a.save()
        self.event_b.save()

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
        person_a_login = self.client.login(username=self.rogue_user, password='12345')
        response = self.client.get('/event/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context[0]['user']), self.rogue_user.username)
        processed_data = json.loads(json.dumps(response.context[0]['serializer']))
        #rogue employee is in invites for event_b, but not event_a
        for events in processed_data:
            if events == self.event_a:
                for grps in events['invites']:
                    query = CommsGroup.objects.get(group_name=grps.group_name)
                    for k,v in query.group_membership.values():
                        if k == 'userid_id':
                            self.assertNotEqual(v, self.rogue_user.id)
                            continue
            elif events == self.event_b:
                for grps in events['invites']:
                    query = CommsGroup.objects.get(group_name=grps.group_name)
                    for k,v in query.group_membership.values():
                        if k == 'userid_id':
                            self.assertEqual(v, self.rogue_user.id)

    def test_create_new_event(self):
        """test that it is possible to create a new event with an event owner who is then added to the associated
        invites group"""
        client = APIClient()
        client.login(username='emorse2', password='password')
        person = Person.objects.get(userid=self.user)
        pcc_comms = CommsGroup(group_name="pcc", group_purpose="pcc comms", group_owner=person)
        pcc_comms.save()
        data = {
            "title": "pcc meeting",
            "start": datetime.strptime("2020-07-03 12:00", "%Y-%m-%d %H:%M"),
            "end": datetime.strptime("2020-07-03 13:00", "%Y-%m-%d %H:%M"),
            "event_owner": person.id,
            "recurring": False,
            "description": "PCC meeting about matters of fabric",
            "website_publish": False,
            "invites": [pcc_comms.group_name]
        }
        request = client.post(reverse('event-list'), data, format='json')
        self.assertEqual(request.status_code, 201)
        query = Event.objects.get(title="pcc meeting")
        self.assertEqual(query.title, "pcc meeting")
        self.assertEqual(query.event_owner, person)

    def test_edit_event(self):
        """test that it is possible to edit an event"""
        client = APIClient()
        client.login(username='emorse2', password='password')
        data = {'slug': 'summer-fete'}
        response = client.get(reverse('event-detail', kwargs=data))
        self.assertEqual(response.status_code, 200)
        update_data = json.dumps({
            "title": "summer fete",
            "description": "Church money raiser of the year",
            "invites": [self.comms_grp.group_name]
        })
        update_response = client.post(reverse('event-detail', kwargs=data), data=update_data,
                                      content_type='application/json')
        self.assertEqual(update_response.status_code, 200)
        query_check = Event.objects.get(title="summer fete")
        self.assertEqual(query_check.description, "Church money raiser of the year")

    def test_edit_try_bad_data(self):
        """test to make sure cannot edit event with bad data"""
        client = APIClient()
        client.login(username='emorse2', password='password')
        data = {'slug': 'summer-fete'}
        bad_data = {
            'event_title': 'summer fayre'
        }
        bad_response = client.post(reverse('event-detail', kwargs=data), data=bad_data, content_type="application/json")
        self.assertEqual(bad_response.status_code, 400)

    def test_return_404_for_nonevent(self):
        """test that 404 is returned when slug specifies non-existent event"""
        client = APIClient()
        client.login(username='emorse2', password='password')
        data = {'slug': "prayer-grp"}
        response = client.get(reverse('event-detail', kwargs=data), format='json')
        self.assertEqual(response.status_code, 404)

    def test_delete_event(self):
        """test that an event can be deleted"""
        client = APIClient()
        client.login(username='emorse2', password='password')
        data = {'slug': 'summer-fete'}
        response = client.post(reverse('event-delete', kwargs=data), format='json')
        self.assertEqual(response.status_code, 302)
        query_check = Event.objects.filter(title="summer fete")
        self.assertEqual(list(query_check), [])


