sample-avro-alert
=================

Repo for a sample alert in Avro format and simple Python code to populate an Avro schema and print. Schemas are given as .avsc files. Data are given as .json files. Postage stamp cutout files can be included.

Requires `avro.schema` for combining nested schemas, which you can get with `pip install avro-python3`.

Requires `fastavro` for faster serialization, which you can get with `pip install fastavro`.

Jupyter notebooks included in `examples`.

Usage
-----

On the command line, pass schema files first and then a single json data file last:

```
python validateAvroNestedSchema.py schema/simple.avsc data/simple.json
```

Multiple nested schemas must be passed in order of most internal first:

```
python validateAvroNestedSchema.py schema/diasource.avsc schema/diaobject.avsc schema/ssobject.avsc schema/cutout.avsc schema/alert.avsc data/alert.json
```

For example, this will not work:

```
python validateAvroNestedSchema.py schema/alert.avsc schema/diaobject.avsc schema/ssobject.avsc schema/diasource.avsc schema/cutout.avsc data/alert.json
```

"Postage stamp" cutout files (difference and template images) can be included as optional arguments:

```
python validateAvroNestedSchema.py schema/diasource.avsc schema/diaobject.avsc schema/ssobject.avsc schema/cutout.avsc schema/alert.avsc data/alert.json --cutoutDiff examples/stamp-40320.fits --cutoutTemp examples/stamp-48960.fits
```

The collected stamps will then appear in a local 'output' directory.
