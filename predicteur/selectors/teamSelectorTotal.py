from pulp import LpMaximize, LpProblem, LpVariable, lpSum
import csv

# Read the player rankings from the CSV
player_rankings = []
with open('../rankers/player_rankings_filtered.csv', 'r') as csv_file:
    next(csv_file)  # Skip the header
    for line in csv_file:
        position, rank, name, points, now_cost = line.strip().split(',')
        player_rankings.append((position, name, float(points), int(now_cost)))

# Define the problem
model = LpProblem(name="FantasyTeamOptimization", sense=LpMaximize)

# Create variables
players_selected = LpVariable.dicts("Selected", range(len(player_rankings)), cat="Binary")
captains = LpVariable.dicts("Captain", range(len(player_rankings)), cat="Binary")

# Objective function (maximize total points)
model += sum(players_selected[player] * points * (2 if captains[player].varValue else 1)
              for player, (_, _, points, _) in enumerate(player_rankings))

# Select only one captain
model += lpSum(captains[player] for player in captains) == 1

# Constraints for the number of players per position
model += lpSum(players_selected[player] for player, (position, _, _, _) in enumerate(player_rankings) if position == "MID") == 5
model += lpSum(players_selected[player] for player, (position, _, _, _) in enumerate(player_rankings) if position == "DEF") == 5
model += lpSum(players_selected[player] for player, (position, _, _, _) in enumerate(player_rankings) if position == "FWD") == 3
model += lpSum(players_selected[player] for player, (position, _, _, _) in enumerate(player_rankings) if position == "GK") == 2

# Constraints to ensure the budget constraint
model += lpSum(players_selected[player] * cost for player, (_, _, _, cost) in enumerate(player_rankings)) <= 1000

# Solve the problem
model.solve()

# Collect selected player data
selected_players = []
total_points = 0.0
total_cost = 0
captain = None
for player, (_, name, points, cost) in enumerate(player_rankings):
    if players_selected[player].varValue:
        selected_players.append((name, points * (2 if captains[player].varValue else 1), cost, "Captain" if captains[player].varValue else "No"))
        total_points += points * (2 if captains[player].varValue else 1)
        total_cost += cost
        if captains[player].varValue:
            captain = name

# Print and write the optimized team selection with detailed breakdown
output_filename = 'optimized_team_selection.csv'
with open(output_filename, 'w', newline='') as output_csv:
    csv_writer = csv.writer(output_csv)
    csv_writer.writerow(["Position", "Name", "Points", "Cost", "Captain"])
    for name, points, cost, captain_flag in selected_players:
        position = next(position for position, n, p, c in player_rankings if n == name)
        csv_writer.writerow([position, name, f"{points:.2f}", cost, captain_flag])
    csv_writer.writerow(["Total Points", f"{total_points:.2f}", "Total Cost", total_cost])

print(f"Optimized team selection and detailed breakdown have been written to {output_filename}")
