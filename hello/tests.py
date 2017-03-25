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
        self.assertGreater(y, x)

    def test_delete_meeting(self):
        meeting = self.get_test_meeting()
        CalendarApiViews.add_new_meeting(meeting)
        CalendarApiViews.delete_meeting(meeting)
        mtg = CalendarApiViews.get_meeting_from_db(meeting)
        self.assertIsNone(mtg)

    def test_edit_meeting_name(self):
        raise Exception

    def test_edit_meeting_start_date(self):
        raise Exception

    def test_edit_meeting_place(self):
        raise Exception

    def test_edit_meeting_color(self):
        raise Exception

    def test_edit_meeting_participant(self):
        raise Exception

    def test_get_duration(self):
        raise Exception