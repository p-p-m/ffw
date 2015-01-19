import logging
import os

from .base import *


IS_TEST = True

TEST_DISCOVER_TOP_LEVEL = BASE_DIR
TEST_DISCOVER_ROOT = BASE_DIR


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    },
}


SECRET_KEY = '9v*1)^ixje!h8920_yf7cnb2d7e7!sv@bnm_fym1l)tr7&amp;fst&amp;'

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'testmedia')
EMAIL_FILE_PATH = os.path.join(PROJECT_ROOT, 'testmails/')
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
DEFAULT_FROM_EMAIL = 'webmaster@localhost'

SOUTH_TESTS_MIGRATE = False  # To disable migrations and use syncdb instead
SKIP_SOUTH_TESTS = True      # To disable South's own unit tests

logging.disable(logging.CRITICAL)
