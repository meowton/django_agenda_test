from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    address = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    event_date = models.DateTimeField()
    created_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Event"
        ordering = ["-event_date"]

    def __str__(self):
        return self.title

    def get_event_date(self):
        return self.event_date.strftime("%d/%m/%Y, %H:%M")

    def get_event_date_str(self):
        return self.event_date.strftime("%Y-%m-%dT%H:%M")

    def is_event_date_past(self):
        return True if self.event_date < datetime.now() else False

    def is_event_date_due(self):
        # return True if self.event_date > datetime.now() - timedelta(hours=3) else False
        current_time = datetime.now() + timedelta(hours=3)
        event_time = self.event_date + timedelta(hours=3)
        return (
            True
            if self.event_date < current_time < event_time
            else False
        )
