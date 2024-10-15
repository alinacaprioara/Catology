import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder


df = pd.read_excel('data.xlsx', engine='openpyxl')

file_path = 'data.xlsx'
xls = pd.ExcelFile(file_path)

sheet_names = xls.sheet_names
print(sheet_names)

data_df = pd.read_excel(xls, sheet_name='Data')

data_df_head = data_df.head()

duplicate_rows = data_df.duplicated().sum()
missing_values = data_df.isnull().sum()

df = df.drop_duplicates()
#df = df = df.fillna(df.mean()) //nu poti face media coloanelor in cazul in care is nule, pt ca ai si valori non numerice

race_counts = data_df['Race'].value_counts()

print("Columns with no value:\n", missing_values)
print("Number of duplicates:\n", duplicate_rows)
print("Number of instances per class (Race):\n", race_counts)

print("\nDistinct values and frequencies for each attribute:\n")
for column in data_df.columns:
    unique_values = data_df[column].value_counts()
    print(f"Column: {column}")
    print(unique_values)
    print(f"Total distinct values in {column}: {len(unique_values)}\n")

print("Data types of columns:\n", data_df.dtypes)

label_encoder = LabelEncoder()
data_df['Sexe'] = label_encoder.fit_transform(data_df['Sexe'])
data_df['Race'] = label_encoder.fit_transform(data_df['Race'])
data_df['Logement'] = label_encoder.fit_transform(data_df['Logement'])

print("Data types of columns:\n", data_df.dtypes)

sns.set_theme(style="whitegrid")

numeric_columns = data_df.select_dtypes(include=['number']).columns
for column in numeric_columns:
    plt.figure(figsize=(10, 4))
    sns.histplot(data_df[column], bins=20, kde=True)
    plt.title(f'Value distribution for: {column}')
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.show()

for column in numeric_columns:
    plt.figure(figsize=(10, 4))
    sns.boxplot(x=data_df[column])
    plt.title(f'Boxplot for {column}')
    plt.xlabel(column)
    plt.show()

#
# if data_df.select_dtypes(include=[float, int]).shape[1] > 0:
#     correlation_matrix = data_df.corr()
#     print("Correlation matrix between numerical attributes:\n", correlation_matrix)
# else:
#     print("No numerical attributes found for correlation analysis.")