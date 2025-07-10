-- FACT TABLE
CREATE TABLE FACT_SALES (
    fact_sales_id BIGINT PRIMARY KEY,
    
    -- Foreign Keys ke Dimensi
    customer_key INT NOT NULL,
    product_key INT NOT NULL,
    date_key INT NOT NULL,
    geography_key INT NOT NULL,
    order_key INT NOT NULL,
    
    -- Measures (Metrik Bisnis)
    sales DECIMAL(15,2) NOT NULL,
    quantity INT NOT NULL,
    discount DECIMAL(5,4) NOT NULL,
    profit DECIMAL(15,2) NOT NULL,
    shipping_cost DECIMAL(10,2) NOT NULL,
    
    -- Calculated Measures
    gross_sales DECIMAL(15,2) NOT NULL, -- sales / (1 - discount)
    profit_margin DECIMAL(5,4) NOT NULL, -- profit / sales
    
    -- Metadata
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- DIM TABLE
CREATE TABLE DIM_CUSTOMER (
    customer_key INT PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    customer_name VARCHAR(255) NOT NULL,
    segment VARCHAR(50) NOT NULL,
    
    -- SCD Type 2 fields
    effective_date DATE NOT NULL,
    expiry_date DATE,
    is_current BOOLEAN DEFAULT TRUE,
    
    -- Metadata
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE DIM_PRODUCT (
    product_key INT PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL,
    product_name VARCHAR(500) NOT NULL,
    category VARCHAR(100) NOT NULL,
    sub_category VARCHAR(100) NOT NULL,
    
    -- Product Hierarchy
    category_id INT,
    sub_category_id INT,
    
    -- SCD Type 2 fields
    effective_date DATE NOT NULL,
    expiry_date DATE,
    is_current BOOLEAN DEFAULT TRUE,
    
    -- Metadata
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE DIM_GEOGRAPHY (
    geography_key INT PRIMARY KEY,
    
    -- Geographic Hierarchy
    country VARCHAR(100) NOT NULL,
    region VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    market VARCHAR(100) NOT NULL,
    market2 VARCHAR(100), -- market tambahan jika ada
    
    -- Geographic Hierarchy IDs
    country_id INT,
    region_id INT,
    state_id INT,
    city_id INT,
    market_id INT,
    
    -- Metadata
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE DIM_DATE (
    date_key INT PRIMARY KEY, -- Format: YYYYMMDD
    full_date DATE NOT NULL,
--     ship_date DATE NOT NULL,
    
    -- Date Attributes
    day_of_week INT NOT NULL,
    day_of_month INT NOT NULL,
    day_of_year INT NOT NULL,
    week_of_year INT NOT NULL,
    month_number INT NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    quarter INT NOT NULL,
    year INT NOT NULL,
    
    -- Formatted Dates
    day_name VARCHAR(20) NOT NULL,
    month_year VARCHAR(20) NOT NULL,
    quarter_year VARCHAR(20) NOT NULL,
    
    -- Business Attributes
    is_weekend BOOLEAN NOT NULL,
    is_holiday BOOLEAN DEFAULT FALSE,
    fiscal_year INT,
    fiscal_quarter INT,
    
    -- Metadata
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE DIM_ORDER (
    order_key INT PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL,
    order_priority VARCHAR(50) NOT NULL,
    ship_mode VARCHAR(100) NOT NULL,
    
    -- Order Attributes
    priority_rank INT, -- 1=High, 2=Medium, 3=Low, 4=Not Specified
    ship_mode_category VARCHAR(50), -- Same Day, Express, Standard, etc.
    
    -- SCD Type 2 fields
    effective_date DATE NOT NULL,
    expiry_date DATE,
    is_current BOOLEAN DEFAULT TRUE,
    
    -- Metadata
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

