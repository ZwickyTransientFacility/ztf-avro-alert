# Filtering the ZTF alert stream

ZTF alert streams contain an nearly entirely unfiltered stream of all 5-sigma (only the most obvious artefacts are rejected).
Depending on your science case, you may wish to improve the purity of your sample by filtering the data
on the included attributes.

Based on tests done at IPAC (F. Masci, priv. comm), the following filter delivers a relatively pure sample:
```
rb >= 0.65 and
nbad = 0 and
fwhm <= 5 and
elong <= 1.2 and
abs(magdiff) <= 0.1
```

More characterization will follow as the survey and analyses progress.

[This notebook](https://github.com/ZwickyTransientFacility/ztf-avro-alert/blob/master/notebooks/Filtering_alerts.ipynb) provides one example of how to apply these filters.
