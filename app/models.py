import datetime, rfc822, quopri, re
from django.utils import formats
from django.db import models
from django.contrib.auth.models import User
from ajax import to_json, from_json


### Constants / Helpers ###
UPDATE_TYPES = (
    ('updating', 'Updating...'),
    ('updated', 'Updated'),
    ('fail', 'Failed'),
)

re_subject = re.compile("^inReach message from (.*)")
def get_sender(subject):
    m = re_subject.match(subject)
    if m:
        return m.groups()[0]

def split_body(src):
    first, second = src.split("View the location or send a reply to ")
    return first.strip(), second.strip()

re_link = re.compile("https://explore\.delorme\.com/textmessage/txtmsg\?mo=(\w+)")
def get_link(src):
    return re_link.search(src).group()

re_loc = re.compile("Lat ([-\d\.]+) Lon ([-\d\.]+)")
def get_loc(src):
    return ", ".join(re_loc.search(src).groups())


### Models ###
class Account(models.Model):
    user = models.ForeignKey(User, related_name="accounts")
    address = models.CharField(max_length=255, default="imap.gmail.com")
    port = models.CharField(max_length=255, default='993')
    use_ssl = models.BooleanField("Use SSL", default=True)
    login = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    search = models.CharField(max_length=255, default='(SUBJECT "inReach message") (SENTSINCE 21-Nov-2013)')
    send_to_twitter = models.BooleanField("Send to Twitter", default=False)

    def __unicode__(self):
        return "Account(%s)" % self.id

    def get_last_update(self):
        try:
            return self.updates.all()[0]
        except IndexError:
            return None

    def get_updates_since(self, since=None):
        if not since:
            return self.updates.all().order_by('-id')[:10]
        else:
            return self.updates.filter(id__gt=since).order_by('-id')

    def status(self):
        if not self.id:
            return ''

        last = self.get_last_update()
        if last is None:
            return ''

        return unicode(last)

    def update(self, type, data=None):
        self.updates.filter(when__lt=datetime.datetime.now() - datetime.timedelta(days=1)).delete()
        return Update.objects.create(account=self, type=type, data_src=to_json(data))


class Message(models.Model):
    account = models.ForeignKey(Account, related_name="messages")
    uid = models.CharField(max_length=255)
    sender = models.CharField(max_length=255)
    to = models.CharField(max_length=255)
    loc = models.CharField(max_length=255, blank=True)
    body = models.TextField()
    url = models.CharField(max_length=255)
    raw = models.TextField()
    sent = models.DateTimeField()
    processed = models.BooleanField(default=False)

    def __unicode__(self):
        return "Message(%s)" % self.id

    def set_message(self, message):
        self.sender = get_sender(message['Subject'])
        self.to = message['To']
        if message.is_multipart():
            src = unicode(quopri.decodestring(message.get_payload()[0]))
        else:
            src = unicode(quopri.decodestring(message.get_payload()))
        self.body, rest = split_body(src)
        self.loc = get_loc(rest)
        self.url = get_link(rest)
        self.raw = message.as_string()
        self.sent = datetime.datetime(*rfc822.parsedate(message['Date'])[:6])

    def simple(self):
        data = {}
        for key in ('sender', 'to', 'body', 'sent', 'processed', 'loc'):
            data[key] = getattr(self, key)
        return data

    class Meta:
        ordering = ['-sent']


class Update(models.Model):
    account = models.ForeignKey(Account, related_name="updates")
    type = models.SlugField(choices=UPDATE_TYPES)
    data_src = models.TextField(blank=True)
    when = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        if (self.type == 'fail'):
            return "failed: %s" % self.data
        elif (self.type == 'updated'):
            return "last updated: %s" % formats.date_format(self.when, "SHORT_DATETIME_FORMAT")
        elif (self.type == 'updating'):
            return "updating..."

    def simple(self):
        return {
            'when': self.when,
            'data': self.data,
            'type': self.type,
            'id': self.id
        }

    @property
    def data(self):
        if not hasattr(self, '_data'):
            self._data = from_json(self.data_src)
        return self._data

    class Meta:
        ordering = ['-id']

