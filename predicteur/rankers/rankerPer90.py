import os
import csv
from collections import defaultdict

# Read the CSV file and process the data
data = []
with open('../../data/2022-23/cleaned_players.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        data.append(row)

# Find the player with the most minutes
most_minutes = max(int(player['minutes']) for player in data)

# Calculate points per 90 minutes for players with enough minutes
valid_players = []
for player in data:
    if int(player['minutes']) > most_minutes / 2:
        points_per_90 = (int(player['total_points']) / int(player['minutes'])) * 90
        player['points_per_90'] = points_per_90
        valid_players.append(player)

# Group valid players by position
position_players = defaultdict(list)
for player in valid_players:
    position_players[player['element_type']].append(player)

# Sort players within each position by points per 90 minutes
for position, players in position_players.items():
    position_players[position] = sorted(players, key=lambda x: x['points_per_90'], reverse=True)

# Create a folder for output files
output_folder = 'player_rankings_per_90'
os.makedirs(output_folder, exist_ok=True)

# Write data to separate CSV files for each position
for position, players in position_players.items():
    output_filename = os.path.join(output_folder, f'player_rankings_{position}.csv')
    with open(output_filename, 'w', newline='') as output_csv:
        fieldnames = ['Position', 'Rank', 'Name', 'Points per 90 Minutes', 'Now Cost']
        csv_writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
        csv_writer.writeheader()

        for rank, player in enumerate(players, start=1):
            csv_writer.writerow({
                'Position': position,
                'Rank': rank,
                'Name': f"{player['first_name']} {player['second_name']}",
                'Points per 90 Minutes': f"{player['points_per_90']:.2f}",
                'Now Cost': player['now_cost']
            })

print(f"Data has been written to {output_folder}")
