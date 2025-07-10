import pandas as pd
import datetime as dt

def transform_customer(df):
    dim = df[['customer_id', 'customer_name', 'segment']].drop_duplicates()
    dim['customer_key'] = range(1, len(dim)+1)
    dim['effective_date'] = dt.date.today()
    dim['expiry_date'] = None
    dim['is_current'] = True
    return dim

def transform_product(df):
    dim = df[['product_id', 'product_name', 'category', 'sub_category']].drop_duplicates()
    dim['product_key'] = range(1, len(dim)+1)
    
    # Add category and sub_category IDs (simple enumeration)
    category_mapping = {cat: idx for idx, cat in enumerate(dim['category'].unique(), 1)}
    sub_category_mapping = {sub_cat: idx for idx, sub_cat in enumerate(dim['sub_category'].unique(), 1)}
    
    dim['category_id'] = dim['category'].map(category_mapping)
    dim['sub_category_id'] = dim['sub_category'].map(sub_category_mapping)
    
    # SCD Type 2 fields
    dim['effective_date'] = dt.date.today()
    dim['expiry_date'] = None
    dim['is_current'] = True
    
    return dim

def transform_geography(df):
    dim = df[['country', 'region', 'state', 'city', 'market', 'market2']].drop_duplicates()
    dim['geography_key'] = range(1, len(dim)+1)
    return dim

def transform_order(df):
    dim = df[['order_id', 'order_priority', 'ship_mode']].drop_duplicates()
    dim['order_key'] = range(1, len(dim)+1)
    
    # Add priority_rank based on order_priority
    priority_mapping = {
        'High': 1,
        'Medium': 2,
        'Low': 3,
        'Critical': 1,
        'Not Specified': 4
    }
    dim['priority_rank'] = dim['order_priority'].map(priority_mapping).fillna(4)
    
    # Add ship_mode_category based on ship_mode
    def categorize_ship_mode(ship_mode):
        if ship_mode in ['Same Day', 'First Class']:
            return 'Express'
        elif ship_mode in ['Second Class', 'Standard Class']:
            return 'Standard'
        else:
            return 'Other'
    
    dim['ship_mode_category'] = dim['ship_mode'].apply(categorize_ship_mode)
    
    # SCD Type 2 fields
    dim['effective_date'] = dt.date.today()
    dim['expiry_date'] = None
    dim['is_current'] = True
    
    return dim