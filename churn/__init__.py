import time
import imap
import tweet_out

from app.models import Account
from multiprocessing import Pool


def churn():
    pool = Pool(10)
    while True:
        accounts = list(Account.objects.all())
        print "update"
        pool.map(imap.update, accounts)
        print "process_new_messages"
        pool.map(tweet_out.process_new_messages, accounts)
        print "done."
        time.sleep(60 * 5)  # Every 5 minutes
