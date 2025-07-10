from sqlalchemy import create_engine

def get_engine():
    return create_engine(
        "postgresql+psycopg2://postgres:postgres@localhost:5432/dw_global_superstore",
        echo=False  # matikan logging SQL
    )
