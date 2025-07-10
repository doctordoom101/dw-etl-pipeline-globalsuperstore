from db_config import get_engine
from extract import extract_csv
from transform.date import generate_date_dimension
from transform.dimension import transform_customer, transform_product, transform_geography, transform_order
from transform.fact import transform_fact
from load import load_dataframe

import pandas as pd

# Load data
df = extract_csv('data/global_superstore.csv')

# Rename columns
df.rename(columns={
    'Customer.ID': 'customer_id',
    'Customer.Name': 'customer_name',
    'Segment': 'segment',
    'Product.ID': 'product_id',
    'Product.Name': 'product_name',
    'Category': 'category',
    'Sub.Category': 'sub_category',
    'Country': 'country',
    'Region': 'region',
    'State': 'state',
    'City': 'city',
    'Market': 'market',
    'Market2': 'market2',
    'Order.Date': 'full_date',
    # 'Ship.Date': 'ship_date',
    'Year': 'year',
    'weeknum': 'week_of_year',
    'Order.ID': 'order_id',
    'Order.Priority': 'order_priority',
    'Ship.Mode': 'ship_mode',
    'Sales': 'sales',
    'Quantity': 'quantity',
    'Discount': 'discount',
    'Profit': 'profit',
    'Shipping.Cost': 'shipping_cost',
    'Row.ID': 'fact_sales_id'
}, inplace=True)

df['full_date'] = pd.to_datetime(df['full_date'])
# df['ship_date'] = pd.to_datetime(df['ship_date'])

# Transform dimensions
dim_customer = transform_customer(df)
dim_product = transform_product(df)
dim_geo = transform_geography(df)
dim_order = transform_order(df)
dim_date = generate_date_dimension(df)

# Merge dimension keys
df = df.merge(dim_customer, on=['customer_id', 'customer_name', 'segment'], how='left')
df = df.merge(dim_product, on=['product_id', 'product_name', 'category', 'sub_category'], how='left')
df = df.merge(dim_geo, on=['country', 'region', 'state', 'city', 'market', 'market2'], how='left')
df = df.merge(dim_order, on=['order_id', 'order_priority', 'ship_mode'], how='left')

# Merge date keys for both order_date and ship_date
df = df.merge(dim_date[['date_key', 'full_date']], on='full_date', how='left')
# df = df.merge(dim_date[['date_key', 'full_date']], left_on='ship_date', right_on='full_date', how='left', suffixes=('', '_ship'))
# df.rename(columns={'date_key_ship': 'ship_date_key'}, inplace=True)

# Create fact table with all required columns
fact = df[['fact_sales_id', 'customer_key', 'product_key', 'date_key',  
           'geography_key', 'order_key', 'sales', 'quantity', 'discount', 'profit', 
           'shipping_cost']].copy()

# Transform fact table (adds calculated columns)
fact = transform_fact(fact)

# Load dimensions first
engine = get_engine()
print("Loading dimension tables...")
load_dataframe(dim_customer, 'dim_customer', engine)
load_dataframe(dim_product, 'dim_product', engine)
load_dataframe(dim_geo, 'dim_geography', engine)
load_dataframe(dim_order, 'dim_order', engine)
load_dataframe(dim_date, 'dim_date', engine)

# Load fact table last
print("Loading fact table...")
load_dataframe(fact, 'fact_sales', engine)

print("✅ ETL Process Completed")