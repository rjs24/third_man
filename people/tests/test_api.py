from django.test import TestCase
from rest_framework.test import APIClient
import json
from ..models import Person, Role, Staff, Volunteer
from django.contrib.auth.models import User


class PeopleAPITest(TestCase):
    @classmethod
    def setUp(self):
        self.user_director = User(username='joebl1')
        self.user_director.save()
        self.role_director = Role.objects.create(role_name="Director", role_responsibility="Everything")
        self.role_director.save()
        self.role_employee = Role.objects.create(role_name="all_things", role_responsibility="make it all work")
        self.role_employee.save()
        self.top_role = Role.objects.create(role_name="everything", role_responsibility="make it nearly all work")
        self.top_role.save()
        self.user_employee_a = User(username='emorse2')
        self.user_employee_a.save()
        self.user_employee_b = User(username='jfrost4')
        self.user_employee_b.save()
        self.employee_a = Person.objects.create(userid=self.user_employee_a, email="endeavourmorse@email.com", first_name="Endeavour",
                                              second_name="Morse", date_of_birth="1985-06-21", postcode="B1 0AA",
                                              address="2, Old Street, Newtown", organisation_role=self.role_employee,
                                              allowed_access=3, notes="likes curries", line_manage=self.role_director)
        self.employee_a.save()
        self.employee_b = Person.objects.create(userid=self.user_employee_b, email="jackfrost@email.com", first_name="Jack",
                                              second_name="Frost", date_of_birth="1961-09-14", postcode="G1 0AA",
                                              address="4, Brutalistblock avenue", organisation_role=self.role_employee,
                                              allowed_access=3, notes="likes pasta", line_manage=self.top_role)
        self.employee_b.save()

    def test_listRole(self):
        """Test api to list all roles"""
        client = APIClient()
        resp = client.get('/api/role')
        self.assertEqual(resp.status_code, 200)
        roles = Role.objects.all()
        self.assertEqual(json.loads(resp.content), json.loads(roles))

    def test_createRole(self):
        """test api to create a role"""
        client = APIClient()
        resp = client.post('/api/role',
                           {"role_name": "manager", "role_responsibility": "mostly everything"}, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.content), json.loads('{ "role_status": "role created" }'))

    def test_editRole(self):
        """test api to edit role"""
        client = APIClient()
        resp = client.put('/api/role',
                           {"search": {"role_name": "manager"}, "role_name": "Director",}, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.content), json.loads('{ "role_status": "role edited" }'))

    def test_deleteRole(self):
        """test api to delete role"""
        client = APIClient()
        resp = client.delete('/api/role',
                           {"search": {"role_name": "manager"}}, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.content), json.loads('{ "role_status": "role deleted" }'))

    def test_listPerson(self):
        """Test api to list all person"""
        client = APIClient()
        resp = client.get('/api/person')
        self.assertEqual(resp.status_code, 200)
        people = Person.objects.all()
        self.assertEqual(json.loads(resp.content), json.loads(people))

    def test_createPerson(self):
        """test api to create a person"""
        client = APIClient()
        resp = client.post('/api/person',
                           {"userid": self.user_director, "email": "joebloggs@email.com", "first_name": "Joe",
                            "second_name": "Bloggs", "date_of_birth": "1985-06-21", "postcode": "S1 9AA",
                            "address": "29, Acacia Road, Nuttytown", "organisation_role": self.role_director,
                            "allowed_access": 3, "notes": "likes pizza", "line_manage": None }, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.content), json.loads('{ "person_status": "person created" }'))


    def test_editPerson(self):
        """test api to edit person"""
        client = APIClient()
        resp = client.put('/api/person',
                           {"search": {"userid": self.user_director}, "notes": "Actually prefers curry"}, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.content), json.loads('{ "person_status": "person edited" }'))

    def test_deletePerson(self):
        """test api to delete person"""
        client = APIClient()
        resp = client.delete('/api/role',
                           {"search": {"userid": self.user_director}}, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.content), json.loads('{ "person_status": "person deleted" }'))

    def test_listStaff(self):
        """Test api to list all staff"""
        client = APIClient()
        resp = client.get('/api/person')
        self.assertEqual(resp.status_code, 200)
        staff = Staff.objects.all()
        self.assertEqual(json.loads(resp.content), json.loads(staff))

    def test_createStaff(self):
        """test api to create a staff"""
        client = APIClient()
        resp = client.post('/api/person',
                           {"person": self.employee_a, "staff_number": "DF548", "nat_insurance_num": "DF000000A",
                            "salary": 23475}, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.content), json.loads('{ "person_status": "person created" }'))


    def test_editStaff(self):
        """test api to edit staff"""
        client = APIClient()
        resp = client.put('/api/staff',
                           {"search": {"person": self.employee_a.userid}, "staff_number": "XL456"}, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.content), json.loads('{ "person_status": "person edited" }'))

    def test_deleteStaff(self):
        """test api to delete staff"""
        client = APIClient()
        resp = client.delete('/api/staff',
                           {"search": {"person": self.user_director}}, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.content), json.loads('{ "staff_status": "staff deleted" }'))

    def test_listVolunteer(self):
        """Test api to list all volunteer"""
        client = APIClient()
        resp = client.get('/api/volunteer')
        self.assertEqual(resp.status_code, 200)
        volunteers = Volunteer.objects.all()
        self.assertEqual(json.loads(resp.content), json.loads(volunteers))

    def test_createVolunteer(self):
        """test api to create a volunteer"""
        client = APIClient()
        resp = client.post('/api/volunteer',
                           {"person": self.employee_a, "staff_number": "DF550"}, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.content), json.loads('{ "volunteer_status": "volunteer created" }'))

    def test_editVolunteer(self):
        """test api to edit volunteer"""
        client = APIClient()
        resp = client.put('/api/volunteer',
                          {"search": {"person": self.employee_b.userid}, "staff_number": "XL456"}, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.content), json.loads('{ "volunteer_status": "volunteer edited" }'))

    def test_deleteVolunteer(self):
        """test api to delete volunteer"""
        client = APIClient()
        resp = client.delete('/api/volunteer',
                             {"search": {"person": self.employee_b.userid}}, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.content), json.loads('{ "volunteer_status": "volunteer deleted" }'))