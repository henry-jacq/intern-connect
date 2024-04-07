import pandas as pd

excel_file = 'internconnect/internship_data.xlsx'
df = pd.read_excel(excel_file)
for index, row in df.iterrows():
    print(row)