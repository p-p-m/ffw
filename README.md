# Filters for water (FFW)

Simple django web store

Installation
----
1. Create `ffw/settings/custom.py` file (you can use `ffw/settings/custom.py.example` as template) and configure your
custom database and other settings.

2. Setup mysql database (if you don't have it):

        CREATE DATABASE ffw CHARACTER SET utf8 COLLATE utf8_general_ci;
        CREATE USER 'ffw_user'@'localhost' IDENTIFIED BY 'ffw_password';
        GRANT ALL ON ffw.* TO 'ffw_user'@'localhost';

3. Sync and migrate base:

        make syncdb

4. Run tests:

        make test

5. Start site:

        make run