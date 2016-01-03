# requiver
Python Library for Interacting with Archer DX Quiver Fusion Database

#### This is an unoffical library, all content is copyright of Archer DX ####
#### This is also a webscraper, appropriate and responsible useage is required ####

### useage
Simple example:

```python
import Requiver

# create an instance
req = Requiver()

# query the db
query_results = req.query("SOME_GENE")

# The query returns a results object, which is a thin wrapper containing two arrays
# .panels contains the panels which were hits for the query
# .fusions contains the fusions which were hits for the query

for panel in query_results.panels:
  print panel

for fusion in query_results.fusions:
  print fusion
```
