import csv
import pandas as pd
import os
import shutil

# File paths
input_file = 'data/bouwen_of_verbouwen_van_woningen.csv'
output_decimal_file = 'data/bouwen_of_verbouwen_van_woningen_decimal.csv'
output_datetime_file = 'data/bouwen_of_verbouwen_van_woningen_with_datetime.csv'
output_filtered_file = 'data/bouwen_of_verbouwen_van_woningen_filtered.csv'
output_nieuwbouw_pivot_file = 'data/nieuwbouw_pivot.csv'
output_renovatie_pivot_file = 'data/renovatie_pivot.csv'
output_sloop_pivot_file = 'data/sloop_pivot.csv'
output_aandeel_flats_pivot_file = 'data/aandeel_flats_pivot.csv'

# Output directory
output_dir = 'output'
output_data_dir = os.path.join(output_dir, 'data')
os.makedirs(output_data_dir, exist_ok=True)

# --- Step 1: Convert to Decimal format ---
print("Starting Step 1: Converting to Decimal format...")

# Read the input CSV file
with open(input_file, 'r', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    rows = list(reader)

# Process the data
processed_rows = []
for row in rows:
    processed_row = [cell.replace('.', '').replace(',', '.') for cell in row]
    processed_rows.append(processed_row)

# Write the processed data to the output CSV file
with open(output_decimal_file, 'w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    writer.writerows(processed_rows)

print(f"Step 1 Completed: Processed data saved to {output_decimal_file}")

# --- Step 2: Add datetime column ---
print("Starting Step 2: Adding datetime column...")

# Read the input CSV file
df = pd.read_csv(output_decimal_file)

# Create a mapping for quarters to months
quarter_to_month = {
    'Q1': '01',
    'Q2': '04',
    'Q3': '07',
    'Q4': '10'
}

# Extract the quarter from the column and map it to the corresponding month
df['Month'] = df['[Project Indiening DatumautoCalendarQuarter]'].map(quarter_to_month)

# Combine 'Jaar' and 'Month' to create a new datetime column
df['Date'] = pd.to_datetime(df['Jaar indiening'].astype(str) + '-' + df['Month'] + '-01')

# Drop the temporary 'Month' column
df.drop(columns=['Month'], inplace=True)

# Save the updated DataFrame to a new CSV file
df.to_csv(output_datetime_file, index=False)

print(f"Step 2 Completed: Updated data saved to {output_datetime_file}")

# --- Step 3: Filter data ---
print("Starting Step 3: Filtering data...")

# Read the input CSV file
df = pd.read_csv(output_datetime_file)

# Convert the 'Date' column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Filter the rows to include only dates starting from 2018
df_filtered = df[df['Date'] >= '2018-01-01']

# Identify the last quarter available in the data
last_date = df_filtered['Date'].max()
last_quarter_start = pd.Timestamp(year=last_date.year, month=(last_date.month - 1) // 3 * 3 + 1, day=1)
last_quarter_end = pd.Timestamp(year=last_date.year, month=(last_date.month - 1) // 3 * 3 + 3, day=1) + pd.offsets.MonthEnd(1)

# Remove the last quarter
df_filtered = df_filtered[df_filtered['Date'] < last_quarter_start]

# Print the last quarter available
last_quarter = f"Q{((last_quarter_start.month - 1) // 3) + 1} {last_quarter_start.year}"
print(f"The last quarter available was: {last_quarter}")

# Save the updated DataFrame to a new CSV file
df_filtered.to_csv(output_filtered_file, index=False)

print(f"Step 3 Completed: Filtered data saved to {output_filtered_file}")

# --- Step 4: Create Nieuwbouw Pivot ---
print("Starting Step 4: Creating Nieuwbouw pivot table...")

# Read the input CSV file
df = pd.read_csv(output_filtered_file)

# Filter for Handeling = Nieuwbouw
df_nieuwbouw = df[df['Handeling'] == 'Nieuwbouw']

# Further filter for Gebouw Functie kort = eengezinswoning and meergezinswoning
df_nieuwbouw = df_nieuwbouw[df_nieuwbouw['Gebouw Functie kort'].isin(['eengezinswoning', 'meergezinswoning'])]

# Create a new column for Year-Quarter
df_nieuwbouw['Year-Quarter'] = df_nieuwbouw['Jaar indiening'].astype(str) + '-' + df_nieuwbouw['[Project Indiening DatumautoCalendarQuarter]']

# Create a pivot table
pivot_table = df_nieuwbouw.pivot_table(
    index='Year-Quarter',
    columns='Gebouw Functie kort',
    values='Aantal wooneenheden',
    aggfunc='sum',
    fill_value=0
)

# Save the pivot table to a new CSV file
pivot_table.to_csv(output_nieuwbouw_pivot_file)

print(f"Step 4 Completed: Pivot table saved to {output_nieuwbouw_pivot_file}")

# --- Step 5: Create Renovatie Pivot ---
print("Starting Step 5: Creating Renovatie pivot table...")

# Read the input CSV file
df = pd.read_csv(output_filtered_file)

# Filter for Handeling = Verbouwen of hergebruik
df_renovatie = df[df['Handeling'] == 'Verbouwen of hergebruik']

# Further filter for Gebouw Functie kort = eengezinswoning and meergezinswoning
df_renovatie = df_renovatie[df_renovatie['Gebouw Functie kort'].isin(['eengezinswoning', 'meergezinswoning'])]

# Create a new column for Year-Quarter
df_renovatie['Year-Quarter'] = df_renovatie['Jaar indiening'].astype(str) + '-' + df_renovatie['[Project Indiening DatumautoCalendarQuarter]']

# Create a pivot table
pivot_table = df_renovatie.pivot_table(
    index='Year-Quarter',
    columns='Gebouw Functie kort',
    values='Aantal wooneenheden',
    aggfunc='sum',
    fill_value=0
)

# Save the pivot table to a new CSV file
pivot_table.to_csv(output_renovatie_pivot_file)

print(f"Step 5 Completed: Pivot table saved to {output_renovatie_pivot_file}")

# --- Step 6: Create Sloop Pivot ---
print("Starting Step 6: Creating Sloop pivot table...")

# Read the input CSV file
df = pd.read_csv(output_filtered_file)

# Filter for Handeling = Sloop
df_sloop = df[df['Handeling'] == 'Sloop']

# Create a new column for Year-Quarter
df_sloop['Year-Quarter'] = df_sloop['Jaar indiening'].astype(str) + '-' + df_sloop['[Project Indiening DatumautoCalendarQuarter]']

# Create a pivot table
pivot_table = df_sloop.pivot_table(
    index='Year-Quarter',
    values='Aantal gebouwen',
    aggfunc='sum',
    fill_value=0
)

# Rename the column
pivot_table.rename(columns={'Aantal gebouwen': 'Sloop'}, inplace=True)

# Save the pivot table to a new CSV file
pivot_table.to_csv(output_sloop_pivot_file)

print(f"Step 6 Completed: Pivot table saved to {output_sloop_pivot_file}")

# --- Step 7: Create Aandeel Flats Pivot ---
print("Starting Step 7: Creating Aandeel Flats pivot table...")

# Read the input CSV file
df = pd.read_csv(output_nieuwbouw_pivot_file)

# Calculate the 'aandeel-flats' column
df['aandeel-flats'] = df['meergezinswoning'] / (df['eengezinswoning'] + df['meergezinswoning'])

# Select only the 'Year-Quarter' and 'aandeel-flats' columns for the output
df_aandeel_flats = df[['Year-Quarter', 'aandeel-flats']]

# Save the result to a new CSV file
df_aandeel_flats.to_csv(output_aandeel_flats_pivot_file, index=False)

print(f"Step 7 Completed: Pivot table saved to {output_aandeel_flats_pivot_file}")

# --- Step 8: Copy pivot CSV files to output folder
print("Starting Step 8: Copying pivot CSV files to output folder...")
pivot_files = [output_nieuwbouw_pivot_file, output_renovatie_pivot_file, output_sloop_pivot_file, output_aandeel_flats_pivot_file]
for file in pivot_files:
  shutil.copy(file, output_data_dir)
  print(f"Copied {file} to {output_data_dir}")


print("All steps completed.")