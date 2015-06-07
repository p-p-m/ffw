# Basic information

Products - base application of project that implement 'Product' model and product-related features

# Parameters of views from application 'products'

## Context processors(available at each view):

- sections context processor:
   - `sections` - list of all active sections. Categories can be extracted from section with `get_categories` method.
   Similarly subcategories can be extracted from category with `get_subcategories` method.

## Views

- `home`:
  - `main` - banner for main page.
  - `subcategories` - list of active subcategories
