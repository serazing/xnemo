xNEMO
=====

xNEMO provides an simple interface to read NEMO simulations using the xarray
library.

To open a dataset from a NEMO simulation, you need to create a `ǸemoSim` object to read data in the path "/data/*":
```
import xnemo
sim = xnemo.io.NemoSim("/data/*")
```

The new variable `sim` contains the NEMO data on the different grids. For instance, the gridU dataset is accessible using ̀`sim.gridU`. Grids and masks are also available.s