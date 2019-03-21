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
    parser.add_argument("--status", required=True)
    parser.add_argument("--missing_airports", required=True)
    parser.add_argument("--airport_dict", required=True)
    parser.add_argument("--bad_statuses", required=True)
    parser.add_argument("--bad_droplocs", required=True)
    parser.add_argument("--bad_pulocs", required=True)
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

    predrop = len(df)
    df = df[~df['PULOC'].isnull()]
    postdrop = len(df)
    print(f'Dropped {predrop - postdrop} records with null PULOC')
    del predrop, postdrop

    predrop = len(df)
    df = df[~df['DropLoc'].isnull()]
    postdrop = len(df)
    print(f'Dropped {predrop - postdrop} records with null DropLoc')
    del predrop, postdrop

    # Filling in some missing airport name and country values from hand/.
    # Could integrate this with process for removing duplicate airports?

    missing = pd.read_csv(args.missing_airports)

    air_names = list(df['air_AirportName'].cat.categories)
    air2_names = list(df['air2_AirportName'].cat.categories)
    air_countries = list(df['air_Country'].cat.categories)
    air2_countries = list(df['air2_Country'].cat.categories)

    air_names.extend(list(missing['airport_name']))
    air2_names.extend(list(missing['airport_name']))
    air_countries.extend(list(missing['airport_country']))
    air2_countries.extend(list(missing['airport_country']))

    df['air_AirportName'].cat.set_categories(set(air_names), inplace=True)
    df['air2_AirportName'].cat.set_categories(set(air2_names), inplace=True)
    df['air_Country'].cat.set_categories(set(air_countries), inplace=True)
    df['air2_Country'].cat.set_categories(set(air2_countries), inplace=True)

    for index, row in missing.iterrows():
        code = row['airport_code']
        name = row['airport_name']
        country = row['airport_country']
        df.loc[df['PULOC'] == code, 'air_Country'] = country
        df.loc[df['PULOC'] == code, 'air_AirportName'] = name
        df.loc[df['DropLoc'] == code, 'air2_Country'] = country
        df.loc[df['DropLoc'] == code, 'air2_AirportName'] = name

    with open(args.clean, 'r') as yamlfile:
        clean = yaml.load(yamlfile)

    # Want to be careful that this is not deleting anything we want to keep
    # Also we will want to move this into a pre-import step for public repo
    # And it takes a long time to regex entire DF, we probably only need to
    # do the `Status` and `GangMember` fields.
    df.replace(to_replace='[0-9]{8,9}',
               value='POSSIBLE A NUMBER DELETED',
               regex=True,
               inplace=True)

    for key in clean.keys():
        print(f'Cleaning {key}')
        df[key] = df[key].replace(clean[key])
        df[key] = df[key].astype('category')

    df['CountryOfCitizenship'].astype('str', inplace=True)
    df['CountryOfCitizenship'] = df['CountryOfCitizenship'].str.upper()
    df['CountryOfCitizenship'].fillna('UNKNOWN', inplace=True)

    out_of_bounds_high = df['Age'] > 99
    out_of_bounds_low = df['Age'] < 0
    df.loc[out_of_bounds_high, 'Age'] = np.nan
    df.loc[out_of_bounds_low, 'Age'] = np.nan
    assert df['Age'].min() == 0

    df['Juvenile'].fillna(False, inplace=True)

    # Could standardize column name capitalization here
    df['PULOC'] = df['PULOC'].str.upper()
    df['PULOC'] = df['PULOC'].astype('category')
    df['DropLoc'] = df['DropLoc'].str.upper()
    df['DropLoc'] = df['DropLoc'].astype('category')

    status = pd.read_csv(args.status)
    valid_status_codes = list(status['Code'])
    df['Status'] = df['Status'].str.upper()
    df['Status'] = df['Status'].astype('category')

    invalid_status = df[~df['Status'].isin(valid_status_codes)]
    status_counts = invalid_status['Status'].value_counts()
    bad_statuses = list(status_counts[status_counts > 0].index)

    with open(args.bad_statuses, 'w') as outfile:
            yaml.dump(bad_statuses, outfile,
                      default_flow_style=False,
                      allow_unicode=True)

    df['NonCriminal'] = df['Criminality'] == 'NC'
    df['NonCriminal'] = df['NonCriminal'].astype('category')

    # Dropping duplicate records caused by merge of bad airport data by ICE.
    # Should end with set of unique `AlienMasterID` values.
    # Should not affect any statistics caluclated using unique `AlienMasterID`.

    bad_pulocs = pd.read_csv(args.bad_pulocs)
    bad_droplocs = pd.read_csv(args.bad_droplocs)

    premerge = len(df)
    df = pd.merge(df, bad_pulocs, how='left')
    df = pd.merge(df, bad_droplocs, how='left')
    postmerge = len(df)
    assert premerge == postmerge
    del premerge, postmerge

    predrop = len(df)
    df = df[df['PULOC_drop'].isnull()]
    df = df[df['DropLoc_drop'].isnull()]
    postdrop = len(df)
    print(f'Dropped {predrop - postdrop} records with duplicated airports.')
    assert len(df) == len(set(df.AlienMasterID))

    df = df.drop(['PULOC_drop', 'DropLoc_drop'], axis=1)

    to_csv_opts = {'sep': '|',
                   'quotechar': '"',
                   'compression': 'gzip',
                   'encoding': 'utf-8',
                   'index': False}

    df.to_csv(args.output, **to_csv_opts)

    dtypes['Juvenile'] = 'bool'
    dtypes['CountryOfCitizenship'] = 'category'
    dtypes['NonCriminal'] = 'bool'

    with open(args.dtypes_out, 'w') as outfile:
        yaml.dump(dtypes, outfile,
                  default_flow_style=False)

    pickup_names = df[['PULOC', 'air_AirportName']].drop_duplicates()
    pickup_names.set_index('PULOC', inplace=True)
    dropoff_names = df[['DropLoc', 'air2_AirportName']].drop_duplicates()
    dropoff_names.set_index('DropLoc', inplace=True)

    pickup_dict = pickup_names.to_dict()['air_AirportName']
    dropoff_dict = dropoff_names.to_dict()['air2_AirportName']

    airport_dict = {**pickup_dict, **dropoff_dict}

    with open(args.airport_dict, 'w') as outfile:
            yaml.dump(airport_dict, outfile, default_flow_style=False, allow_unicode=True)
# END.
