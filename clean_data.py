"""
This is a script that cleans the messy_population.csv file.
"""
import pandas as pd
import numpy as np
from numpy.random import default_rng
import argparse
from tqdm import tqdm
import warnings

## reading file ##
df = pd.read_csv('messy_population_data.csv')


## cleaning missing values ##
cleaned_df = df.dropna(subset=['year'])

# imputing missing values for categorical columns with "unknown"
categorical_columns = cleaned_df.select_dtypes(include='object').columns
cleaned_df.loc[:, categorical_columns] = df[categorical_columns].fillna("unknown")

# imputing missing values for numerical columns with the median
numerical_columns = cleaned_df.select_dtypes(include=['float64', 'int64']).columns
for col in numerical_columns:
    median_value = cleaned_df[col].median()
    cleaned_df.loc[:, col] = cleaned_df[col].fillna(median_value)
    

## filtering out future year values ##
cleaned_df = cleaned_df[cleaned_df['year'] <= 2024]


## log transforming population outliers ##
cleaned_df.loc[:, 'population'] = np.log1p(cleaned_df['population'])


## dropping duplicate rows ##
cleaned_df = cleaned_df.drop_duplicates()


## changing income_groups and gender to category type ##
cleaned_df.loc[:, 'gender'] = cleaned_df['gender'].astype('int')
cleaned_df.loc[:, 'income_groups'] = cleaned_df['income_groups'].astype('category')


## changing inconsistent category types ##
income_replacements = {
    "low_income_typo": "low_income",
    "upper_middle_income_typo": "upper_middle_income",
    "high_income_typo": "high_income",
    "lower_middle_income_typo": "lower_middle_income",
}
    
# replacing 3 in gender with 9
cleaned_df.loc[:, 'gender'] = cleaned_df['gender'].replace(3, 9)

# replacing values in 'income_groups' column
cleaned_df.loc[:, 'income_groups'] = cleaned_df['income_groups'].replace(income_replacements)
    
# consolidating income_groups
cleaned_df.loc[:, 'income_groups'] = cleaned_df['income_groups'].replace({
    "low_income": "low_income",
    "upper_middle_income": "upper_middle_income",
    "high_income": "high_income",
    "lower_middle_income": "lower_middle_income"
})


## saving cleaned file ##
output_file = 'clean_population_data.csv'
cleaned_df.to_csv(output_file, index=False)
print(f"\nClean dataset saved as '{output_file}'")

## printing out data summaries ##
print(cleaned_df.info())
print(cleaned_df.describe())
unique_counts = cleaned_df.nunique()
print(unique_counts)

# income group proportion
income_group_proportion = cleaned_df['income_groups'].value_counts(normalize=True) * 100
print("Proportion of income_groups:")
print(income_group_proportion)

# gender proportion
gender_proportion = cleaned_df['gender'].value_counts(normalize=True) * 100
print("\nProportion of gender:")
print(gender_proportion)