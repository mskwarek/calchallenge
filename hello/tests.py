from django.test import TestCase
from datetime import datetime, date, time
from django.utils import timezone
from hello.models import Calendar, Meeting
from views import CalendarApiViews


class CalendarTestCase(TestCase):
    def setUp(self):
        self.cal = Calendar.objects.create(name="TEST")

    def tearDown(self):
        pass

    def get_test_meeting(self):
        start_date = datetime(2017, 5, 18, 12, 0, 0, 0, tzinfo=timezone.utc)
        return Meeting(calendar=self.cal, name="test meeting",
                                         place="test place", start_date=start_date,
                                         participant_surname="abacki")

    def test_insert_new_meeting(self):
        meeting = Meeting(calendar=self.cal, name="test meeting", place="test place",
                          start_date=timezone.now(), end_date=timezone.now(),
                          participant_surname="abacki", creation_date=timezone.now())
        meeting.save(force_insert=True)

    def test_add_new_meeting_with_end_date(self):
        date_to_write = timezone.now()
        meeting = Meeting(calendar=self.cal, name="proper", place="warsaw",
                          start_date=date_to_write, end_date=date_to_write,
                          participant_surname="babacki", creation_date=timezone.now())
        meeting.save(force_insert=True)
        mtg = Meeting.objects.get(name="proper")
        self.assertEqual(date_to_write, mtg.start_date)

    def test_add_new_meeting_without_end_date(self):
        start_date = datetime(2017, 5, 18, 12, 0, 0, 0, tzinfo=timezone.utc)
        new_meeting = Meeting(calendar=self.cal, name="test meeting",
                                         place="test place", start_date=start_date,
                                         participant_surname="abacki")
        CalendarApiViews.add_new_meeting(new_meeting)
        mtg = Meeting.objects.latest('creation_date')
        x = (timezone.now() - datetime(1970, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc)).total_seconds()
        y = (mtg.creation_date - datetime(1970, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc)).total_seconds()
        self.assertGreater(x, y)

    def test_delete_meeting(self):
        meeting = self.get_test_meeting()
        CalendarApiViews.add_new_meeting(meeting)
        CalendarApiViews.delete_meeting(meeting)
        mtg = CalendarApiViews.get_meeting_from_db(meeting)
        self.assertIsNone(mtg)

    def test_edit_meeting_name(self):
        meeting = self.get_test_meeting()
        CalendarApiViews.add_new_meeting(meeting)
        old = CalendarApiViews.get_meeting_from_db(meeting)
        meeting = CalendarApiViews.get_meeting_from_db(meeting)
        meeting.name = "updated name"
        CalendarApiViews.update(meeting)
        new = CalendarApiViews.get_meeting_from_db(meeting)
        self.assertEqual(old.name, "test meeting")
        self.assertEqual(new.name, "updated name")
        self.assertEqual(old.id, new.id)

    def test_edit_meeting_start_date(self):
        meeting = self.get_test_meeting()
        CalendarApiViews.add_new_meeting(meeting)
        old = CalendarApiViews.get_meeting_from_db(meeting)
        meeting = CalendarApiViews.get_meeting_from_db(meeting)
        new_start_date = timezone.now()
        meeting.start_date = new_start_date
        CalendarApiViews.update(meeting)
        new = CalendarApiViews.get_meeting_from_db(meeting)
        self.assertNotEqual(old.start_date, new.start_date)
        self.assertEqual(old.id, new.id)

    def test_edit_meeting_place(self):
        meeting = self.get_test_meeting()
        CalendarApiViews.add_new_meeting(meeting)
        old = CalendarApiViews.get_meeting_from_db(meeting)
        meeting = CalendarApiViews.get_meeting_from_db(meeting)
        meeting.place = "updated place"
        CalendarApiViews.update(meeting)
        new = CalendarApiViews.get_meeting_from_db(meeting)
        self.assertEqual(old.place, "test place")
        self.assertEqual(new.place, "updated place")
        self.assertEqual(old.id, new.id)

    def test_edit_meeting_color(self):
        meeting = self.get_test_meeting()
        CalendarApiViews.add_new_meeting(meeting)
        old = CalendarApiViews.get_meeting_from_db(meeting)
        meeting = CalendarApiViews.get_meeting_from_db(meeting)
        meeting.color = "color"
        CalendarApiViews.update(meeting)
        new = CalendarApiViews.get_meeting_from_db(meeting)
        self.assertEqual(old.color, None)
        self.assertEqual(new.color, "color")
        self.assertEqual(old.id, new.id)

    def test_edit_meeting_participant(self):
        meeting = self.get_test_meeting()
        CalendarApiViews.add_new_meeting(meeting)
        old = CalendarApiViews.get_meeting_from_db(meeting)
        meeting = CalendarApiViews.get_meeting_from_db(meeting)
        meeting.participant_surname = "abacka"
        CalendarApiViews.update(meeting)
        new = CalendarApiViews.get_meeting_from_db(meeting)
        self.assertEqual(old.participant_surname, "abacki")
        self.assertEqual(new.participant_surname, "abacka")
        self.assertEqual(old.id, new.id)

    def test_get_duration(self):
        meeting = self.get_test_meeting()
        CalendarApiViews.add_new_meeting(meeting)
        self.assertEqual(31, meeting.get_duration())

    def test_get_duration_february(self):
        date_to_write = datetime(2017, 1, 31, 12, 0, 0, 0, tzinfo=timezone.utc)
        meeting = Meeting(calendar=self.cal, name="february meeting", place="warsaw",
                          start_date=date_to_write,
                          participant_surname="babacki")
        CalendarApiViews.add_new_meeting(meeting)
        self.assertEqual(28, meeting.get_duration())
