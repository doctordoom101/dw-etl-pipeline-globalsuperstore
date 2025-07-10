import numpy as np

def transform_fact(df):
    # Calculate gross_sales (handle division by zero)
    df['gross_sales'] = df.apply(
        lambda row: row['sales'] / (1 - row['discount']) if row['discount'] != 1 else row['sales'],
        axis=1
    ).round(2)
    
    # Calculate profit_margin (handle division by zero)
    df['profit_margin'] = df.apply(
        lambda row: row['profit'] / row['sales'] if row['sales'] != 0 else 0,
        axis=1
    ).round(4)

    # Round other numeric columns
    df['sales'] = df['sales'].round(2)
    df['discount'] = df['discount'].round(4)
    df['profit'] = df['profit'].round(2)
    df['shipping_cost'] = df['shipping_cost'].round(2)

    # Handle inf and NaN values
    df.replace([np.inf, -np.inf], 0, inplace=True)
    df.fillna(0, inplace=True)

    return df