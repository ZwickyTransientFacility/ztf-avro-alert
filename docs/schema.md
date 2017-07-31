ZTF Avro Schemas
================

These documents are for schema v1.1.

## Schema Heirarchy

ZTF uses nested schemas to organize the data in the alert packet.

`ztf.alert` (defined in [`alert.avsc`](https://github.com/ZwickyTransientFacility/ztf-avro-alert/blob/master/schema/alert.avsc)) is the top-level namespace.  In turn


### ztf.alert


### ztf.alert.candidate

### ztf.alert.prv_candidate

The `prv_candidates` field contains an array of one or more previous subtraction candidates at the position of the alert.  These are obtained by a simple cone search at the position of the alert candidate on the last 30 days of history.  If there are no previous candidates or upper limits, this field is null.

The fields for an individual `prv_candidate` are identical to `candidate` except for the omission of `sgmag`, `sgscore`, `ndethist`, `ncovhist`, `jdstarthist`, and `jdendhist`.

## ztf.alert.cutout

Each cutout contains two fields:

| Field | Type | Contents |
|:--------|:-------:|--------:|
| `fileName` | string | Original cutout location |
| `stampData` | bytes | JPEG cutout image |
