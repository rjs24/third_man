from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from people.models import Role, Person
from comms.models import CommsGroup
from datetime import datetime
import json


class CommsGrpAPITest(TestCase):
    @classmethod
    def setUp(self):
        self.user = User(username='emorse2')
        self.user.set_password('password')
        self.user.save()
        self.user_b = User(username='jfrost3')
        self.user_b.set_password(('12345'))
        self.user_b.save()
        self.role_a = Role.objects.create(role_name="nearly all_things", role_responsibility="make nearly it all work")
        self.role_a.save()
        self.role_b = Role.objects.create(role_name="most_things", role_responsibility="try to get it to work")
        self.role_b.save()
        self.top_role = Role.objects.create(role_name="all_things", role_responsibility="make it all work")
        self.top_role.save()
        self.person_a = self.person_a = Person.objects.create(userid=self.user, email="joebloggs@email.com",
                                        first_name="joe", second_name="bloggs",
                                        date_of_birth=datetime.strptime("1985-06-21", "%Y-%m-%d"), postcode="S1 9AA",
                                        address= "29, Acacia Road, Nuttytown", organisation_role=self.role_a,
                                        allowed_access=3, notes="likes pizza", line_manage=self.top_role)
        self.person_a.save()
        self.person_b = Person.objects.create(userid=self.user_b, email="jackfrost@email.com", first_name="Jack",
                                        second_name="Frost", date_of_birth=datetime.strptime("1961-09-14", "%Y-%m-%d"),
                                        postcode="G1 0AA", address="4, Brutalistblock avenue", organisation_role=self.role_b,
                                        allowed_access=1, notes="likes rice", line_manage=self.top_role)
        self.person_b.save()

    def create_new_commsgrp_4_test(self):
        """Re-useable function to create new commsgroup in test db when needed by other tests."""
        client = APIClient()
        resp = client.post('/api/comms',
            data={"group_name":"Knitting", "group_owner": self.person_a.id, "group_purpose": "knitting and tea"},
            format='json')
        return resp

    def test_get_CommsGrps(self):
        """test listing of existing commsGroups via api"""
        self.create_new_commsgrp_4_test()
        client = APIClient()
        resp = client.get('/api/comms')
        self.assertEqual(resp.status_code, 200)
        comms_groups = CommsGroup.objects.all()
        proc_resp = json.loads(resp.content)
        self.assertEqual(proc_resp[0]['group_name'], comms_groups[0].group_name)

    def test_new_CommsGrp(self):
        """test creation of new commsGroup via api"""
        resp = self.create_new_commsgrp_4_test()
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(json.loads(resp.content), {"comms status": "comms group created"})

    def test_person_in_commsGrp_membership(self):
        """Test commsGroup 'Knitting' exists and can add person_b """
        self.create_new_commsgrp_4_test()
        dbq = CommsGroup.objects.all()[0]
        initial_count = dbq.group_membership.count()
        self.assertEqual(initial_count, 1)
        client = APIClient()
        update_data = {"group_name": "Knitting", "group_purpose": "knitting and tea", "group_owner": self.person_a.id,
                                      "group_membership": [self.person_a.id, self.person_b.id]}
        resp = client.put('/api/comms/knitting', data=update_data, format='json')
        self.assertEqual(resp.status_code, 200)
        dbq2 = CommsGroup.objects.all()[0]
        final_count = dbq2.group_membership.count()
        self.assertEqual(final_count, 2)

    def test_edit_group_title_in_commsGrp(self):
        """Test to see if possible to edit text via api"""
        self.create_new_commsgrp_4_test()
        client = APIClient()
        resp = client.put('/api/comms/knitting',
                          data={"group_name": "Knitting", "group_owner": self.person_a.id,
                                "group_purpose": "knitting, sowing and chat"}, format='json')
        self.assertEqual(resp.status_code, 200)
        edited_event = CommsGroup.objects.get(group_name="Knitting")
        self.assertEqual(edited_event.group_purpose, "knitting, sowing and chat")

    def test_delete_commsGrp(self):
        """Test if a commsGrp can be deleted via the api."""
        self.create_new_commsgrp_4_test()
        initial_count = len(list(CommsGroup.objects.all()))
        client = APIClient()
        resp = client.delete('/api/comms/knitting', format='json')
        self.assertEqual(resp.status_code, 204)
        all_comms = CommsGroup.objects.all()
        self.assertEqual(len(list(all_comms)), initial_count-1)
