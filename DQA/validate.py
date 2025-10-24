import dask.dataframe as dd
import re
import pandas as pd

def check_not_null(ddf, column):
    missing = ddf[column].isnull().sum().compute()
    return missing

def check_unique(ddf, column):
    # Count duplicates manually
    counts = ddf.groupby(column)[column].count()
    duplicates = counts[counts > 1].sum().compute()
    return duplicates

def check_range(ddf, column, min_val, max_val):
    invalid = ddf[(ddf[column] < min_val) | (ddf[column] > max_val)][column].count().compute()
    return invalid

def check_regex(ddf, column, pattern):
    invalid = ddf[~ddf[column].str.match(pattern, na=False)][column].count().compute()
    return invalid

def run_validations(ddf, table_name, table_rules, rules_config):
    results = []
    for column, checks in table_rules.items():
        for check in checks:
            if check == "not_null":
                res = check_not_null(ddf, column)
                results.append((column, check, res))
            elif check == "unique":
                res = check_unique(ddf, column)
                results.append((column, check, res))
            elif check == "range":
                min_val, max_val = rules_config["ranges"][column]
                res = check_range(ddf, column, min_val, max_val)
                results.append((column, check, res))
            elif check == "regex":
                pattern = rules_config["regex_patterns"][column]
                res = check_regex(ddf, column, pattern)
                results.append((column, check, res))
    return results
