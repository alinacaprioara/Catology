import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from deep_translator import GoogleTranslator



df = pd.read_excel('data.xlsx', engine='openpyxl')

file_path = 'data.xlsx'
xls = pd.ExcelFile(file_path)

sheet_names = xls.sheet_names
print(sheet_names)

data_df = pd.read_excel(xls, sheet_name='Data')

data_df_head = data_df.head()
def translate_column(column):
    translator = GoogleTranslator(source='fr', target='en')
    return column.apply(lambda x: translator.translate(str(x)))
#translated_df = data_df.apply(translate_column) // nu imi dau seama daca il folosesc gresit sau sunt atat de multe date incat dureaza
filtered_columns = data_df.drop(columns=["Row.names", "Plus"])
duplicate_rows = filtered_columns.duplicated().sum()
missing_values = filtered_columns.isnull().sum()

df = df.drop_duplicates()
label_encoder = LabelEncoder()
non_numeric_columns = df.select_dtypes(include=['object']).columns

for col in non_numeric_columns:
    df[col] = label_encoder.fit_transform(df[col].astype(str))
df = df = df.fillna(df.mean())
#nu poti face media coloanelor in cazul in care is nule, pt ca ai si valori non numerice MERGE ACUM

race_counts = data_df['Race'].value_counts()

print("Columns with no value:\n", missing_values)
print("Number of duplicates:\n", duplicate_rows)
print("Number of instances per class (Race):\n", race_counts)

print("\nDistinct values and frequencies for each attribute:\n")
for column in data_df.columns:
    if column not in ["Row.names", "Plus"]:
        unique_values = data_df[column].value_counts()
        print(f"Column: {column}")
        print(unique_values)
        print(f"Total distinct values in {column}: {len(unique_values)}\n")

print("Data types of columns:\n", data_df.dtypes)

data_df['Sexe'] = label_encoder.fit_transform(data_df['Sexe'])
data_df['Race'] = label_encoder.fit_transform(data_df['Race'])
data_df['Logement'] = label_encoder.fit_transform(data_df['Logement'])

df_corr = df.drop(columns=["Row.names", "Plus"])
print("Data types of columns:\n", data_df.dtypes)
#corelatii
correlation_matrix = df_corr.corr()


plt.figure(figsize=(16, 12))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f",  linewidths=0.5, cbar_kws={"shrink": 0.8})
plt.title('Matricea de corelatie între atribute', size=18)
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.show()
#gata corelatii
sns.set_theme(style="whitegrid")

numeric_columns = [col for col in data_df.select_dtypes(include=['number']).columns if col not in ["Row.names", "Plus"]]
column_index = 0
show_histogram = True
show_boxplot = False
def plot_next():
    global column_index, show_histogram, canvas
    if column_index < len(numeric_columns):
        column = numeric_columns[column_index]

        for widget in plot_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(10, 6))

        if show_histogram:
            sns.histplot(df[column], bins=20, kde=True, ax=ax)
            ax.set_title(f'Histogram for: ')
            ax.set_xlabel(column)
            ax.set_ylabel('Frequency')
            show_histogram = False
            show_boxplot = True
        else:
            sns.boxplot(x=df[column], ax=ax)
            ax.set_title(f'Boxplot for: ')
            ax.set_xlabel(column)
            show_boxplot = False
            show_histogram = True
            column_index += 1


        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()


    else:
        messagebox.showinfo("End", "No more columns to display.")
        root.quit()

root = tk.Tk()
root.title("Navigator")

plot_frame = tk.Frame(root)
plot_frame.pack(pady=20)

next_button = tk.Button(root, text="Next", command=plot_next)
next_button.pack(pady=10)

plot_next()

root.mainloop()
#
# if data_df.select_dtypes(include=[float, int]).shape[1] > 0:
#     correlation_matrix = data_df.corr()
#     print("Correlation matrix between numerical attributes:\n", correlation_matrix)
# else:
#     print("No numerical attributes found for correlation analysis.")