ztf-avro-alert
=================

Repository with the ZTF Avro schemas, example data products, and simple example scripts demonstrating how to work with them.  Public access to ZTF alerts is provided by the [University of Washington](https://ztf.uw.edu/alerts/public/).

[Additional documentation](https://zwickytransientfacility.github.io/ztf-avro-alert/) is available in the `docs` directory.  Of particular interest is the [guide to the alert contents](https://zwickytransientfacility.github.io/ztf-avro-alert/schema.html).

There is an [example notebook](https://github.com/ZwickyTransientFacility/ztf-avro-alert/blob/master/notebooks/Working_with_avro_files.ipynb) which provides a tutorial for loading the alert packet contents in python.  Another notebook shows [example filters for transients](https://github.com/ZwickyTransientFacility/ztf-avro-alert/blob/master/notebooks/Filtering_alerts.ipynb).

Schemas are in `schema/` and are given as .avsc files.  `alert.avsc` is the top-level schema.

Example Avro packets are saved as binary files in `data/`.  A simple script to print the contents of a packet to the terminal is in `bin/`.

Requires python 3 and `avro.schema` for combining nested schemas, which you can get with `pip install avro-python3`. The python2 `avro` is significantly different from `avro-python3` and will not work here without addressing those changes.
Better performance may be obtained with the `fastavro` library, available with `pip install fastavro`.
