# Tychopy

[Project Tycho API](https://www.tycho.pitt.edu/) wrapper with python.
Make easy queries and get a `pandas.DataFrame`:

```python
from tycho import Tycho

tycho = Tycho(APIKEY)
tycho.query('CUBA', 'Dengue')
```
Instance `Tyco()` with your `APIKEY`. Get it from https://www.tycho.pitt.edu/accounts/profile/
after logging in. 

`Tyco.query()` infers the region level (countryName, Admin1Name...)  

Project Tycho site: https://www.tycho.pitt.edu/
