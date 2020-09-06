from django.test import TestCase
from rest_framework.test import APIClient
import json
from ..models import Person, Role, Staff, Volunteer, Working_Hrs
from django.contrib.auth.models import User
from datetime import datetime


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
        self.user_employee_c = User(username='rlewis3')
        self.user_employee_c.save()
        self.employee_a = Person.objects.create(userid=self.user_employee_a, email="endeavourmorse@email.com",
                                            first_name="Endeavour", second_name="Morse",
                                            date_of_birth=datetime.strptime("2020-06-21", "%Y-%m-%d"), postcode="B1 0AA",
                                            address="2, Old Street, Newtown", organisation_role=self.role_employee,
                                            allowed_access=3, notes="likes curries", line_manage=self.role_director)
        self.employee_a.save()
        self.employee_b = Person.objects.create(userid=self.user_employee_b, email="jackfrost@email.com", first_name="Jack",
                                              second_name="Frost", date_of_birth="1961-09-14", postcode="G1 0AA",
                                              address="4, Brutalistblock avenue", organisation_role=self.role_employee,
                                              allowed_access=3, notes="likes pasta", line_manage=self.top_role)
        self.employee_b.save()
        self.working_hrs_a = Working_Hrs.objects.create(shift_name="Weds", day_of_week=3, start="08:00:00",
                                                        end="17:00:00", duration="9:00:00")
        self.working_hrs_a.save()
        self.working_hrs_b = Working_Hrs.objects.create(shift_name="Friday", day_of_week=5, start="08:00:00",
                                                        end="17:00:00", duration="9:00:00")
        self.working_hrs_b.save()
        self.staff_a = Staff.objects.create(person=self.employee_a, staff_number="DF548", nat_insurance_num="DF000000A",
                                            salary=23475)
        self.staff_a.save()
        self.staff_a.hours.add(self.working_hrs_a.id)
        self.staff_a.save()
        self.volunteer_b = Volunteer.objects.create(person=self.employee_b, staff_number="DF549")
        self.volunteer_b.save()

    def test_listRole(self):
        """Test api to list all roles"""
        client = APIClient()
        resp = client.get('/api/people/roles')
        self.assertEqual(resp.status_code, 200)
        roles = Role.objects.get(role_name='all_things')
        self.assertEqual(json.loads(resp.content)[0]['role_name'], roles.role_name)

    def test_createRole(self):
        """test api to create a role"""
        client = APIClient()
        resp = client.post('/api/people/roles',
                           {"role_name": "manager", "role_responsibility": "mostly everything"}, format='json')
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(json.loads(resp.content), json.loads('{ "Role status": "New role created" }'))

    def test_editRole(self):
        """test api to edit role"""
        test_role = Role.objects.create(role_name="manager", role_responsibility="make it nearly all work")
        test_role.save()
        client = APIClient()
        update_data = {"role_name": "manager", "role_responsibility": "everything"}
        resp = client.put('/api/people/roles/manager', data=update_data, format='json')
        self.assertEqual(resp.status_code, 200)

    def test_deleteRole(self):
        """test api to delete role"""
        client = APIClient()
        Role.objects.create(role_name="useless", role_responsibility="never works")
        resp = client.delete('/api/people/roles/useless', format='json')
        self.assertEqual(resp.status_code, 204)
        test_query = Role.objects.filter(role_name='useless')
        self.assertEqual(list(test_query), [])

    def test_listPerson(self):
        """Test api to list all person"""
        client = APIClient()
        resp = client.get('/api/people/person')
        self.assertEqual(resp.status_code, 200)
        people = Person.objects.values()
        db_query = list(people)
        resp_content = json.loads(resp.content)
        self.assertEqual(len(db_query), len(resp_content))

    def test_createPerson(self):
        """test api to create a person"""
        client = APIClient()
        resp = client.post('/api/people/person',
                           {"userid": self.user_director.id, "email": "joebloggs@email.com", "first_name": "Joe",
                            "second_name": "Bloggs", "date_of_birth": datetime.strptime("1984-11-12", "%Y-%m-%d"),
                            "postcode": "S19AA", "address": "29, Acacia Road, Nuttytown",
                            "organisation_role": self.role_director.role_name, "phone_number": "00001111111",
                            "allowed_access": 3, "notes": "likes pizza", "line_manage": self.top_role.role_name},
                           format='json')
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(json.loads(resp.content), json.loads('{ "Person status": "person created" }'))

    def test_editPerson(self):
        """test api to edit person"""
        client = APIClient()
        update_data = {"userid": self.user_director.id, "email": "endeavourmorse@email.com", "first_name": "Endeavour",
                    "second_name": "Morse", "date_of_birth": datetime.strptime("2020-06-21", "%Y-%m-%d"),
                    "postcode": "B23BB", "address": "90, New Street, Oldtown", "organisation_role": self.role_employee.pk,
                    "phone_number": "00001111111", "allowed_access": 2, "notes": "likes pizza", "line_manage": self.role_director.pk}
        resp = client.put('/api/people/person/emorse2', data=update_data, format='json')
        self.assertEqual(resp.status_code, 200)
        test_person = Person.objects.get(second_name="Morse")
        self.assertNotEqual(test_person.postcode, "B1 0AA")
        self.assertNotEqual(test_person.address, "2, Old Street, Newtown")
        self.assertNotEqual(test_person.notes, "likes curries")
        self.assertEqual(test_person.postcode, "B23BB")
        self.assertEqual(test_person.address, "90, New Street, Oldtown")
        self.assertEqual(test_person.notes, "likes pizza")

    def test_deletePerson(self):
        """test api to delete person"""
        client = APIClient()
        test_person = Person.objects.create(userid=self.user_employee_c, email="rlewis3@email.com", first_name="Robby",
                              second_name="Lewis", date_of_birth="1955-07-16", postcode="M1 1BB",
                              address="79, Victorian close", organisation_role=self.role_employee,
                              allowed_access=1, notes="likes ice cream", line_manage=self.top_role)
        test_person.save()
        id = test_person.userid
        url_str = '/api/people/person/{}'.format(str(id))
        resp2 = client.delete(url_str, format='json')
        self.assertEqual(resp2.status_code, 204)
        test_query = list(Person.objects.filter(userid=test_person.userid))
        self.assertEqual(test_query, [])

    def test_listStaff(self):
        """Test api to list all staff"""
        client = APIClient()
        resp = client.get('/api/people/staff')
        self.assertEqual(resp.status_code, 200)
        staff = list(Staff.objects.all())
        resp_content = json.loads(resp.content)
        self.assertEqual(len(staff), len(resp_content))

    def test_createStaff(self):
        """test api to create a staff"""
        client = APIClient()
        resp = client.post('/api/people/staff',
                           {"person": self.employee_a.id, "staff_number": "DF549", "nat_insurance_num": "DF000000A",
                            "salary": 23475, "hours": [self.working_hrs_b.id]}, format='json')
        self.assertEqual(resp.status_code, 201)

    def test_editStaff(self):
        """test api to edit staff"""
        client = APIClient()
        update_data = {"person": self.employee_a.id, "staff_number": "DF548", "nat_insurance_num": "HJ111111B",
                            "salary": 31000, "hours": [self.working_hrs_b.id]}
        resp = client.put('/api/people/staff/df548', data=update_data, format='json')
        self.assertEqual(resp.status_code, 200)
        test_staff = Staff.objects.get(staff_number="DF548")
        self.assertEqual(test_staff.salary, 31000)
        self.assertEqual(test_staff.nat_insurance_num, "HJ111111B")

    def test_deleteStaff(self):
        """test api to delete staff"""
        client = APIClient()
        resp = client.delete('/api/people/staff/df548', format='json')
        self.assertEqual(resp.status_code, 204)
        test_staff = list(Staff.objects.filter(staff_number="DF548"))
        self.assertEqual(test_staff, [])

    def test_listVolunteer(self):
        """Test api to list all volunteer"""
        client = APIClient()
        resp = client.get('/api/people/volunteer')
        self.assertEqual(resp.status_code, 200)
        volunteers = list(Volunteer.objects.all())
        self.assertEqual(len(json.loads(resp.content)), len(volunteers))

    def test_createVolunteer(self):
        """test api to create a volunteer"""
        client = APIClient()
        resp = client.post('/api/people/volunteer',
                           data={"person": self.employee_b.id, "staff_number": "DF550", "hours": [self.working_hrs_b.id]
                                 }, format='json')
        self.assertEqual(resp.status_code, 201)

    def test_editVolunteer(self):
        """test api to edit volunteer"""
        client = APIClient()
        resp = client.put('/api/people/volunteer/df549',
                          data={"person": self.employee_b.id, "staff_number": "XL5", "hours": [self.working_hrs_b.id]
                                }, format='json')
        self.assertEqual(resp.status_code, 200)
        test_volunteer = Volunteer.objects.get(staff_number="XL5")
        self.assertNotEqual(test_volunteer, [])
        self.assertEqual(test_volunteer.staff_number, "XL5")

    def test_deleteVolunteer(self):
        """test api to delete volunteer"""
        client = APIClient()
        resp = client.delete('/api/people/volunteer/df549', format='json')
        self.assertEqual(resp.status_code, 204)
        test_volunteer = list(Volunteer.objects.filter(staff_number="DF549"))
        self.assertEqual(test_volunteer, [])