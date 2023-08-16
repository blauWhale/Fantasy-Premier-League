import csv
import os
from collections import defaultdict

# Read input CSV data
input_filename = '../../data/2023-24/gws/gw1.csv'
output_folder = 'player_xP_per90'

data = []
with open(input_filename, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        data.append(row)

# Filter out players with 0 total points
data = [row for row in data if int(row['total_points']) > 0]

# Calculate delta and points per 90 minutes, and update data
for row in data:
    row['delta'] = float(row['total_points']) - float(row['xP'])
    minutes = int(row['minutes'])
    if minutes > 0:
        points_per_90 = (float(row['total_points']) / minutes) * 90
        row['points_per_90'] = round(points_per_90, 2)
    else:
        row['points_per_90'] = 0.0

# Define the output fields
output_fields = ['name', 'team', 'position', 'total_points', 'xP', 'delta', 'points_per_90', 'minutes']

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Group data by position
position_players = defaultdict(list)
for player in data:
    position_players[player['position']].append(player)

# Write separate output CSV files for each position
for position, players in position_players.items():
    output_filename = os.path.join(output_folder, f'output_{position}.csv')
    with open(output_filename, 'w', newline='') as output_csv:
        csv_writer = csv.DictWriter(output_csv, fieldnames=output_fields)
        csv_writer.writeheader()

        for player in players:
            csv_writer.writerow({
                'name': player['name'],
                'team': player['team'],
                'position': player['position'],
                'total_points': player['total_points'],
                'xP': player['xP'],
                'delta': player['delta'],
                'points_per_90': player['points_per_90'],
                'minutes': player['minutes']
            })

    print(f"CSV file '{output_filename}' created successfully for position {position}.")

print("All files have been created successfully.")
