import pandas as pd
import numpy as np

def ABC(percentage):
    if percentage > 0 and percentage < 70:
        return 'A'
    elif percentage >= 70 and percentage < 90:
        return 'B'
    elif percentage >= 90:
        return 'C'

def prep(df):
    df['TotalC'] = df['Annual Demand'] * df['Unit price']
    Stotal = df['TotalC'].sum()
    df['DPercentage'] = (1/len(df)) * 100
    df['CPercentage'] = (df['TotalC']/Stotal) * 100
    df.sort_values(by = ['CPercentage'], ascending = False, inplace = True)
    df['CummulativeCP'] = df['CPercentage'].cumsum()
    df['CummulativeDP'] = df['DPercentage'].cumsum()
    df['Class'] = df['CummulativeCP'].apply(ABC)
    return df, Stotal
    
    
def summary(df, Stotal):
    cls = ['A', 'B', 'C']
    temp = []
    for i in cls:
        temp.append(i)
        temp.append(df[df.Class == i]['TotalC'].sum())
        temp.append((df[df.Class == i]['TotalC'].sum()/Stotal) * 100)
        temp.append(df.Class.value_counts()[i])
        temp.append(df.Class.value_counts()[i]/len(df) * 100)
    return temp


df = pd.read_csv('data/inventory.csv')
agg = {'Item-code': 'first', 'Annual Demand': 'sum', 'Unit price': 'first'}
df = df.groupby(df['Item-code']).aggregate(agg)
df, Stotal = prep(df)
data = np.array(summary(df,Stotal))
summary = pd.DataFrame(np.array_split(data, 3), columns=['Class', 'Total Cost', 'Cost Percentage', 'Frequency', 'Share Percentage'])
df.reset_index(drop = True, inplace = True)
df.to_csv('result/complete.csv', index = False)
summary.to_csv('result/summary.csv', index = False)