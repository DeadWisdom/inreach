#!env/bin/python

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

from churn import churn
churn()