# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.

from krwlight.settings import *

DATABASES = {
    # Changed server from production to staging
    'default': {
        'NAME': 'krwlight',
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'USER': 'krwlight',
        'PASSWORD': 'jj#4)93eak',
        'HOST': 's-web-db-00-d03.external-nens.local',
        'PORT': '5432',
        },
    }

# TODO: Put your real url here to configure Sentry.
# RAVEN_CONFIG = {
#     'dsn': ('http://some:hash@your.sentry.site/some_number')}

# TODO: add staging gauges ID here.
UI_GAUGES_SITE_ID = ''  # Staging has a separate one.
