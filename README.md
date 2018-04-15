# Tychopy

Project Tycho API wrapper with python.
Make easy queries and get a `pandas.DataFrame`:

```python
from tycho import Tycho

tycho = Tycho(APIKEY)
tycho.query('CUBA', 'Dengue')
```
`Tyco.query()` infers the region level (countryName, Admin1Name...)  
