# :date: 2020-12-11
# :author: PN
# :copyright: GPL v2 or later
#
# ice-air/installment3/clean/src/clean-passengers.py
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
    parser.add_argument("--airports_to_merge", required=True)
    parser.add_argument("--bad_airports", required=True)
    parser.add_argument("--airport_dict_updated", required=True)
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

    with open(args.airport_dict_updated, 'r') as yamlfile:
        air_dict = yaml.load(yamlfile)

    name_dict = {v['AirportName']: k for k, v in air_dict.items()}

    df['PULOC'] = df['air_AirportName'].replace(name_dict)
    df['DropLoc'] = df['air2_AirportName'].replace(name_dict)

    # AlienMasterID redacted in installment3, therefore we replace with
    # unique, arbitrary ID values here. We know from installment1 that
    # AlienMasterID is not particularly meaningful.

    df['AlienMasterID'] = range(len(df))
    df['AlienMasterID'] = df['AlienMasterID'].astype(int)
    dtypes['AlienMasterID'] = 'int'

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

    predrop = len(df)
    df = df[~df['air_AirportID'].isin([29.0, 90.0, 165.0])]
    df = df[~df['air2_AirportID'].isin([29.0, 90.0, 165.0])]
    postdrop = len(df)
    dropped_bad_airports = predrop - postdrop
    print(f'Dropped {dropped_bad_airports} records with bad airport metadata.')
    del predrop, postdrop

    predrop = len(df)
    df = df[~df['PULOC'].isnull()]
    postdrop = len(df)
    null_puloc = predrop - postdrop
    print(f'Dropped {null_puloc} records with null PULOC')
    del predrop, postdrop

    predrop = len(df)
    df = df[~df['DropLoc'].isnull()]
    postdrop = len(df)
    null_droploc = predrop - postdrop
    print(f'Dropped {null_droploc} records with null DropLoc')
    del predrop, postdrop

    # Fixing some missing/bad airport name and country values from hand/.
    # This ignores some fields we don't use in analysis, like AirportID
    # and StateID values.
    # Not sure all this category fiddling is necessary?

    bad = pd.read_csv(args.bad_airports)

    air_names = list(df['air_AirportName'].cat.categories)
    air2_names = list(df['air2_AirportName'].cat.categories)
    air_countries = list(df['air_Country'].cat.categories)
    air2_countries = list(df['air2_Country'].cat.categories)
    air_cities = list(df['air_City'].cat.categories)
    air2_cities = list(df['air2_City'].cat.categories)
    air_states = list(df['st_StateAbbr'].cat.categories)
    air2_states = list(df['st2_StateAbbr'].cat.categories)

    air_names.extend(list(bad['airport_name'].dropna()))
    air2_names.extend(list(bad['airport_name'].dropna()))
    air_countries.extend(list(bad['airport_country'].dropna()))
    air2_countries.extend(list(bad['airport_country'].dropna()))
    air_cities.extend(list(bad['airport_city'].dropna()))
    air2_cities.extend(list(bad['airport_city'].dropna()))
    air_states.extend(list(bad['airport_state'].dropna()))
    air2_states.extend(list(bad['airport_state'].dropna()))

    df['air_AirportName'].cat.set_categories(set(air_names), inplace=True)
    df['air2_AirportName'].cat.set_categories(set(air2_names), inplace=True)
    df['air_Country'].cat.set_categories(set(air_countries), inplace=True)
    df['air2_Country'].cat.set_categories(set(air2_countries), inplace=True)
    df['air_City'].cat.set_categories(set(air_cities), inplace=True)
    df['air2_City'].cat.set_categories(set(air2_cities), inplace=True)
    df['st_StateAbbr'].cat.set_categories(set(air_states), inplace=True)
    df['st2_StateAbbr'].cat.set_categories(set(air2_states), inplace=True)

    for index, row in bad.iterrows():
        code = row['airport_code']
        name = row['airport_name']
        city = row['airport_city']
        state = row['airport_state']
        country = row['airport_country']
        df.loc[df['PULOC'] == code, 'air_Country'] = country
        df.loc[df['PULOC'] == code, 'air_AirportName'] = name
        df.loc[df['PULOC'] == code, 'air_City'] = city
        df.loc[df['PULOC'] == code, 'st_StateAbbr'] = state
        df.loc[df['DropLoc'] == code, 'air2_Country'] = country
        df.loc[df['DropLoc'] == code, 'air2_AirportName'] = name
        df.loc[df['DropLoc'] == code, 'air2_City'] = city
        df.loc[df['DropLoc'] == code, 'st2_StateAbbr'] = state

    with open(args.clean, 'r') as yamlfile:
        clean = yaml.load(yamlfile)

    df['CountryOfCitizenship'] = df['CountryOfCitizenship'].astype('str')
    df['CountryOfCitizenship'] = df['CountryOfCitizenship'].str.upper()
    df['CountryOfCitizenship'].fillna('UNKNOWN', inplace=True)

    for key in clean.keys():
        if key == 'airport_codes':
            pass
        else:
            print(f'Cleaning {key}')
            df[key] = df[key].replace(clean[key])
            df[key] = df[key].astype('category')

    age_high_bound = 99
    age_low_bound = 0
    out_of_bounds_high = df['Age'] > age_high_bound
    out_of_bounds_low = df['Age'] < age_low_bound
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

    airports_to_merge = pd.read_csv(args.airports_to_merge)
    df = pd.merge(df, airports_to_merge,
                  left_on='PULOC',
                  right_on='ICAOCode',
                  how='left')
    df = df.drop(['ICAOCode'], axis=1)
    df = df.rename({'LongitudeDecimalDegrees': 'air_LongitudeDecimalDegrees',
                    'LatitudeDecimalDegrees': 'air_LatitudeDecimalDegrees'},
                   axis=1)
    df = pd.merge(df, airports_to_merge,
                  left_on='DropLoc',
                  right_on='ICAOCode',
                  how='left')
    df = df.drop(['ICAOCode'], axis=1)
    df = df.rename({'LongitudeDecimalDegrees': 'air2_LongitudeDecimalDegrees',
                    'LatitudeDecimalDegrees': 'air2_LatitudeDecimalDegrees'},
                   axis=1)

    df['NonCriminal'] = df['Criminality'] == 'NC'
    df['NonCriminal'] = df['NonCriminal'].astype('category')

    to_csv_opts = {'sep': '|',
                   'quotechar': '"',
                   'compression': 'gzip',
                   'encoding': 'utf-8',
                   'index': False}

    output_len = len(df)
    df.to_csv(args.output, **to_csv_opts)

    # Outputting a few YAML dictionaries used in downstream tasks
    # First updating data types that we've cleaned here:

    dtypes['Juvenile'] = 'bool'
    dtypes['CountryOfCitizenship'] = 'category'
    dtypes['NonCriminal'] = 'bool'
    dtypes['air_LongitudeDecimalDegrees'] = 'float'
    dtypes['air_LatitudeDecimalDegrees'] = 'float'
    dtypes['air2_LongitudeDecimalDegrees'] = 'float'
    dtypes['air2_LatitudeDecimalDegrees'] = 'float'

    with open(args.dtypes_out, 'w') as outfile:
        yaml.dump(dtypes, outfile,
                  default_flow_style=False)

    # Creating a standard set of airport codes and names
    # We could standardize all airport metadata in this task, including
    # longitude/latitude, if desired, especially since some is broken.
    dict_cols = ['AirportName',
                 'LongitudeDecimalDegrees',
                 'LatitudeDecimalDegrees',
                 'State',
                 'City',
                 'Country']
    pickup_data = df[['PULOC',
                      'air_AirportName',
                      'air_LongitudeDecimalDegrees',
                      'air_LatitudeDecimalDegrees',
                      'st_StateAbbr',
                      'air_City',
                      'air_Country']].drop_duplicates()
    pickup_data.set_index('PULOC', inplace=True)
    pickup_data.columns = dict_cols
    dropoff_data = df[['DropLoc',
                       'air2_AirportName',
                       'air2_LongitudeDecimalDegrees',
                       'air2_LatitudeDecimalDegrees',
                       'st2_StateAbbr',
                       'air2_City',
                       'air2_Country']].drop_duplicates()
    dropoff_data = dropoff_data.drop_duplicates(subset='DropLoc', keep='first')
    dropoff_data.set_index('DropLoc', inplace=True)
    dropoff_data.columns = dict_cols

    pickup_dict = pickup_data.to_dict('index')
    dropoff_dict = dropoff_data.to_dict('index')
    airport_dict = {**pickup_dict, **dropoff_dict}

    with open(args.airport_dict, 'w') as outfile:
        yaml.dump(airport_dict,
                  outfile,
                  default_flow_style=False,
                  allow_unicode=True)

    # Outputting cleaning statistics for use in reporting

    clean_stats = dict(input_records=input_records,
                       dropped_bad_airports=dropped_bad_airports,
                       null_puloc=null_puloc,
                       null_droploc=null_droploc,
                       age_high_bound=age_high_bound,
                       age_low_bound=age_low_bound,
                       output_len=output_len)

    with open(args.clean_stats, 'w') as outfile:
        yaml.dump(clean_stats,
                  outfile,
                  default_flow_style=False,
                  allow_unicode=True)

# END.
