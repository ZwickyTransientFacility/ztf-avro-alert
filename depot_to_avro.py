
import copy
import json
from glob import glob
import pandas as pd
import numpy as np
import tarfile
import uuid
import base64
import io
# fastavro can't handle nested schemas
#import fastavro
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter
import avro.schema
from validateAvroNestedSchema import combine_schemas

schema_files = ['schema/candidate.avsc', 'schema/prv_candidate.avsc',
                'schema/cutout.avsc', 'schema/alert.avsc']

alert_schema = avro.schema.Parse(json.dumps(combine_schemas(schema_files)))


def load_all_candidates():
    """Take a sample ztf-depot directory and convert all candidates into json"""
    base_dir = 'data/ztf-depot/'
    candidate_files = glob(base_dir + '*/*/public/*/*cands.txt')
    for candidate_file in candidate_files:
        try:
            write_avro(candidate_file, outdir='data/ztf_avro_packets')
        except:
            print(f'Bad candidate: {candidate_file}')

# temporary single event testing:
candidate_file = 'data/ztf_2016122322956_000515_sg_c16_o_q4_cands.txt'


def write_avro(candidate_file, schema=alert_schema, outdir='data/'):

    df = read_ztf_depot_candidate(candidate_file)
    dc = DepotCutout(candidate_file)
    for i, row in df.iterrows():
        # TODO: make the alert id something meaningful and distinct from candid
        alertId = int(np.abs(row.candid))
        alert = {"alertId": alertId,
                 "candid": row.candid}
        alert['candidate'] = row.to_dict()
        df_hist = dc.read_history(row.candid)
        if df_hist is None:
            alert['prv_candidates'] = None
        else:
            hist = [hrow.to_dict() for (j, hrow) in df_hist.iterrows()]
            # can't get pandas to use native types with the Nones, and
            # avro doesn't handle numpy types
            hist_retyped = []
            for hrow in hist:
                hist_retyped.append(
                    {k: candidate_converters[k](v) for (k, v) in hrow.items()})
            alert['prv_candidates'] = hist_retyped

        alert['cutoutScience'] = dc.read_sci(row.candid, row.pid)
        alert['cutoutTemplate'] = dc.read_ref(row.candid, row.pid)
        alert['cutoutDifference'] = dc.read_scimref(row.candid, row.pid)

        with open('{}/{}.avro'.format(outdir, alertId), 'wb') as f:
            #fastavro.schemaless_writer(f, schema, alert)
            #fastavro.writer(f, schema, alert)
            writer = DataFileWriter(f, DatumWriter(), schema)
            writer.append(alert)
            writer.close()


# parsing these fixed width sql dumps is gross.  For now it looks like I need to
# define a bunch of converters so I can force the data types to be correct,
# particularly for empty fields.
# (pandas can't use the dtype argument with skipfooter)

candidate_names = \
    ['jd', 'fid', 'pid', 'diffmaglim', 'pdiffimfilename', 'programpi',
     'programid', 'candid', 'isdiffpos', 'tblid', 'nid', 'rcid',
     'field', 'xpos', 'ypos', 'ra', 'dec', 'magpsf', 'sigmapsf',
     'chipsf', 'magap', 'sigmagap', 'distnr', 'magnr', 'sigmagnr',
     'chinr', 'sharpnr', 'sky', 'magdiff', 'fwhm', 'classtar', 'mindtoedge',
     'magfromlim', 'seeratio', 'aimage', 'bimage', 'aimagerat', 'bimagerat',
     'elong', 'nneg', 'nbad', 'rb', 'ssdistnr', 'ssmagnr', 'ssnamenr', 'sumrat',
     'strcat', 'sgmag', 'sgscore', 'luid', 'name', 'ra_lu', 'dec_lu', 'a',
     'b2arat', 'pa', 'dm', 'dmkin', 'btc', 'objtype', 'm21', 'source']


# fields not in history
not_in_history = ['strcat', 'sgmag', 'sgscore', 'luid', 'name', 'ra_lu',
                  'dec_lu', 'a', 'b2arat', 'pa', 'dm', 'dmkin',
                  'btc', 'objtype', 'm21', 'source']

history_names = copy.deepcopy(candidate_names)

for field in not_in_history:
    history_names.remove(field)


def str2val(tok, converter, null):
    """If string is not empty, convert it to numpy type

    converter: function, eg np.float32
    null: value for empty strings (e.g., np.nan)"""
    tok = tok.strip()
    if len(tok):
        return converter(tok)
    else:
        return null

