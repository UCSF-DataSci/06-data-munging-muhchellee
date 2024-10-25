"""
This is a script does the following to clean the messy_population.csv file:
    - Imputes missing values
    - 
"""
import pandas as pd
import numpy as np
from numpy.random import default_rng
import argparse
from tqdm import tqdm
import warnings

# default input and output filenames
DEFAULT_INPUT_FILE = 'messy_population_data.csv'
DEFAULT_OUTPUT_FILE = 'cleaned_population_data.csv'

def load_data(file_path):
    """load the original clean dataset"""
    return pd.read_csv(file_path)

def clean_missing_values(df):
    """handles missing values"""
    # dropping rows where year is NA
    df = df.dropna(subset=['year'])

    # imputing missing values for categorical columns with "unknown"
    categorical_columns = df.select_dtypes(include='object').columns
    df.loc[:, categorical_columns] = df[categorical_columns].fillna("unknown")

    # imputing missing values for numerical columns with the median
    numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns
    for col in numerical_columns:
        median_value = df[col].median()
        df.loc[:, col] = df[col].fillna(median_value)
    
    return df

def filter_future_years(df):
    """filters out future year values"""
    df = df[df['year'] <= 2024]

    return df

def log_transform_outliers(df, column_name):
    """log transforms outliers"""
    # using np.log1p to handle zero values (log(1 + x)), as log(0) is undefined
    if column_name in df.columns:
        df[column_name] = np.log1p(df[column_name])
    else:
        print(f"Column '{column_name}' does not exist in the DataFrame.")
    
    return df

def drop_duplicate_rows(df):
    """drops duplicate rows if they exist"""
    init_row_count = df.shape[0]
    dropped_duplicates = df.drop_duplicates()
    final_row_count = dropped_duplicates.shape[0]

    num_duplicates = init_row_count - final_row_count
    if num_duplicates > 0:
        print(f"{num_duplicates} duplicate rows removed.")
    else:
        print("No duplicate rows found.")

    return dropped_duplicates

def convert_to_categorical(df, columns):
    """converts specified columns in a df to categorical type"""
    for col in columns:
        try:
            if col in df.columns:
                # check if the column is already a category
                if isinstance(df[col].dtype, pd.CategoricalDtype):
                    warnings.warn(f"Column '{col}' is already of type 'category'.")
                else:
                    # convert to categorical
                    df[col] = df[col].astype('category')
            else:
                raise ValueError(f"Column '{col}' not found in DataFrame.")
        except Exception as e:
            print(f"Error processing column '{col}': {e}")
    
    return df

