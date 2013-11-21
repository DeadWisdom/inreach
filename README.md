inreach
=======

Scans an IMAP for Iridium messages and posts them to a twitter account.

setup
=======
To begin development, clone the repository and install the requirements:

    > virtualenv env
    ...

    > env/bin/pip install -r requirements.txt
    ...


Create a file named "secrets.py", with the twitter app information and django secret key:

    # secrets.py
    TWITTER_CONSUMER_KEY         = "my app's consumer key"
    TWITTER_CONSUMER_SECRET      = "my app's consumer secret"
    SECRET_KEY                   = "my random string of characters"


Setup the database with syncdb:

    > env/bin/python manage.py syncdb --noinput
    ...
