ztf-avro-alert
=================

Repository with the ZTF Avro schemas, example data products, and simple example scripts demonstrating how to work with them. 

Additional documentation is available in the `docs/` directory, which is rendered [here](https://zwickytransientfacility.github.io/ztf-avro-alert/).

Schemas are in `schema/` and are given as .avsc files.  `alert.avsc` is the top-level schema.

Example Avro packets are saved as binary files in `data/`.  A simple script to print the contents of a packet to the terminal is in `bin/`.

Requires python3 and `avro.schema` for combining nested schemas, which you can get with `pip install avro-python3`. The python2 `avro` is significantly different from `avro-python3` and will not work here without addressing those changes.

Usage
-----

```
./bin/cat_avro_file.py data/396522680015040000.avro
```
