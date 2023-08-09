from pulp import LpMaximize, LpProblem, LpVariable, lpSum
import csv


# Read the player rankings from the CSV
player_rankings = []
with open('../rankers/player_rankings_filtered.csv', 'r') as csv_file:
    next(csv_file)  # Skip the header
    for line in csv_file:
        position, rank, name, points_per_90, now_cost = line.strip().split(',')
        player_rankings.append((position, name, float(points_per_90), int(now_cost)))

# Define the problem
model = LpProblem(name="FantasyTeamOptimization", sense=LpMaximize)

# Create variables
players_selected = LpVariable.dicts("Selected", range(len(player_rankings)), cat="Binary")

# Objective function (maximize points per 90)
model += sum(players_selected[player] * points for player, (_, _, points, _) in enumerate(player_rankings))

# Corrected Constraints
budget = 1000
model += lpSum(players_selected[player] * cost for player, (_, _, _, cost) in enumerate(player_rankings)) <= budget
model += lpSum(players_selected[player] for player, (_, position, _, _) in enumerate(player_rankings) if position == "MID") >= 5
model += lpSum(players_selected[player] for player, (_, position, _, _) in enumerate(player_rankings) if position == "DEF") >= 5
model += lpSum(players_selected[player] for player, (_, position, _, _) in enumerate(player_rankings) if position == "FWD") >= 3
model += lpSum(players_selected[player] for player, (_, position, _, _) in enumerate(player_rankings) if position == "GK") >= 2



# Solve the problem
model.solve()

# Collect selected player data
selected_players = []
total_points_per_90 = 0.0
for player, (_, name, points_per_90, _) in enumerate(player_rankings):
    if players_selected[player].varValue:
        selected_players.append((name, points_per_90))
        total_points_per_90 += points_per_90

# Print and write the optimized team selection with detailed breakdown
output_filename = 'optimized_team_selection.csv'
with open(output_filename, 'w', newline='') as output_csv:
    csv_writer = csv.writer(output_csv)
    csv_writer.writerow(["Name", "Points per 90"])
    for name, points_per_90 in selected_players:
        csv_writer.writerow([name, f"{points_per_90:.2f}"])
    csv_writer.writerow(["Total Points per 90", f"{total_points_per_90:.2f}"])

print(f"Optimized team selection and detailed breakdown have been written to {output_filename}")
