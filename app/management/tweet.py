import tweepy
from django.conf import settings
from app.models import Account


def process_message(client, message):
    body = message.sender + ": "
    body += message.body
    if (len(body) >= 115):
        body = body[:115] + "..."
    body += '\n' + message.url

    lat, long = message.loc.split(',')
    print lat, long

    try:
        client.update_status(body, lat=lat.strip(), long=long.strip())
    except:
        pass
    message.processed = True
    message.save()


def process_new_messages(account):
    if not account.send_to_twitter:
        return False
    try:
        messages = tuple(account.messages.exclude(processed=True))
        if messages:
            print "sending to twitter -", account
            client = get_client(account)
            print "client gotten, now to the messages!"
            for message in messages:
                process_message(client, message)
            print "done."
            return True
        else:
            print "No messages."
            return False
    except Exception, e:
        account.update("fail", str(e))


def get_client(account):
    auth = account.user.social_auth.get(provider='twitter')
    tokens = auth.tokens
    access_token = tokens['oauth_token']
    access_token_secret = tokens['oauth_token_secret']
    auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)
