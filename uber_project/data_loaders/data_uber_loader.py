import io
import pandas as pd

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader


@data_loader
def load_data(*args, **kwargs):
    filepath = 'uber_project/data/uber_data.csv'
    return pd.read_csv(filepath)
