#!/usr/bin/env python
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter
import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: ./cat_avro_file.py /path/to/file.avro')   
        sys.exit()
    else:
        fname = sys.argv[1]
    with open(fname,'rb') as f:
        freader = DataFileReader(f,DatumReader())
        for datum in freader:
            print(datum)
