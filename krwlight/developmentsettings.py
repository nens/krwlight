# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from krwlight.settings import *

DEBUG = True

LOGGING['loggers']['']['level'] = DEBUG
RAVEN_CONFIG = None


try:
    from krwlight.localsettings import *
    # For local dev overrides.
except ImportError:
    pass
