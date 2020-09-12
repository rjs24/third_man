from django.test import TestCase
from ..models import Role, Person, Staff, Volunteer, Working_Hrs
from comms.models import CommsGroup
from django.contrib.auth.models import User
from datetime import datetime, timedelta


class PeopleTest(TestCase):

    def setUp(self):

        self.user_director = User(username='joebl1')
        self.user_manager = User(username='jsmith2')
        self.user_employee_a = User(username='emorse2')
        self.user_employee_b = User(username='jfrost3')
        self.user_director.save()
        self.user_manager.save()
        self.user_employee_a.save()
        self.user_employee_b.save()

        self.role_director = Role.objects.create(role_name="Director", role_responsibility="Everything")
        self.role_manager = Role.objects.create(role_name="manager", role_responsibility="Nearly everything")
        self.role_employee = Role.objects.create(role_name="all_things", role_responsibility="make it all work")
        self.role_director.save()
        self.role_manager.save()
        self.role_employee.save()
        self.top_role = Role.objects.create(role_name="everything", role_responsibility="make it nearly all work")
        self.top_role.save()

        self.director = Person.objects.create(userid=self.user_director, email="joebloggs@email.com", first_name="Joe",
                                              second_name="Bloggs", date_of_birth="1985-06-21", postcode="S1 9AA",
                                              address="29, Acacia Road, Nuttytown", organisation_role=self.role_director,
                                              allowed_access=3, notes="likes pizza", line_manage=self.top_role)

        self.manager = Person.objects.create(userid=self.user_manager, email="johnsmith@email.com", first_name="john",
                                              second_name="smith", date_of_birth="1977-01-03", postcode="LS1 0AA",
                                              address="1, New Street, Drearyton", organisation_role=self.role_manager,
                                              allowed_access=3, notes="likes ice cream", line_manage=self.top_role)

        self.employee_a = Person.objects.create(userid=self.user_employee_a, email="endeavourmorse@email.com", first_name="Endeavour",
                                              second_name="Morse", date_of_birth="1985-06-21", postcode="B1 0AA",
                                              address="2, Old Street, Newtown", organisation_role=self.role_employee,
                                              allowed_access=3, notes="likes curries", line_manage=self.top_role)

        self.employee_b = Person.objects.create(userid=self.user_employee_b, email="jackfrost@email.com", first_name="Jack",
                                              second_name="Frost", date_of_birth="1961-09-14", postcode="G1 0AA",
                                              address="4, Brutalistblock avenue", organisation_role=self.role_employee,
                                              allowed_access=3, notes="likes pasta", line_manage=self.top_role)
        self.director.save()
        self.manager.save()
        self.employee_a.save()
        self.employee_b.save()
        self.comms_employee_grp = CommsGroup.objects.create(group_owner=self.manager, group_name="all",
                                                            group_purpose="general comms")
        self.comms_managers_only = CommsGroup.objects.create(group_owner=self.manager, group_name="managers",
                                                             group_purpose="management")
        self.comms_employee_grp.save()
        self.comms_managers_only.save()
        self.staff_a = Staff.objects.create(person=self.employee_a, staff_number="DF548", nat_insurance_num="DF000000A",
                                            salary=23457)
        self.volunteer_a = Volunteer.objects.create(person=self.employee_b, staff_number="DF549")
        self.staff_a.save()
        self.volunteer_a.save()

    def test_Person_has_Role(self):
        """Check organisation_role is added to """
        self.assertTrue(isinstance(self.director.organisation_role, Role))
        self.assertTrue(isinstance(self.manager.organisation_role, Role))
        self.assertTrue(isinstance(self.employee_a.organisation_role, Role))
        self.assertTrue(isinstance(self.employee_b.organisation_role, Role))

    def test_Role_has_roles(self):
        """Test that Role has responsibly_4_roles where applicable"""
        self.role_director.responsible_4_roles.add(self.role_manager)
        self.role_manager.responsible_4_roles.add(self.role_employee)

        self.assertIn(self.role_manager, self.role_director.responsible_4_roles.all())
        self.assertIn(self.role_employee, self.role_manager.responsible_4_roles.all())

    def test_person_created_in_db_correctly(self):
        """Test that person creation includes info specified in setUp"""
        self.assertEqual(self.employee_b.email, "jackfrost@email.com")
        self.assertEqual(self.director.first_name, "Joe")
        self.assertEqual(self.manager.second_name, "smith")
        self.assertEqual(self.employee_b.address, "4, Brutalistblock avenue")
        self.assertTrue(isinstance(self.employee_a.organisation_role, Role))
        self.assertTrue(isinstance(self.manager.line_manage, Role))

    def test_Staff_and_Volunteer_added_in_db(self):
        """Test that it is possible to add working hours to Staff and Volunteer"""

        for n in range(1, 6):
            shift_name = "Day %s" % n
            wk_hrs = Working_Hrs(shift_name=shift_name, day_of_week=n, start=datetime.strptime("08:30", "%H:%M"),
                                  end=datetime.strptime("17:00", "%H:%M"), duration=timedelta(hours=8))
            wk_hrs.save()
            self.staff_a.hours.add(wk_hrs)
            self.staff_a.save()
        for m in range(6, 8):
            shift_name = "Day %s" % m
            pt_wkhrs = Working_Hrs(shift_name=shift_name, day_of_week=m, start=datetime.strptime("08:30", "%H:%M"),
                                  end=datetime.strptime("13:00", "%H:%M"), duration=timedelta(hours=4.5))
            pt_wkhrs.save()
            self.volunteer_a.hours.add(pt_wkhrs)
            self.volunteer_a.save()
        self.assertEqual(len(list(self.volunteer_a.hours.all())), 2)
        self.assertEqual(len(list(self.staff_a.hours.all())), 5)
        self.assertIn(pt_wkhrs, self.volunteer_a.hours.all())
        self.assertIn(wk_hrs, self.staff_a.hours.all())

    def test_Staff_and_volunteer_detail(self):
        """Test if Staff and volunteer details are saved to db"""
        self.assertEqual(self.volunteer_a.staff_number, "DF549")
        self.assertEqual(self.staff_a.staff_number, "DF548")
        self.assertEqual(self.staff_a.nat_insurance_num, "DF000000A")
