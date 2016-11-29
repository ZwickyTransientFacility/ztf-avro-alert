sample-avro-alert
=================

Repo for a sample alert in Avro format and simple Python code to populate an Avro schema and print. Schemas are given as .avsc files. Data are given as .json files.

Requires `avro.schema` and `avro.io` which you can get with `pip install avro-python3`.

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
