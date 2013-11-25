import time

from django.core.management.base import BaseCommand, CommandError

from app.management import mail, tweet
from app.models import Account
from multiprocessing import Pool


class Command(BaseCommand):
    help = 'Starts a process to get messages and route them to twitter.'

    def handle(self, *args, **options):
        self.stdout.write("Starting to churn messages...")
        pool = Pool(10)
        while True:
            accounts = list(Account.objects.all())
            print "update"
            pool.map(mail.update, accounts)
            print "process_new_messages"
            pool.map(tweet.process_new_messages, accounts)
            print "done."
            time.sleep(60 * 5)  # Every 5 minutes
