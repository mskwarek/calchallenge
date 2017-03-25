from django.db import models
import datetime


class Calendar(models.Model):
    name = models.CharField(max_length=256)


class Meeting(models.Model):
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    place = models.CharField(max_length=1024)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    participant_surname = models.CharField(max_length=512)
    creation_date = models.DateTimeField()
    color = models.CharField(max_length=128, null=True)

    def get_duration(self):
        return (self.end_date-self.start_date).total_days()
