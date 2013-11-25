import re, time, email, imaplib

from app.models import Message, Account


class IMAPError(RuntimeError):
    pass


def login(account):
    try:
        print "connecting", account.address, int(account.port)
        client = imaplib.IMAP4_SSL(account.address, int(account.port))
    except:
        raise IMAPError("Unnable to connect to the imap server.")

    try:
        print "login", account.login, "******"
        result, name = client.login(account.login, account.password)
        client.name = name
        return client
    except:
        raise IMAPError("Unnable to authenticate with the given login and password")


re_uid = re.compile("UID (\d+)")
def get_id_from_envelope(envelope):
    m = re_uid.search(envelope)
    if m:
        return m.group(1)


def get_new_uids(account, client, uids):
    all = set(uids)
    used = set(Message.objects.filter(uid__in=all).values_list('uid', flat=True))
    return all - used


def build_new_messages(account, client):
    print 'search', None, account.search
    result, data = client.uid('search', None, account.search)
    data = " ".join(data)
    uids = data.split()
    new_uids = get_new_uids(account, client, uids)
    if not new_uids:
        return []
    print 'fetch', ",".join(new_uids), 'RFC822'
    result, data = client.uid('fetch', ",".join(new_uids), 'RFC822')
    new = []
    for parts in data:
        if len(parts) != 2:
            continue
        envelope, raw = parts
        uid = get_id_from_envelope(envelope)
        m = Message(account=account, uid=uid)
        m.set_message(email.message_from_string(raw))
        m.save()
        new.append(m)
    return new


def update(account):
    print "updating -", account
    account.update('updating')
    try:
        client = login(account)
        print "select INBOX"
        client.select("INBOX")
        new = build_new_messages(account, client)
        account.update('updated', [m.simple() for m in new])
    except IMAPError, e:
        account.update('fail', str(e))
    except Exception, e:
        raise
        account.update('fail', "Error in update: %s" % e)

