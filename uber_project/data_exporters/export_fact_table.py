import pandas as pd
if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

@data_exporter
def export_data(data, *args, **kwargs):
    """
    Exports data to some source.
    Args:
        data: The output from the upstream parent block (The Fact Table)
    """
    # Define the save path (Forward slashes for Windows safety)
    output_path = "C:/Users/dell/Desktop/uber-data-eng/data/fact_table.csv"
    
    # Save the dataframe to CSV, without the index numbers
    data.to_csv(output_path, index=False)
    
    print(f"Success! Data exported to: {output_path}")