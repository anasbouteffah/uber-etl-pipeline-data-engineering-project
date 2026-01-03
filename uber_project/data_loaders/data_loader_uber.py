import io
import pandas as pd
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader

@data_loader
def load_data(*args, **kwargs):
    # Use forward slashes (/) to avoid the \U error
    file_path = "C:/Users/dell/Desktop/uber-data-eng/data/uber_data.csv"
    
    return pd.read_csv(file_path)