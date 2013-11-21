import json
from django.utils import formats
from django.db import models
from django.contrib.auth.models import User


UPDATE_TYPES = (
    ('checking', 'Checking...'),
    ('verified', 'Verified'),
    ('check', 'Checked'),
    ('fail', 'Failed'),
    ('messages', 'Messages'),
)


class Account(models.Model):
    user = models.ForeignKey(User, related_name="accounts")
    address = models.CharField(max_length=255)
    port = models.CharField(max_length=255, default='993')
    login = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return "Account(%s)" % self.id

    def last_checked(self):
        try:
            return self.updates.filter(type='check')[0].when
        except IndexError:
            return None

    def status(self):
        if not self.id:
            return "not yet created"
        try:
            last_update = self.updates.filter(type='check')[0]
        except IndexError:
            return 'verifying...'
        parts = [last_update.get_display_type()]
        last_checked = self.last_checked()
        if last_checked:
            parts.append("last checked: %s" % formats.date_format(last_checked, "SHORT_DATETIME_FORMAT"))
        return " | ".join(parts)

    def update(self, type, data=None):
        return Update.objects.create(account=self, type=type, data_src=json.dumps(data))


class Message(models.Model):
    account = models.ForeignKey(Account)
    sender = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    loc = models.CharField(max_length=255, blank=True)
    body = models.TextField()
    sent = models.DateTimeField()
    hash = models.SlugField(blank=True)
    processed = models.BooleanField(default=False)

    def __unicode__(self):
        return "Message(%s)" % self.id



class Update(models.Model):
    account = models.ForeignKey(Account, related_name="updates")
    type = models.SlugField(choices=UPDATE_TYPES)
    data_src = models.TextField(blank=True)
    when = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "Update(%s: %s)" % (self.id, self.description)

    @property
    def data(self):
        if not hasattr(self, '_data'):
            self._data = json.loads(data_src)
        return self._data

    class Meta:
        ordering = ['-id']

