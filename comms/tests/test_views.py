from people.models import Person, Role
from rest_framework.test import APIClient
from ..models import CommsGroup
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from datetime import datetime
import json


class CommsGrpViewTest(TestCase):
    @classmethod
    def setUp(self):
        self.user = User(username='emorse2')
        self.user.set_password('password')
        self.user.save()
        self.user_b = User(username='jfrost3')
        self.user_b.set_password(('12345'))
        self.user_b.save()
        self.role_a = Role.objects.create(role_name="all_things", role_responsibility="make it all work")
        self.role_a.save()
        self.role_b = Role.objects.create(role_name="most_things", role_responsibility="try to get it to work")
        self.role_b.save()
        self.top_role = Role.objects.create(role_name="director", role_responsibility="shareholders")
        self.top_role.save()
        self.person_a = Person.objects.create(userid=self.user, email="joebloggs@email.com", first_name="joe",
                                        second_name="bloggs", date_of_birth=datetime.strptime("1985-06-21", "%Y-%m-%d"),
                                        postcode="S1 9AA", address= "29, Acacia Road, Nuttytown",
                                        organisation_role=self.role_a, allowed_access=3, notes="likes pizza",
                                        line_manage=self.top_role)
        self.person_a.save()
        self.person_b = Person.objects.create(userid=self.user_b, email="jackfrost@email.com", first_name="Jack",
                                        second_name="Frost", date_of_birth=datetime.strptime("1961-09-14", "%Y-%m-%d"),
                                        postcode="G1 0AA", address="4, Brutalistblock avenue", organisation_role=self.role_b,
                                        allowed_access=1, notes="likes rice", line_manage=self.top_role)
        self.person_b.save()
        self.comms_grp = CommsGroup.objects.create(group_name="pcc", group_purpose="church fabric and stuff",
                                                   group_owner=self.person_b)
        self.comms_grp.save()
        self.comms_grp.group_membership.add(self.person_a)

    def test_url_exists(self):
        """test response from url"""
        self.client.force_login(User.objects.get_or_create(username='emorse2')[0])
        response = self.client.get('/comms/')
        self.assertEqual(response.status_code, 200)

    def test_url_by_name(self):
        """test endpoint through reverse"""
        self.client.force_login(User.objects.get_or_create(username='emorse2')[0])
        response = self.client.get(reverse('comms-list'))
        self.assertEqual(response.status_code, 200)

    def test_create_new_comms_grp(self):
        """test that is is possible to create a comms_grp and check group_owner is added to group_membership"""
        client = APIClient()
        client.login(username='emorse2', password='password')
        person = Person.objects.get(first_name='joe')
        data = {
            'group_name': 'summer fete',
            'group_owner': person.id,
            'group_purpose': 'organize summer fete'
        }
        response = client.post(reverse('comms-list'), data, format='json')
        self.assertEqual(response.status_code, 201)
        response_list = client.get(reverse('comms-list'))
        self.assertEqual(response_list.status_code, 200)
        item = CommsGroup.objects.get(group_name='summer fete')
        self.assertEqual(item.group_purpose, 'organize summer fete')
        self.assertTrue(item.group_membership.values()[0]['id'])

    def test_edit_comms_grp(self):
        """test that it is possible to edit a comms group"""
        client = APIClient()
        client.login(username='emorse2', password='password')
        data = {'slug':'pcc'}
        response = client.get(reverse('comms-detail', kwargs=data))
        comms_grp = CommsGroup.objects.filter(group_name='pcc')
        self.assertEqual(list(response.data['queryset']), list(comms_grp))
        self.assertEqual(response.status_code, 200)
        update_data = json.dumps({'group_name': 'pcc', 'group_purpose': 'looking after vicar', 'group_owner': self.person_a.id})
        update_response = client.post(reverse('comms-detail', kwargs=data), data=update_data, content_type='application/json')
        self.assertEqual(update_response.status_code, 200)
        query_check = CommsGroup.objects.filter(group_name='pcc')
        self.assertEqual(query_check.values()[0]['group_purpose'], 'looking after vicar')

    def test_edit_try_bad_data(self):
        """test to make sure edit cannot take place with bad data"""
        client = APIClient()
        client.login(username='emorse2', password='password')
        data = {'slug': 'pcc'}
        bad_data = json.dumps(
            {'group_name': 'flowers'})
        bad_response = client.post(reverse('comms-detail', kwargs=data), data=bad_data,
                                      content_type='application/json')
        self.assertEqual(bad_response.status_code, 400)

    def test_return_404_for_non_grp(self):
        """Test that a non-existent group return 404"""
        client = APIClient()
        client.login(username='emorse2', password='password')
        data = {'slug': 'choir'}
        response = client.get(reverse('comms-detail', kwargs=data))
        self.assertEqual(response.status_code, 404)

    def test_delete_comms_grp(self):
        """test if it is possible to delete a comms group"""
        client = APIClient()
        client.login(username='emorse2', password='password')
        data = {'slug': 'pcc'}
        response = client.post(reverse('comms-delete', kwargs=data), format='json')
        self.assertEqual(response.status_code, 302) # for redirect to comms homepage
        query_check = CommsGroup.objects.filter(group_name='pcc')
        self.assertEqual(list(query_check), [])

    '''
    def test_user_can_only_see_comms_groups_they_are_in(self):
        """Write a test to ensure a user can only see comms_groups they belong to as a user"""
        auth_response = self.client.post(reverse('login'),
                                         {'username': self.user,
                                          'password': 'password'})
        self.assertEqual(auth_response.status_code, 200)
        self.assertIn('__auth_user_id', self.client.session)
        comms_q_initiial_length = self.comms_grp.all()
        self.assertEqual(comms_q_initiial_length, 0)
        self.comms_grp.add(self.user_a)
        self.assertIn(self.user_a, self.comms_grp)
        self.assertNotIn(self.user_b, self.comms_grp)
        '''






