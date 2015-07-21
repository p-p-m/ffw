## Before starting work

Currently product is base is not stable, so migrations are not fully supported.
Thats means that DB has to be recreated after each pull from develop.

To reinit DB:
 - delete exist database file
 - execute: `make initdb` - command will create new DB and fill it with test data

For easier template integration all views parameters are described in file docs/views.md.


## Architecture detail and agreements

1. Now all templates (and mostly all views) are located in application `assembly`. We will move them to separate
applications only after code stabilization (we will decide what views and templates are reusable).

2. All js logic that are related to backend(operations with cart, adding filters to URL ...) are based on
data-.. attributes of tags so better to avoid usage of this attributes for frontend-related js.

