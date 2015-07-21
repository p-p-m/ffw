# Code style and general architecture rules

General recommendations for project developers.

## Imports

(TODO: translate to English)

В нашем проекте импорты делятся на 4 блока:
1. Испорты из `__xxx__` приложений. Например: `from __future__ import unicode_literals`
2. Иморты из модулей встроеных питона. Например из `from datetime import datetime` или `import re`
3. Импорты из установленых модулей. Например: `from django import db`
4. Импорты из внутрених модулей. Например `from . import models`, `from products import views`

Каждый блок отделяется одной пустой строкой от предидущего.

Импорты в пределах одного блока размещаются по алфавиту ориентируясь на названия модуля а не ключевого слова(например `import datetime` будет выше чем `from django import db` потому что `datetime` идет раньше по алфавиту чем `django`).

Если модули испортируются из одного источника они должны быть объединены в один импорт.

Правильно:
`from django import db, forms`

Не правильно:
```
from django import db
from django import forms
```

(TODO: Add application structure here)
