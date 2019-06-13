import csv


'''
La idea es ordenar los jugadores por puntaje en la primera fecha, luego ir llenando cada posicion con el 
que obtuvo mas puntaje en esa fecha, siempre que de el presupuesto.
'''

LIMITS_BY_POSITION = {"ARQ": 1, "DEL": 2, "DEF": 4, "VOL": 4}


def parse_csv(csv_file):
    with open(csv_file) as csv_file:
        reader = csv.reader(csv_file, delimiter=",")
        next(reader) # ignore header
        sorted_data = sorted(reader, key=lambda row: int(row[4]), reverse=True)
        parsed_data = []
        for player in sorted_data:
            parsed_data.append({"name": player[0], "position": player[1], "club": player[2], "cost": player[3], "points": player[4]})
    return parsed_data


def fill_position(position, data, team, current_money):
    print(current_money)
    spend = 0
    while len(team[position]) < LIMITS_BY_POSITION[position]:
        for player in data:
            if player["position"] == position and current_money - int(player["cost"]) >= 0 and player["name"] not in team[position]:
                team[position].append(player["name"])
                spend += int(player["cost"])
                break
    return spend


def calculate_team_for_match(csv_file, budget):
    team = {
        "ARQ": [],
        "DEL": [],
        "DEF": [],
        "VOL": []
    }

    data = parse_csv(csv_file)

    current_money = budget
    for position in team.keys():
        current_money -= fill_position(position, data, team, current_money)
    print(current_money)
    return team


team = calculate_team_for_match("./NoNulos.csv", 65000000)
print(team)
