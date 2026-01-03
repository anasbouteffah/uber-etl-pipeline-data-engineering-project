import pandas as pd
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer

@transformer
def transform(df, *args, **kwargs):
    # --- 1. CONVERT DATE COLUMNS ---
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
    
    # --- 2. CLEANING (Based on your Notebook) ---
    # Remove duplicates first
    df = df.drop_duplicates().reset_index(drop=True)
    
    # Filter 1: Remove trips with 0 passengers
    df = df[df['passenger_count'] > 0]
    
    # Filter 2: Remove trips with 0 distance
    df = df[df['trip_distance'] > 0]
    
    # Filter 3: Remove trips with 0 or negative total amount
    df = df[df['total_amount'] > 0]
    
    # --- 3. CREATE TRIP ID ---
    # We reset the index AFTER cleaning so trip_ids are sequential (0, 1, 2...)
    df = df.reset_index(drop=True)
    df['trip_id'] = df.index

    # --- 4. DATETIME DIMENSION ---
    datetime_dim = df[['tpep_pickup_datetime', 'tpep_dropoff_datetime']].drop_duplicates().reset_index(drop=True)
    datetime_dim['datetime_id'] = datetime_dim.index
    
    # Extract Pickup features
    datetime_dim['pick_hour'] = datetime_dim['tpep_pickup_datetime'].dt.hour
    datetime_dim['pick_day'] = datetime_dim['tpep_pickup_datetime'].dt.day
    datetime_dim['pick_month'] = datetime_dim['tpep_pickup_datetime'].dt.month
    datetime_dim['pick_year'] = datetime_dim['tpep_pickup_datetime'].dt.year
    datetime_dim['pick_weekday'] = datetime_dim['tpep_pickup_datetime'].dt.weekday
    
    # Extract Dropoff features
    datetime_dim['drop_hour'] = datetime_dim['tpep_dropoff_datetime'].dt.hour
    datetime_dim['drop_day'] = datetime_dim['tpep_dropoff_datetime'].dt.day
    datetime_dim['drop_month'] = datetime_dim['tpep_dropoff_datetime'].dt.month
    datetime_dim['drop_year'] = datetime_dim['tpep_dropoff_datetime'].dt.year
    datetime_dim['drop_weekday'] = datetime_dim['tpep_dropoff_datetime'].dt.weekday
    
    datetime_dim = datetime_dim[['datetime_id', 'tpep_pickup_datetime', 'pick_hour', 'pick_day', 'pick_month', 'pick_year', 'pick_weekday',
                                 'tpep_dropoff_datetime', 'drop_hour', 'drop_day', 'drop_month', 'drop_year', 'drop_weekday']]

    # --- 5. RATE CODE DIMENSION ---
    rate_code_type = {
        1:"Standard rate", 2:"JFK", 3:"Newark", 4:"Nassau or Westchester", 5:"Negotiated fare", 6:"Group ride"
    }
    rate_code_dim = df[['RatecodeID']].drop_duplicates().reset_index(drop=True)
    rate_code_dim['rate_code_id'] = rate_code_dim.index
    rate_code_dim['rate_code_name'] = rate_code_dim['RatecodeID'].map(rate_code_type)
    rate_code_dim = rate_code_dim[['rate_code_id', 'RatecodeID', 'rate_code_name']]

    # --- 6. PAYMENT TYPE DIMENSION ---
    payment_type_name = {
        1:"Credit card", 2:"Cash", 3:"No charge", 4:"Dispute", 5:"Unknown", 6:"Voided trip"
    }
    payment_type_dim = df[['payment_type']].drop_duplicates().reset_index(drop=True)
    payment_type_dim['payment_type_id'] = payment_type_dim.index
    payment_type_dim['payment_type_name'] = payment_type_dim['payment_type'].map(payment_type_name)
    payment_type_dim = payment_type_dim[['payment_type_id', 'payment_type', 'payment_type_name']]

    # --- 7. VENDOR DIMENSION ---
    vendor_type = {1:"Creative Mobile Technologies", 2:"VeriFone Inc"}
    vendor_dim = df[['VendorID']].drop_duplicates().reset_index(drop=True)
    vendor_dim['vendor_id'] = vendor_dim.index
    vendor_dim['vendor_name'] = vendor_dim['VendorID'].map(vendor_type)
    vendor_dim = vendor_dim[['vendor_id', 'VendorID', 'vendor_name']]

    # --- 8. FACT TABLE ---
    fact_table = (
        df.merge(datetime_dim, on=['tpep_pickup_datetime', 'tpep_dropoff_datetime'])
          .merge(payment_type_dim, on='payment_type')
          .merge(rate_code_dim, on='RatecodeID')
          .merge(vendor_dim, on='VendorID')
    )

    # Select final columns (IDs + Measures + Locations)
    fact_table = fact_table[[
        'trip_id',
        'vendor_id',
        'datetime_id',
        'rate_code_id',
        'payment_type_id',
        'tpep_pickup_datetime',   # <--- ADDED: Actual Date
        'tpep_dropoff_datetime',  # <--- ADDED: Actual Date
        'payment_type_name',      # <--- ADDED: Readable Name (Credit Card, etc.)
        'rate_code_name',         # <--- ADDED: Readable Name (Standard, JFK, etc.)
        'vendor_name',            # <--- ADDED: Readable Name
        'passenger_count',
        'trip_distance',
        'fare_amount',
        'extra',
        'mta_tax',
        'tip_amount',
        'tolls_amount',
        'improvement_surcharge',
        'total_amount'
    ]]

    return fact_table