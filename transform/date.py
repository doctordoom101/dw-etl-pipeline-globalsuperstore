import pandas as pd

def generate_date_dimension(df):
    # Get all unique dates from both order_date and ship_date
    order_dates = df[['full_date', 'year', 'week_of_year']].rename(columns={'full_date': 'date'})
    # ship_dates = df[['ship_date', 'year', 'week_of_year']].rename(columns={'ship_date': 'date'})
    
    # Combine and get unique dates
    all_dates = pd.concat([order_dates], ignore_index=True)
    all_dates = all_dates.drop_duplicates(subset=['date'])
    
    # Convert to datetime
    all_dates['date'] = pd.to_datetime(all_dates['date'])
    
    # Create date_key
    all_dates['date_key'] = all_dates['date'].dt.strftime('%Y%m%d').astype(int)
    
    # Add date attributes
    all_dates['full_date'] = all_dates['date']
    all_dates['day_of_week'] = all_dates['date'].dt.weekday + 1
    all_dates['day_of_month'] = all_dates['date'].dt.day
    all_dates['day_of_year'] = all_dates['date'].dt.dayofyear
    all_dates['month_number'] = all_dates['date'].dt.month
    all_dates['month_name'] = all_dates['date'].dt.strftime('%B')
    all_dates['quarter'] = all_dates['date'].dt.quarter
    all_dates['day_name'] = all_dates['date'].dt.strftime('%A')
    all_dates['month_year'] = all_dates['date'].dt.strftime('%Y-%m')
    all_dates['quarter_year'] = all_dates['date'].dt.to_period('Q').astype(str)
    all_dates['is_weekend'] = all_dates['day_of_week'] >= 6
    all_dates['fiscal_year'] = all_dates['year']
    all_dates['fiscal_quarter'] = all_dates['quarter']
    
    # Remove temporary date column
    all_dates = all_dates.drop('date', axis=1)
    
    return all_dates