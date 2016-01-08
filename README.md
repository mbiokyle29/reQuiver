# reQuiver
#### Archer DX Quiver Fusion Database + Python Requests
#### This is an **unoffical** library, all content is copyright of Archer DX ####
#### This is also a webscraper, appropriate and responsible useage is required ####
#### It does it's best to cache things though ####
Python Library for Interacting with Archer DX Quiver Fusion Database

Example:
```python
import reQuiver

# instantiate and query
requiver = reQuiver()
results_set = requiver.query("cancer")  # any query is fine, gene, disease, fusion

# results set is an instance of QuiverResultSet
# has:
# QuiverResultSet.panels (an array of panels)
# QuiverResultSet.fusions (an array of fusions)
for panel in results_set.panels:
    print panel.genes

for fusion in results_set.fusions:
    print fusion.annotation
```