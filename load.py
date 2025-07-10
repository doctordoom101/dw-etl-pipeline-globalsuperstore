def load_dataframe(df, table_name, engine, if_exists='append'):
    try:
        print(f"Loading: {table_name}...")
        df.to_sql(table_name, engine, if_exists=if_exists, index=False, method='multi')
        print(f"✅ Loaded: {table_name}")
    except Exception as e:
        print(f"❌ Error loading {table_name}: {e}")
