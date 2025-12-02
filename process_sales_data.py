import pandas as pd
import os

# Define the data directory and file names
data_dir = 'data'
csv_files = [
    'daily_sales_data_0.csv',
    'daily_sales_data_1.csv',
    'daily_sales_data_2.csv'
]

# List to store filtered dataframes
filtered_data = []

# Process each CSV file
for csv_file in csv_files:
    file_path = os.path.join(data_dir, csv_file)
    
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Filter for pink morsel products only (case-insensitive)
    pink_morsel_df = df[df['product'].str.lower() == 'pink morsel']
    
    # Clean the price column (remove '$' and convert to float)
    pink_morsel_df = pink_morsel_df.copy()
    pink_morsel_df['price'] = pink_morsel_df['price'].str.replace('$', '').astype(float)
    
    # Calculate sales (price * quantity)
    pink_morsel_df['sales'] = pink_morsel_df['price'] * pink_morsel_df['quantity']
    
    # Select only the required columns
    output_df = pink_morsel_df[['sales', 'date', 'region']]
    
    # Add to the list
    filtered_data.append(output_df)
    
    print(f"Processed {csv_file}: {len(output_df)} pink morsel records found")

# Combine all dataframes
combined_df = pd.concat(filtered_data, ignore_index=True)

# Write to output file
output_file = 'pink_morsel_sales.csv'
combined_df.to_csv(output_file, index=False)

print(f"\nTotal pink morsel records: {len(combined_df)}")
print(f"Output file created: {output_file}")
print(f"\nFirst few rows of output:")
print(combined_df.head(10))
