import pandas as pd


data = pd.read_excel("internship_data.xlsx", sheet_name='Sheet1')



# print(data.head(10))
# data.head(10)
# data.describe()
# data.info()

for col, val in data.items():
    if col == 'digital_id':
        print(type(val) )

