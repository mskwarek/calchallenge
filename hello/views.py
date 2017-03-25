from django.shortcuts import render
import datetime
from models import Meeting, Calendar


class CalendarApiViews():
    @staticmethod
    def validate_fields(meeting):
        if meeting.name is None or meeting.calendar is None \
                or meeting.participant_surname is None or meeting.place is None\
                or meeting.start_date is None:
            raise Exception
        if meeting.end_date is None:
            meeting.end_date = meeting.start_date + datetime.timedelta(days=30)
        meeting.creation_date = datetime.datetime.now()

    @staticmethod
    def add_new_meeting(meeting):
        CalendarApiViews.validate_fields(meeting)
        meeting.save(force_insert=True)

    @staticmethod
    def get_meeting_from_db(meeting):
        try:
            return Meeting.objects.get(calendar=meeting.calendar, name=meeting.name,
                                       place=meeting.place, creation_date=meeting.creation_date,
                                       start_date=meeting.start_date)
        except:
            return None

    @staticmethod
    def delete_meeting(meeting):
        instance = CalendarApiViews.get_meeting_from_db(meeting)
        instance.delete()
