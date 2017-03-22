ztf-avro-alert
=================

Repo for a sample ZTF alert in Avro format and simple Python code to populate an Avro schema and print. Schemas are given as .avsc files. Data are given as .json files. Postage stamp cutout files can be included.

Requires python3 and `avro.schema` for combining nested schemas, which you can get with `pip install avro-python3`. The python2 `avro` is significantly different from `avro-python3` and will not work here without addressing those changes.

Requires `fastavro` for faster serialization, which you can get with `pip install fastavro`.

Jupyter notebooks included in `examples`.

Usage
-----

On the command line, pass schema files first and then a single json data file last.
Multiple nested schemas must be passed in order of most internal first:

```
python validateAvroNestedSchema.py \
  schema/candidate.avsc \
  schema/cutout.avsc \
  schema/alert.avsc \
  data/alert.json \
  --cutoutSci data/ztf_2016122322956_000515_sg_c16_o_q4_candcutouts/candid-87704463155000_pid-8770446315_targ_sci.jpg \
  --cutoutTemp data/ztf_2016122322956_000515_sg_c16_o_q4_candcutouts/candid-87704463155000_ref.jpg \
  --cutoutDiff data/ztf_2016122322956_000515_sg_c16_o_q4_candcutouts/candid-87704463155000_pid-8770446315_targ_scimref.jpg
```
