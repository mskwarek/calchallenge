from django.test import TestCase
from hello.models import Calendar, Meeting
import datetime


class CalendarTestCase(TestCase):
    def setUp(self):
        self.cal = Calendar.objects.create(name="TEST")

    def test_animals_can_speak(self):
        meeting = Meeting(calendar = self.cal, name="test meeting", place="test place", start_date=datetime.datetime.now(),
                                         end_date=datetime.datetime.now(), participant_surname="abacki")

