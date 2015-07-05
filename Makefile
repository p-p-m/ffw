# find . -name "*.pyc" -exec rm -rf {} \;

# settings:
APPLICATION = ffw
CONFIG = settings.custom
TEST_CONFIG = settings.test

# python path:
PYPATH=$(PWD%%/)$(APPLICATION)

# execute scrips:
MAINSCRIPT = django-admin.py
MANAGESCRIPT = python $(APPLICATION)/manage.py

SCRIPT = PYTHONPATH=$(PYPATH) DJANGO_SETTINGS_MODULE=$(CONFIG) $(MAINSCRIPT)
TEST_SCRIPT = PYTHONPATH=$(PYPATH) DJANGO_SETTINGS_MODULE=$(TEST_CONFIG) $(MAINSCRIPT)


# commands:

test:
	$(TEST_SCRIPT) test $(APP)

run:
	$(SCRIPT) runserver $(PORT)

migrate:
	$(SCRIPT) migrate

manage:
	$(MANAGESCRIPT) $(CMD)

shell:
	$(MANAGESCRIPT) shell

collectstatic:
	$(SCRIPT) collectstatic --noinput

validate:
	$(SCRIPT) validate

reinitdb:
	$(MANAGESCRIPT) flush --noinput
	$(MANAGESCRIPT) createtestdata
	$(MANAGESCRIPT) createbanners

initdb:
	$(SCRIPT) migrate
	$(MANAGESCRIPT) createtestdata
	$(MANAGESCRIPT) createbanners