str2double = lambda tok: str2val(tok, float, None)
str2float = lambda tok: str2val(tok, float, None)
# python 3 has no long
str2long = lambda tok: str2val(tok, int, None)
str2int = lambda tok: str2val(tok, int, None)
str2str = lambda tok: str2val(tok, str, None)

candidate_converters = \
    {'jd': str2double, 'fid': str2int, 'pid': str2long,
     'diffmaglim': str2float, 'pdiffimfilename': str2str, 'programpi': str2str,
     'programid': str2int, 'candid': str2long, 'isdiffpos': str2int,
     'tblid': str2long, 'nid': str2int, 'rcid': str2int,
     'field': str2int, 'xpos': str2float, 'ypos': str2float,
     'ra': str2double, 'dec': str2double,
     'magpsf': str2float, 'sigmapsf': str2float,
     'chipsf': str2float, 'magap': str2float, 'sigmagap': str2float,
     'distnr': str2float, 'magnr': str2float, 'sigmagnr': str2float,
     'chinr': str2float, 'sharpnr': str2float, 'sky': str2float,
     'magdiff': str2float, 'fwhm': str2float, 'classtar': str2float,
     'mindtoedge': str2float, 'magfromlim': str2float, 'seeratio': str2float,
     'aimage': str2float, 'bimage': str2float,
     'aimagerat': str2float, 'bimagerat': str2float,
     'elong': str2float, 'nneg': str2int, 'nbad': str2int, 'rb': str2float,
     'ssdistnr': str2float, 'ssmagnr': str2float, 'ssnamenr': str2str,
     'sumrat': str2float, 'strcat': str2int, 'sgmag': str2float,
     'sgscore': str2float, 'luid': str2long, 'name': str2str,
     'ra_lu': str2double, 'dec_lu': str2double, 'a': str2float,
     'b2arat': str2float, 'pa': str2float, 'dm': str2float, 'dmkin': str2float,
     'btc': str2float, 'objtype': str2float, 'm21': str2float,
     'source': str2str}


# def retype(x):
#    if type(x) is np.int64:
#        return int(x)
#    elif type(x) is np.float64:
#        return float(x)
#    else:
#        return x


def read_ztf_depot_candidate(candidate_file):
    df = pd.read_table(candidate_file, sep='|', skiprows=2, skipfooter=1,
                       names=candidate_names, converters=candidate_converters)

    return df


class DepotCutout:
    """Class for facilitating access to the data stored in depot cutouts"""

    def __init__(self, candidate_file):
        self.candidate_file = candidate_file
        self.cutout_file = candidate_file.replace(
            'cands.txt', 'candcutouts.tar.gz')
        # for reading within the tarfile
        self.prefix = self.cutout_file.split('/')[-1][:-7]
        self.open_cutouts()

    def open_cutouts(self):
        self.tf = tarfile.open(self.cutout_file, 'r')

    def read_image(self, candid, pid, suffix, targ='targ'):

        # targ could be "hist" for historical cutouts. different pids
        if suffix != 'ref':
            member = '{}/candid{}_pid{}_{}_{}.jpg'.format(
                self.prefix, candid, pid, targ, suffix)
        else:
            member = '{}/candid{}_ref.jpg'.format(self.prefix, candid)

        # returns bytes, which is what we want
        f = self.tf.extractfile(member)
        return {'fileName': member, 'stampData': f.read()}

    def read_sci(self, candid, pid):
        return self.read_image(candid, pid, 'sci')

    def read_scimref(self, candid, pid):
        return self.read_image(candid, pid, 'scimref')

    def read_ref(self, candid, pid):
        return self.read_image(candid, pid, 'ref')

    def read_history(self, candid):
        member = '{}/candid{}_history.txt'.format(self.prefix, candid)
        # tarfile returns this as bytes, which requires an annoying
        # workaround to get into pandas
        try:
            f = self.tf.extractfile(member)
        except KeyError:
            return None
        # Python 3: read to bytes...
        b = f.read()
        #... and decode
        data = b.decode('ascii')
        # drop the last footer line  so  we don't need skipfooter and
        # read_table can use the C parser
        data = '\n'.join(data.split('\n')[:-2])
        # and make a file-like object again...
        fs = io.StringIO(data)
        df = pd.read_table(fs, sep='|', skiprows=2,
                           names=history_names, dtype=str)
        # converters=candidate_converters)

        # replace NaNs with None (null).  Changes all dtypes to object
        # return df.where((pd.notnull(df)), None)
        return df
