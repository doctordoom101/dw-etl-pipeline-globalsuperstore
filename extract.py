import pandas as pd

def extract_csv(path):
    df = pd.read_csv(path, encoding='utf-8')
    return df
