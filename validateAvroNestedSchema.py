""" Check that json data follows a given Avro schema.

Schema files have to be given in order of internal nests first.
"""

import avro.schema
import avro.io
import io
import json
import argparse
import sys


def combine_schemas(schema_files):
    """Combine multiple nested schemas into a single schema.
    """
    known_schemas = avro.schema.Names()

    for s in schema_files:
        schema = load_single_avsc(s, known_schemas)
    return schema


def load_single_avsc(file_path, names):
    """Load a single avsc file.
    """
    with open(file_path) as file_text:
        json_data = json.load(file_text)
    schema = avro.schema.SchemaFromJSONData(json_data, names)
    return schema


def write_avro_data(json, avro_schema):
    """Encode json into avro format given a schema.
    """
    writer = avro.io.DatumWriter(avro_schema)
    bytes_io = io.BytesIO()
    encoder = avro.io.BinaryEncoder(bytes_io)
    writer.write(json, encoder)
    return bytes_io


def read_avro_data(bytes_io, avro_schema):
    """Read avro data and decode with a given schema.
    """
    raw_bytes = bytes_io.getvalue()
    bytes_reader = io.BytesIO(raw_bytes)
    decoder = avro.io.BinaryDecoder(bytes_reader)
    reader = avro.io.DatumReader(avro_schema)
    message = reader.read(decoder)
    return message


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('schema', metavar='file.avsc', type=str, nargs='+',
                        help='schema file(s)')
    parser.add_argument('data', metavar='file.json', type=str,
                        help='json data file to fill the schema')

    args = parser.parse_args()
    json_path = args.data
    schema_files = args.schema

    with open(json_path) as file_text:
        json_data = json.load(file_text)

    alert_schema = combine_schemas(schema_files)
    avro_bytes = write_avro_data(json_data, alert_schema)
    message = read_avro_data(avro_bytes, alert_schema)

    print(message)
    print("size in bytes of json message: %d" % sys.getsizeof(json_data))
    raw_bytes = avro_bytes.getvalue()
    print("size in bytes of avro message: %d" % sys.getsizeof(raw_bytes))

if __name__ == "__main__":
    main()
