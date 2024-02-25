import pandas as pd

df = pd.read_csv("/home/sonin/Downloads/sport data - bars.csv")

def proc(row):
    formula = row['formula']
    # print(formula)
    total_weight = 0
    if pd.isna(formula):
        return
    if '+' in formula:
        for set in formula.split(' + '):
            sets, reps = map(int, set.split("*"))
            total_weight += sets*reps
    else:
        sets, reps = map(int, formula.split("*"))
        total_weight = sets*reps
    
    return total_weight

df['tw'] = df.apply(proc, axis=1)
# df.to_csv('lalala.csv')

df = df[df["type"] == 'pull_ups'][['type', 'tw']]
print(df)
print(df.tw.sum())

