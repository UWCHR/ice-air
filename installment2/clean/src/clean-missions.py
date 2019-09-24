# :date: 2019-09-24
# :author: PN
# :copyright: GPL v2 or later
#
# ice-air/installment2/clean/src/clean.py
#
#
import argparse
import sys
import pandas as pd
import numpy as np
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
    parser.add_argument("--status", required=True)
    parser.add_argument("--airports_to_merge", required=True)
    parser.add_argument("--bad_airports", required=True)
    parser.add_argument("--airport_dict", required=True)
    parser.add_argument("--bad_statuses", required=True)
    parser.add_argument("--dtypes_in", required=True)
    parser.add_argument("--dtypes_out", required=True)
    parser.add_argument("--clean_stats", required=True)
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

    # Temp fix for dtypes that differ between tables
    dtypes['msnInvoiceNumber'] = 'object'

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

    df = pd.concat(files, sort=False)
    df_obj = df.select_dtypes(include=['object']).copy()
    input_records = len(df)

    # Convert 'object' columns to categories, where efficient.
    # Implementation via https://www.dataquest.io/blog/pandas-big-data/
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
    del df_obj, converted_obj

    with open(args.clean, 'r') as yamlfile:
        clean = yaml.load(yamlfile)

    df['MissionTotalCost'] = df['MissionTotalCost'].astype(object)
    df['MissionTotalCost'] = df['MissionTotalCost'].fillna(0)
    df['MissionTotalCost'] = df['MissionTotalCost'].str.replace(',', '')
    df['MissionTotalCost'] = df['MissionTotalCost'].astype(float)
    dtypes['MissionTotalCost'] = 'float'

    df['msnFlightODCCost'] = df['msnFlightODCCost'].astype(object)
    df['msnFlightODCCost'] = df['msnFlightODCCost'].fillna(0.00)
    df['msnFlightODCCost'] = df['msnFlightODCCost'].str.replace(',', '')
    df['msnFlightODCCost'] = df['msnFlightODCCost'].astype(float)
    dtypes['msnFlightODCCost'] = 'float'

    df['msnProposedFines'] = df['msnProposedFines'].astype(object)
    df['msnProposedFines'] = df['msnProposedFines'].fillna(0.00)
    df['msnProposedFines'] = df['msnProposedFines'].str.replace(',', '')
    df['msnProposedFines'] = df['msnProposedFines'].astype(float)
    dtypes['msnProposedFines'] = 'float'

    df['msnEnforcedFines'] = df['msnEnforcedFines'].astype(object)
    df['msnEnforcedFines'] = df['msnEnforcedFines'].fillna(0.00)
    df['msnEnforcedFines'] = df['msnEnforcedFines'].str.replace(',', '')
    df['msnEnforcedFines'] = df['msnEnforcedFines'].astype(float)
    dtypes['msnEnforcedFines'] = 'float'

    to_csv_opts = {'sep': '|',
                   'quotechar': '"',
                   'compression': 'gzip',
                   'encoding': 'utf-8',
                   'index': False}

    output_len = len(df)
    df.to_csv(args.output, **to_csv_opts)

    # Outputting a few YAML dictionaries used in downstream tasks
    # First updating data types that we've cleaned here:

    with open(args.dtypes_out, 'w') as outfile:
        yaml.dump(dtypes, outfile,
                  default_flow_style=False)

    # Outputting cleaning statistics for use in reporting

    clean_stats = dict(number_of_input_files=len(files),
                       input_records=input_records,
                       output_len=output_len)

    with open(args.clean_stats, 'w') as outfile:
        yaml.dump(clean_stats,
                  outfile,
                  default_flow_style=False,
                  allow_unicode=True)

# END.
