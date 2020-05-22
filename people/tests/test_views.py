from django.test import TestCase
from django.urls import reverse
from people.models import Role
from django.contrib.auth.models import User
from datetime import datetime, timedelta


class PeopleViewTest(TestCase):
    @classmethod
    def setUp(self):
        self.user = User(username='emorse2')
        self.user.set_password('password')
        self.user.save()
        self.role = Role.objects.create(role_name="Director", role_responsibility="make nearly it all work")
        self.role.save()

    def test_url_exists(self):
        """test response from url"""
        response = self.client.get('/people')
        self.assertEqual(response.status_code, 200)

    def test_url_by_name(self):
        """test endpoint through reverse"""
        response = self.client.get(reverse('people'))
        self.assertEqual(response.status_code, 200)

    def test_event_customised_visibility_for_rogue_employee(self):
        """A user should only be able to see events that they are the event_owner for or are in the invites group"""
        person_a_login = self.client.login(username=self.user, password='12345')
        response = self.client.get(reverse('roles'))
        self.assertEqual(str(response.context['user']). self.user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(isinstance(response.context['roles']['role_name'], Role))
        self.assertEqual(response.context['roles']['role_name'], "Director")