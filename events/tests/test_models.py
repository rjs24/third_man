from django.test import TestCase
from ..models import Event
from datetime import datetime, timedelta
from people.models import Person, Role
from comms.models import CommsGroup
from django.contrib.auth.models import User


class EventTest(TestCase):
    """Test event module"""
    @classmethod
    def setUp(self):
        self.start_count = Event.objects.count()
        self.user = User(username='emorse2')
        self.user.save()
        self.rogue_user = User(username='jfrost3')
        self.rogue_user.save()
        self.role = Role.objects.create(role_name="nearly all_things", role_responsibility="make nearly it all work")
        self.role.save()
        self.top_role = Role.objects.create(role_name="all_things", role_responsibility="make it all work")
        self.top_role.save()
        self.person_a = Person.objects.create(userid=self.user, email="joebloggs@email.com", first_name="joe",
                                        second_name="bloggs", date_of_birth=datetime.strptime("1985-06-21", "%Y-%m-%d"),
                                        postcode="S1 9AA", address= "29, Acacia Road, Nuttytown", organisation_role=self.role,
                                        allowed_access=3, notes="likes pizza", line_manage=self.top_role)
        self.person_a.save()
        self.rogue_employee = Person.objects.create(userid=self.rogue_user, email="jackfrost@email.com", first_name="Jack",
                                        second_name="Frost", date_of_birth=datetime.strptime("1961-09-14", "%Y-%m-%d"),
                                        postcode="G1 0AA", address="4, Brutalistblock avenue", organisation_role=self.role,
                                        allowed_access=1, notes="likes rice", line_manage=self.top_role)
        self.rogue_employee.save()

        self.comms_grp = CommsGroup.objects.create(group_owner=self.person_a, group_name="fete group",
                                                   group_purpose="support summer fete")
        self.comms_grp.save()


        self.event_a = Event.objects.create(title="summer fete",
                                  start=datetime.strptime("2020-07-03 12:00", "%Y-%m-%d %H:%M"),
                                  end=datetime.strptime("2020-07-03 16:00", "%Y-%m-%d %H:%M"), event_owner=self.person_a,
                                  duration=timedelta(hours=4),
                                  recurrence_interval=0, description="happy summer fete", website_publish=True)
        self.event_b = Event.objects.create(title="sunday service",
                                  start=datetime.strptime("2020-03-08 10:00", "%Y-%m-%d %H:%M"),
                                  end=datetime.strptime("2020-03-08 11:00","%Y-%m-%d %H:%M"), event_owner=self.person_a,
                                  duration=timedelta(hours=1),
                                  recurrence_interval=2, description="regular Sunday 10 am service", website_publish=False)
        self.event_a.save()
        self.event_b.save()

    def test_event_model_will_create_new_event(self):
        """simple check to see if event count has gone up"""
        new_count = Event.objects.count()
        self.assertNotEqual(self.start_count, new_count)

    def test_event_data(self):
        """test event titles and other attributes"""
        self.assertTrue(isinstance(self.event_a, Event))
        self.assertTrue(self.event_a.start, datetime)
        self.assertEqual(self.event_a.title, "summer fete")
        self.assertTrue(self.event_a.end, datetime)
        self.assertTrue(self.event_a.duration, timedelta)


    def test_event_recurence(self):
        """test if recurring=True auto creates other events from start date"""
        event_b_date = self.event_b.start
        while event_b_date.year != 2021:
            event_b_date = event_b_date + timedelta(days=7)
            try:
                new_event = Event.objects.get(start=event_b_date)
                self.assertTrue(isinstance(new_event, EventTest))
                self.assertEqual(new_event.title, "sunday service")
                if event_b_date.year == 2021:
                    assert True, "Event recurrence tested"
                    break
                else:
                    continue
            except Event.DoesNotExist:
                assert False, "Event object (new_event) not found"
                break

    def test_event_duration(self):
        """Test to see if the duration of the event has been calculated correctly"""
        start_time = self.event_a.start
        end_time = self.event_a.end
        difference = end_time - start_time
        self.assertEqual(difference, self.event_a.duration)

# to implement, probably using a cms
    # def test_website_publish(self):
    #     """test to see if website_publish=True passes data to publish on website in Website app"""
    #     event = self.event_a
    #     public_events = PublicEvent.objects.create(event=event, more_info_link='http://organisation.co.uk/tree_campaign',
    #         ticket_link='http://organisation.co.uk/tickets', contact_number='00000000',
    #         twitter_link='http://twitter.com/event', facebook_link='http://facebook.com/event',
    #         linked_organisation='http://save_the_snails.co.uk')
    #     self.assertTrue(isinstance(event, PublicEvent))
    #     self.assertEqual(public_events.event.website_publish, True)
    #     self.assertEqual(public_events.more_info_link, 'http://organisation.co.uk/tree_campaign')
    #     if public_events:
    #         assert True, "target_event published"
    #     else:
    #         assert False, "target_event not published"

    def test_add_invites_groups(self):
        """Testing if a group can add people/persons"""
        initial_invites = self.comms_grp.group_membership.count()
        self.comms_grp.group_membership.add(self.person_a)
        self.comms_grp.group_membership.add(self.rogue_employee)
        final_invites = self.comms_grp.group_membership.count()
        self.assertNotEqual(initial_invites, final_invites)
        self.assertEqual(final_invites, 2)

    def test_event_add_invites(self):
        """Test if event can add comms_grp to invites attribute"""
        self.event_a.invites.add(self.comms_grp)
        self.assertIn(self.comms_grp, self.event_a.invites.all())

    def test_website_publish_blocking_if_no_access(self):
        """A person should only be able to publish if they have allowed_access=3"""
        rogue_event = Event.objects.create(title="Needless meeting",
                                  start=datetime.strptime("2020-03-27 12:00", "%Y-%m-%d %H:%M"),
                                  end=datetime.strptime("2020-03-27 16:00", "%Y-%m-%d %H:%M"), event_owner=self.rogue_employee,
                                  duration=timedelta(hours=4),
                                  recurrence_interval=0, description="a meeting", website_publish=True)
        rogue_event.save()
        public_rogue_event = PublicEvent.objects.create(event=rogue_event, more_info_link='http://organisation.co.uk/rogue_campaign',
            ticket_link='http://organisation.co.uk/tickets', contact_number='00000000',
            twitter_link='http://twitter.com/rogue_event', facebook_link='http://facebook.com/rogue_event',
            linked_organisation='http://save_the_slugs.co.uk')
        public_rogue_event.save()
        self.assertTrue(isinstance(public_rogue_event, PublicEvent))
        self.assertEqual(public_rogue_event.event.website_publish, False)
        self.assertNotEqual(public_rogue_event.more_info_link, 'http://organisation.co.uk/rogue_campaign')




        public_events = PublicEvent.event.objects.get(website_publish=True)
        for events in public_events:
            if events.event_owner.allowed_access < 3:
                assert False
            else:
                assert True



