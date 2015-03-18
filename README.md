# Filters for water (FFW)

Simple django web store

Installation
----
1. Setup virtual environment and activate it:

        virtualenv venv
        source venv/bin/activate

2. Install develop requirements:

        pip install -r requirements/dev.txt

3. Create `ffw/settings/custom.py` file (you can use `ffw/settings/custom.py.example` as template) and configure your
custom database and other settings.

4. Setup mysql database (if you don't have it):

        CREATE DATABASE ffw CHARACTER SET utf8 COLLATE utf8_general_ci;
        CREATE USER 'ffw_user'@'localhost' IDENTIFIED BY 'ffw_password';
        GRANT ALL ON ffw.* TO 'ffw_user'@'localhost';

5. Sync and migrate base:

        make syncdb

6. Run tests:

        make test

7. Start site:

        make run

8. Static builder

        npm install
        bower install

also ruby, ruby gems, gem sass-lang is required.

        sudo su -c "gem install sass"

for watch static

        grunt

for compile static

        grunt build
