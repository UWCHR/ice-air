#
# :date: 2019-02-01
# :author: PN
# :copyright: GPL v2 or later
#
# ice-air/clean/src/clean.py
#
#
import pandas as pd
import numpy as np
import argparse
import sys
import yaml
if sys.version_info[0] < 3:
    raise "Must be using Python 3"


def _get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fy11", required=True)
    parser.add_argument("--fy12", required=True)
    parser.add_argument("--fy13", required=True)
    parser.add_argument("--fy14", required=True)
    parser.add_argument("--fy15", required=True)
    parser.add_argument("--fy16", required=True)
    parser.add_argument("--fy17", required=True)
    parser.add_argument("--fy18", required=True)
    parser.add_argument("--fy19", required=True)
    parser.add_argument("--clean", required=True)
    parser.add_argument("--dtypes_in", required=True)
    parser.add_argument("--dtypes_out", required=True)
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def mem_usage(pandas_obj):
    if isinstance(pandas_obj, pd.DataFrame):
        usage_b = pandas_obj.memory_usage(deep=True).sum()
    else:  # we assume if not a df it's a series
        usage_b = pandas_obj.memory_usage(deep=True)
    usage_mb = usage_b / 1024 ** 2  # convert bytes to megabytes
    return "{:03.2f} MB".format(usage_mb)


if __name__ == "__main__":
    args = _get_args()

    with open(args.dtypes_in, 'r') as yamlfile:
        dtypes = yaml.load(yamlfile)

    read_csv_opts = {'sep': '|',
                     'quotechar': '"',
                     'compression': 'gzip',
                     'encoding': 'utf-8',
                     'dtype': dtypes,
                     'parse_dates': ['MissionDate'],
                     'infer_datetime_format': True}

    arts_fy11 = pd.read_csv(args.fy11, **read_csv_opts)
    arts_fy12 = pd.read_csv(args.fy12, **read_csv_opts)
    arts_fy13 = pd.read_csv(args.fy13, **read_csv_opts)
    arts_fy14 = pd.read_csv(args.fy14, **read_csv_opts)
    arts_fy15 = pd.read_csv(args.fy15, **read_csv_opts)
    arts_fy16 = pd.read_csv(args.fy16, **read_csv_opts)
    arts_fy17 = pd.read_csv(args.fy17, **read_csv_opts)
    arts_fy18 = pd.read_csv(args.fy18, **read_csv_opts)
    arts_fy19 = pd.read_csv(args.fy19, **read_csv_opts)

    files = [arts_fy11,
             arts_fy12,
             arts_fy13,
             arts_fy14,
             arts_fy15,
             arts_fy16,
             arts_fy17,
             arts_fy18,
             arts_fy19]

    df = pd.concat(files)
    df_obj = df.select_dtypes(include=['object']).copy()

    converted_obj = pd.DataFrame()

    for col in df_obj.columns:
        num_unique_values = len(df_obj[col].unique())
        num_total_values = len(df_obj[col])
        if num_unique_values / num_total_values < 0.5:
            converted_obj.loc[:, col] = df_obj[col].astype('category')
        else:
            converted_obj.loc[:, col] = df_obj[col]

    df[converted_obj.columns] = converted_obj

    with open(args.clean, 'r') as yamlfile:
        clean = yaml.load(yamlfile)

    for key in clean.keys():
        print(f'Cleaning {key}')
        df[key] = df[key].replace(clean[key])
        df[key] = df[key].astype('category')

    df['CountryOfCitizenship'].cat.add_categories(['UNKNOWN'], inplace=True)
    df['CountryOfCitizenship'].fillna('UNKNOWN', inplace=True)

    # out_of_bounds_high = df['Age'] > 99
    # out_of_bounds_low = df['Age'] < 0
    # df.loc[out_of_bounds_high, 'Age'] = np.nan
    # df.loc[out_of_bounds_low, 'Age'] = np.nan
    # assert df['Age'].min() == 0

    # Could standardize column name capitalization here
    df['PULOC'] = df['PULOC'].str.upper()
    df['PULOC'] = df['PULOC'].astype('category')
    df['DropLoc'] = df['DropLoc'].str.upper()
    df['DropLoc'] = df['DropLoc'].astype('category')

    to_csv_opts = {'sep': '|',
                   'quotechar': '"',
                   'compression': 'gzip',
                   'encoding': 'utf-8',
                   'index': False}

    df.to_csv(args.output, **to_csv_opts)

    dtypes['Juvenile'] = 'bool'

    with open(args.dtypes_out, 'w') as outfile:
        yaml.dump(dtypes, outfile, default_flow_style=False)
# END.
