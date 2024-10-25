# Data Cleaning Project: Population Dataset

## 1. Initial State Analysis

### Dataset Overview
- **Name**: messy_population_data.csv
- **Rows**: 125718
- **Columns**: 5

### Column Details
#### Numerical
| Column Name      | Data Type | Non-Null Count | # of Unique Values |  Mean/range  |
|------------------|-----------|----------------|--------------------|--------------|
| [age]            | [float64] | [119495]       | [101]              | [50]         |
| [year]           | [float64] | [119516]       | [169]              | [1950-2119]  |
| [population]     | [float64] | [119378]       | [114925]           | [119378]     |

#### Categorical
| Column Name      | Data Type | Non-Null Count | Unique Values               |  Proportion  |
|------------------|-----------|----------------|-----------------------------|--------------|
| [income_groups]  | [object]  | [119412]       | [8]                         |              |
|                  |           |                | [low_income]                | [23.82%]     |
|                  |           |                | [upper_middle_income]       | [23.74%]     |
|                  |           |                | [high_income]               | [23.74%]     |
|                  |           |                | [lower_middle_income]       | [23.72%]     |
|                  |           |                | [lower_middle_income_typo]  | [1.27%]      |
|                  |           |                | [low_income_typo]           | [1.26%]      |
|                  |           |                | [high_income_typo]          | [1.24%]      |
|                  |           |                | [upper_middle_income_typo]  | [1.22%]      |
| [gender]         | [float64] | [119811]       | [3]                         |              |
|                  |           |                | [1]                         | [47.39%]     |
|                  |           |                | [2]                         | [47.36%]     |
|                  |           |                | [3]                         | [5.25%]      |



### Identified Issues

1. **Missing Values**
   - Description: Columns have missing values.
   - Affected Column(s): `income_groups, age, gender, year, population`
   - Example: income_groups has 6306 missing values.
   - Potential Impact: Missing data can lead to over/underestimation of various metrics and can introduce computational challenges.

2. **Future Dates**
   - Description: 60211 rows have future year values in the `[year]` column.
   - Affected Column(s): `year`
   - Example: The year 2119 exists in the `year` column.
   - Potential Impact: Including future years can impact temporal calcuations and time series analysis as future values can lead to overfitting or inaccurate predictions.

3. **Outliers**
   - Description: After calculating the IQR and the upper/lower bounds, there are 2252 outliers in the `population` column.
   - Affected Column(s): `population`
   - Example: The upper bound of `population` is 33185676.75, but there is a data point with a value of 5642672000, which is much higher than this upper bound.
   - Potential Impact: Outliers may skew averages and thus influence the variance/standard deviation, can make it difficult to determine underlying trends in the dataset, and can inflate/deflate test statistics which would lead to more false positives or negatives.

4. **Duplicates**
   - Description: 2950 duplicates rows exist in the dataset.
   - Affected Column(s): `income_groups, age, gender, year, population`
   - Example: Row index 138 is duplicated again at row index 124472. 
   - Potential Impact: Duplicates inflate the sample size, which can affect the validity of confidence intervals and hypothesis tests. Duplicates may also lead to an over/underestimation of the mean and also lead to an inaccurate distribution of the data. This can also lead to overfitting if a model is created, leading to flawed insights.

5. **Incorrect Column Types**
   - Description: Columns of a certain data type might be better stored as a different data type.
   - Affected Column(s): `income_groups, gender`
   - Example: The `gender` column would be better stored as a category or int column but is of float64 type.
   - Potential Impact: Categorical data stored as strings or integers might cause inconsistent grouping which would affect analyses such as frequency counts or aggregations. It also makes it difficult to conduct modeling as they might require data in specific formats, leading to errors or poor model performance. Additionally, there might be errors when filtering or comparisons are done.

6. **Inconsistent Categorical Values**
   - Description: Some columns have inconsistent categorical values, such as typos or new categories.
   - Affected Column(s): `income_groups, gender`
   - Example: The `income_groups` column has categorical values such as `lower_middle_income_typo`.
   - Potential Impact: Inconsistent data can lead to incorrect grouping/classification and can unnecessarily increase the complexity of downstream analyses as more time will need to be spent cleaning and standardizing the data. Additionally, categorical variables being split into too many levels/categories can reduce the statistical power of certain tests, making it more difficult to detect significant effects or relationships between variables. 




## 2. Data Cleaning Process

