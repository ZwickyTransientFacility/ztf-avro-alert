ZTF Avro Alert Format
=====================

This page provides basic documentation for the alert stream data formats
deployed by the [Zwicky Transient Facility](http://ztf.caltech.edu).

The alerts are formatted as [Apache Avro](https://avro.apache.org/).  Avro is an open-source structured data serialization format that uses schemas to validate and enforce data types and contents.  Avro client libraries are available for many major programming languages.  For Python 3, the `avro-python3` library can be obtained with `pip install avro-python3`.  Better performance may be obtained with the `fastavro` library, available with `pip install fastavro`.

The [Schema page](schema.md) provides a human-readable guide to the alert fields. 

An [example notebook](https://github.com/ZwickyTransientFacility/ztf-avro-alert/blob/master/notebooks/Working_with_avro_files.ipynb) provides a tutorial for accessing the alert packet contents from python.

The ZTF Avro schemas may be seen [here](https://github.com/ZwickyTransientFacility/ztf-avro-alert/tree/master/schema).  

Sample alert packets are [here](https://github.com/ZwickyTransientFacility/ztf-avro-alert/tree/master/data).  

