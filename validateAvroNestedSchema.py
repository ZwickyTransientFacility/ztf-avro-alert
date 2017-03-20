""" Check that json data follows a given Avro schema.

Schema files have to be given in order of internal nests first.
"""

import avro.schema
import fastavro
import io
import json
import argparse
import sys
import os.path
import hashlib


def combine_schemas(schema_files):
    """Combine multiple nested schemas into a single schema.
    """
    known_schemas = avro.schema.Names()

    for s in schema_files:
        schema = load_single_avsc(s, known_schemas)
    return schema.to_json()


def load_single_avsc(file_path, names):
    """Load a single avsc file.
    """
    with open(file_path) as file_text:
        json_data = json.load(file_text)
    schema = avro.schema.SchemaFromJSONData(json_data, names)
    return schema


def load_stamp(file_path):
    """Load a cutout postage stamp file to include in alert.
    """
    _, fileoutname = os.path.split(file_path)
    with open(file_path, mode='rb') as f:
        cutout_data = f.read()
        cutout_dict = {"fileName": fileoutname, "stampData": cutout_data}
    return cutout_dict


def write_stamp_file(stamp_dict, output_dir):
    """Given a stamp dict that follows the cutout schema, write data to a file in a given directory.
    """
    filename = stamp_dict['fileName']
    try:
        os.makedirs(output_dir)
    except OSError:
        pass
    out_path = os.path.join(output_dir, filename)
    with open(out_path, 'wb') as f:
        f.write(stamp_dict['stampData'])
    return out_path


def write_avro_data(json_data, json_schema):
    """Encode json with fastavro module into avro format given a schema.
    """
    bytes_io = io.BytesIO()
    fastavro.schemaless_writer(bytes_io, json_schema, json_data)
    return bytes_io


def read_avro_data(bytes_io, json_schema):
    """Read avro data with fastavro module and decode with a given schema.
    """
    bytes_io.seek(
        0)  # force schemaless_reader to read from the start of stream, byte offset = 0
    message = fastavro.schemaless_reader(bytes_io, json_schema)
    return message


def check_md5(infile, outfile):
    """Compare the MD5 hash values of two files.
    """
    with open(infile, 'rb') as f:
        in_data = f.read()
        in_md5 = hashlib.md5(in_data).hexdigest()
    with open(outfile, 'rb') as f:
        out_data = f.read()
        out_md5 = hashlib.md5(out_data).hexdigest()
    return in_md5 == out_md5


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('schema', metavar='file.avsc', type=str, nargs='+',
                        help='schema file(s)')
    parser.add_argument('data', metavar='file.json', type=str,
                        help='json data file to fill the schema')
    parser.add_argument('--cutoutSci', metavar='science.jpg', type=str,
                        help='file for science image postage stamp')
    parser.add_argument('--cutoutTemp', metavar='template.jpg', type=str,
                        help='file for template image postage stamp')
    parser.add_argument('--cutoutDiff', metavar='difference.jpg', type=str,
                        help='file for difference image postage stamp')


    args = parser.parse_args()
    json_path = args.data
    schema_files = args.schema
    cutoutsci_path = args.cutoutSci
    cutouttemp_path = args.cutoutTemp
    cutoutdiff_path = args.cutoutDiff

    alert_schema = combine_schemas(schema_files)

    with open(json_path) as file_text:
        json_data = json.load(file_text)

    # Load science stamp if included
    if cutoutsci_path is not None:
        cutoutTemplate = load_stamp(cutoutsci_path)
        json_data['cutoutScience'] = cutoutTemplate

    # Load template stamp if included
    if cutouttemp_path is not None:
        cutoutTemplate = load_stamp(cutouttemp_path)
        json_data['cutoutTemplate'] = cutoutTemplate

    # Load difference stamp if included
    if cutoutdiff_path is not None:
        cutoutDifference = load_stamp(cutoutdiff_path)
        json_data['cutoutDifference'] = cutoutDifference


    avro_bytes = write_avro_data(json_data, alert_schema)
    message = read_avro_data(avro_bytes, alert_schema)

    # Print message text to screen
    message_text = {k: message[k] for k in message if k not in [
        'cutoutScience', 'cutoutDifference', 'cutoutTemplate']}
    print(message_text)

    # Collect stamps as files written to local directory 'output' and check hashes match expected
    if message.get('cutoutScience') is not None:
        stamp_temp_out = write_stamp_file(message.get('cutoutScience'), 'output')
        print('Science stamp ok:', check_md5(args.cutoutSci, stamp_temp_out))

    if message.get('cutoutTemplate') is not None:
        stamp_temp_out = write_stamp_file(message.get('cutoutTemplate'), 'output')
        print('Template stamp ok:', check_md5(args.cutoutTemp, stamp_temp_out))

    if message.get('cutoutDifference') is not None:
        stamp_diff_out = write_stamp_file(message.get('cutoutDifference'), 'output')
        print('Difference stamp ok:', check_md5(args.cutoutDiff, stamp_diff_out))


    print("size in bytes of json text: %d" % sys.getsizeof(message_text))
    raw_bytes = avro_bytes.getvalue()
    print("size in bytes of avro message: %d" % sys.getsizeof(raw_bytes))


if __name__ == "__main__":
    main()