### Issue 1: Missing Values
- **Cleaning Method**: Missing values will be detected and rows with missing values will be imputed with either an "unknown" value (categorical variables) or the median. Missing values in the `year` column will be dropped.
- **Implementation**:
  ```python
  def clean_missing_values(df):
    df = df.dropna(subset=['year'])

    # imputing missing values for categorical columns with "unknown"
    categorical_columns = df.select_dtypes(include='object').columns
    df.loc[:, categorical_columns] = df[categorical_columns].fillna("unknown")

    # imputing missing values for numerical columns with the median
    numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns
    for col in numerical_columns:
        median_value = df[col].median()
        df.loc[:, col] = df[col].fillna(median_value)
  ```
- **Justification**: 28079 rows have at least 1 NA, which is ~22% of our total number of rows. I would consider this too high to be dropping missing values, so in order to preserve as much data as possible, I'll be imputing data. If <5% of rows were NA, I would consider dropping instead. Categorical variables are imputed as "unknown" as a placeholder value while numerical variables are imputed with their median as it is the least affected by outlier values. NA values in the `year` column are dropped as <5% of these rows are NA, and it would not make sense to impute these values as another number (as it could significantly affect temporal or time series analyses) or a placeholder value like "unknown" (as it does not match the column type and would make any temporal or time series analyses very difficult).
- **Impact**: 
  - Rows affected: [28079]
  - Data distribution change: There are no more missing values. 6202 rows were dropped, so now the total number of rows is 119516. Summary statistics for the numerical variables may change due to imputation with median values.

### Issue 2: Future Dates
- **Cleaning Method**: Rows with future year values will be filtered out from the dataset.
- **Implementation**:
  ```python
  def clean_missing_values(df):
    df = df[df['year'] <= 2024]
  ```
- **Justification**: 60211 rows have a future year value, which makes up for ~47.9% of our total number of rows. Because this is a rather large proportion, imputing these values might significantly change underlying distribution and trends. As we are still in the exploratory data analysis stage, I would simply filter out these rows in order to look at the current temporal data and would revisit the data once a better understanding of future analysis goals with the dataset is understood.
- **Impact**: 
  - Rows affected: [60211]
  - Data distribution change: The number of rows went down to 59305 and the maximum year value is 2024. 

### Issue 3: Outliers
- **Cleaning Method**: Outliers in the `population` column will be log transformed.
- **Implementation**:
  ```python
  df['population'] = np.log1p(df['population'])
  ```
- **Justification**: Rather than dropping outliers, which might still hold important information, these values are log transformed instead to minimize the impact of these values on the distribution. 
- **Impact**: 
  - Rows affected: [59305]
  - Data distribution change: The number of rows have stayed the same but after checking the KDE plot for `population`, the distribution looks a lot more normal.

### Issue 4: Duplicates
- **Cleaning Method**: Duplicate rows will be dropped.
- **Implementation**:
  ```python
  dropped_duplicates = df.drop_duplicates()
  ```
- **Justification**: Duplicate rows are dropped in order to prevent redundant data as it unnecessarily inflates the dataset and can slow down downstream analyses. 
- **Impact**: 
  - Rows affected: [1355]
  - Data distribution change: After previous data cleaning steps, 1355 rows are dropped. Since duplicate values were dropped, summary statistics may have changed. 

### Issue 5: Incorrect Column Types
- **Cleaning Method**: Duplicate rows will be dropped.
- **Implementation**:
  ```python
  dropped_duplicates = df.drop_duplicates()
  ```
- **Justification**: Duplicate rows are dropped in order to prevent redundant data as it unnecessarily inflates the dataset and can slow down downstream analyses. 
- **Impact**: 
  - Rows affected: []
  - Data distribution change: . 

### Issue 6: Inconsistent Categorical Values
- **Cleaning Method**: Duplicate rows will be dropped.
- **Implementation**:
  ```python
  dropped_duplicates = df.drop_duplicates()
  ```
- **Justification**: Duplicate rows are dropped in order to prevent redundant data as it unnecessarily inflates the dataset and can slow down downstream analyses. 
- **Impact**: 
  - Rows affected: []
  - Data distribution change: . 



## 3. Final State Analysis

### Dataset Overview
- **Name**: cleaned_population_data.csv (or whatever you named it)
- **Rows**: [Your answer]
- **Columns**: [Your answer]

### Column Details
| Column Name | Data Type | Non-Null Count | #Unique Values |  Mean  |
|-------------|-----------|----------------|----------------|--------|
| [Column 1]  | [Type]    | [Count]        | [#Unique]      | [Mean] |
| ...         | ...       | ...            | ...            | ...    |

### Summary of Changes
- [List major changes made to the dataset]
- [Discuss any significant changes in data distribution]
