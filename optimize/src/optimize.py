#
# :date: 2019-01-17
# :author: PN
# :copyright: GPL v2 or later
#
# ice-air/optimize/src/src/optimize.py
#
# Shamelessly copied from: https://www.dataquest.io/blog/pandas-big-data/
#
import pandas as pd
import argparse
import sys
import yaml
if sys.version_info[0] < 3:
    raise "Must be using Python 3"


def _get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
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

    read_csv_opts = {'sep': '|',
                     'quotechar': '"',
                     'compression': 'gzip',
                     'encoding': 'utf-8'}

    df = pd.read_csv(args.input, **read_csv_opts)

    print(f'Raw size: {mem_usage(df)}')

    optimized_df = df.copy()

    df_int = df.select_dtypes(include=['int'])
    converted_int = df_int.apply(pd.to_numeric, downcast='unsigned')
    optimized_df[converted_int.columns] = converted_int

    df_float = df.select_dtypes(include=['float'])
    converted_float = df_float.apply(pd.to_numeric, downcast='float')
    optimized_df[converted_float.columns] = converted_float

    df_obj = df.select_dtypes(include=['object']).copy()
    converted_obj = pd.DataFrame()

    for col in df_obj.columns:
        num_unique_values = len(df_obj[col].unique())
        num_total_values = len(df_obj[col])
        if num_unique_values / num_total_values < 0.5:
            converted_obj.loc[:, col] = df_obj[col].astype('category')
        else:
            converted_obj.loc[:, col] = df_obj[col]

    optimized_df[converted_obj.columns] = converted_obj

    print(f'Optimized size: {mem_usage(optimized_df)}')

    dtypes = optimized_df.drop('MissionDate', axis=1).dtypes

    dtypes_col = dtypes.index
    dtypes_type = [i.name for i in dtypes.values]

    column_types = dict(zip(dtypes_col, dtypes_type))

    with open(args.output, 'w') as outfile:
        yaml.dump(column_types, outfile, default_flow_style=False)

# END.
