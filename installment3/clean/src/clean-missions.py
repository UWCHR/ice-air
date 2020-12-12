# :date: 2020-12-11
# :author: PN
# :copyright: GPL v2 or later
#
# ice-air/installment3/clean/src/clean-missions.py
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
    parser.add_argument("--input", required=True)
    parser.add_argument("--clean", required=True)
    parser.add_argument("--status", required=True)
    parser.add_argument("--mission_airports", required=True)
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

    df = pd.read_csv(args.input, **read_csv_opts)

    df_obj = df.select_dtypes(include=['object']).copy()
    input_records = len(df)

    df['msnVendor'] = df['msnVendor'].str.upper()

    # Tail numbers redacted in installment 3
    # df['MsnTailNumber'] = df['MsnTailNumber'].str.upper()

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

    # Cost cols redacted in installment 3
    # cost_cols = ['MissionTotalCost',
    #              'msnFlightODCCost',
    #              'msnProposedFines',
    #              'msnEnforcedFines']

    # for col in cost_cols:
    #     df[col] = df[col].astype(object)
    #     df[col] = df[col].fillna(0)
    #     df[col] = df[col].str.replace(',', '')
    #     df[col] = df[col].astype(float)
    #     dtypes[col] = 'float'



    # Mission stop cols redacted in installment 3 
    # stop_cols = ['MsnStart',
    #              'MsnStpOne',
    #              'MsnStpTwo',
    #              'MsnStpThree',
    #              'MsnStpFour',
    #              'MsnStpFive',
    #              'MsnStpSix',
    #              'MsnStpSeven',
    #              'MsnStpEight',
    #              'MsnEnd']

    # for key in clean.keys():
    #     if key != 'airport_codes':
    #         pass
    #     else:
    #         for col in stop_cols:
    #             print(f'Cleaning {col}')
    #             df[col] = df[col].replace(clean[key])
    #             df[col] = df[col].astype('category')

    # Mission dataset with partially reconstructed stops itinerary from passengers dataset
    # Note we can have duplicate airports as `PULOC`, `DropLoc` for a given mission
    mission_airports = pd.read_csv(args.mission_airports, sep='|')

    pulocs = mission_airports.groupby('MissionID')['PULOC'].unique()
    droplocs = mission_airports.groupby('MissionID')['DropLoc'].unique()

    pulocs_df = pulocs.apply(pd.Series)
    droplocs_df = droplocs.apply(pd.Series)

    pulocs_df.columns = [f'puloc_{i+1}' for i in pulocs_df.columns]
    droplocs_df.columns = [f'droploc_{i+1}' for i in droplocs_df.columns]

    stops = pd.concat([pulocs_df, droplocs_df], axis=1)

    df = df.set_index('MissionID')
    df = pd.concat([df, stops], axis=1)
    df = df.reset_index()

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

    clean_stats = dict(input_records=input_records,
                       output_len=output_len)

    with open(args.clean_stats, 'w') as outfile:
        yaml.dump(clean_stats,
                  outfile,
                  default_flow_style=False,
                  allow_unicode=True)

# END.
