from django.test import TestCase
from ..models import CommsGroup
from people.models import Person
from django.contrib.auth.models import User
from people.models import Role


class CommsGroupTest(TestCase):
    """Test event module"""
    def setUp(self):
        self.user_manager = User(username='jsmith2')
        self.user_employee_a = User(username='emorse2')
        self.user_employee_b = User(username='jfrost3')
        self.user_manager.save()
        self.user_employee_a.save()
        self.user_employee_b.save()

        self.role_manager = Role.objects.create(role_name="manager", role_responsibility="Nearly everything")
        self.role_employee = Role.objects.create(role_name="all_things", role_responsibility="make it all work")
        self.role_manager.save()
        self.role_employee.save()
        self.top_role = Role.objects.create(role_name="director", role_responsibility="shareholders")
        self.top_role.save()

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
        self.manager.save()
        self.employee_a.save()
        self.employee_b.save()
        self.comms_employee_grp = CommsGroup.objects.create(group_name="all", group_purpose="general comms",
                                                            group_owner=self.manager)
        self.comms_employee_grp.save()

    def test_group_owner_in_group_membership(self):
        """test that the save method auto added the group_owner to group_membership"""
        self.assertTrue(self.comms_employee_grp.group_owner.id)
        self.assertEqual(self.comms_employee_grp.group_owner.id, self.manager.id)

    def test_group_membership(self):
        """test that people/persons can be added into the comms group"""
        start_count = self.comms_employee_grp.group_membership.count()
        self.comms_employee_grp.group_membership.add(self.employee_a)
        self.comms_employee_grp.group_membership.add(self.employee_b)
        end_count = self.comms_employee_grp.group_membership.count()
        self.assertNotEqual(start_count, end_count)
        self.assertEqual(end_count, 3)

    def test_commsGroup_name_str(self):
        """Test commsGroup name saving okay"""
        self.assertEqual(self.comms_employee_grp.group_name, "all")