#
# :date: 2019-01-16
# :author: PN
# :copyright: GPL v2 or later
#
# ice-air/hashid/src/hashid.py
#
#

import hashlib
import argparse
import pandas as pd
import sys
if sys.version_info[0] < 3:
    raise "Must be using Python 3"


def _get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--arts_fy11", required=True)
    parser.add_argument("--arts_fy12", required=True)
    parser.add_argument("--arts_fy13", required=True)
    parser.add_argument("--arts_fy14", required=True)
    parser.add_argument("--arts_fy15", required=True)
    parser.add_argument("--arts_fy16", required=True)
    parser.add_argument("--arts_fy17", required=True)
    parser.add_argument("--arts_fy18", required=True)
    parser.add_argument("--arts_fy19", required=True)
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def make_hashid(row):
    try:
        s = ''.join([str(getattr(row, f)) for f in hash_fields])
    except:
        print(row)
        raise
    b = bytearray("iceair{}".format(s), encoding='utf8')
    h = hashlib.sha1()
    h.update(b)
    return h.hexdigest()


if __name__ == "__main__":

    args = _get_args()
    print(args)

    read_csv_opts = {'sep': '|',
                     'quotechar': '"',
                     'compression': 'gzip',
                     'encoding': 'utf-8'}
    to_csv_opts = {'sep': '|',
                   'quotechar': '"',
                   'index': False,
                   'compression': 'gzip',
                   'encoding': "utf-8"}

    arts_fy11 = pd.read_csv(args.arts_fy11, **read_csv_opts)
    arts_fy12 = pd.read_csv(args.arts_fy12, **read_csv_opts)
    arts_fy13 = pd.read_csv(args.arts_fy13, **read_csv_opts)
    arts_fy14 = pd.read_csv(args.arts_fy14, **read_csv_opts)
    arts_fy15 = pd.read_csv(args.arts_fy15, **read_csv_opts)
    arts_fy16 = pd.read_csv(args.arts_fy16, **read_csv_opts)
    arts_fy17 = pd.read_csv(args.arts_fy17, **read_csv_opts)
    arts_fy18 = pd.read_csv(args.arts_fy18, **read_csv_opts)
    arts_fy19 = pd.read_csv(args.arts_fy19, **read_csv_opts)

    files = [arts_fy11,
             arts_fy12,
             arts_fy13,
             arts_fy14,
             arts_fy15,
             arts_fy16,
             arts_fy17,
             arts_fy18,
             arts_fy19]

    for file in files:
        hash_fields = file.columns

        file['hashid'] = file.apply(make_hashid, axis=1)
        assert len(set(file['hashid'])) == len(file['hashid'])

        del hash_fields

    arts_fy11.to_csv('output/arts_fy11.csv.gz', **to_csv_opts)
    arts_fy12.to_csv('output/arts_fy12.csv.gz', **to_csv_opts)
    arts_fy13.to_csv('output/arts_fy13.csv.gz', **to_csv_opts)
    arts_fy14.to_csv('output/arts_fy14.csv.gz', **to_csv_opts)
    arts_fy15.to_csv('output/arts_fy15.csv.gz', **to_csv_opts)
    arts_fy16.to_csv('output/arts_fy16.csv.gz', **to_csv_opts)
    arts_fy17.to_csv('output/arts_fy17.csv.gz', **to_csv_opts)
    arts_fy18.to_csv('output/arts_fy18.csv.gz', **to_csv_opts)
    arts_fy19.to_csv('output/arts_fy19.csv.gz', **to_csv_opts)

# End.
