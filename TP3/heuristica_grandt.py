import csv

#TODO: Hacer una funcion para imprimir los datos listos para latex

'''
* La idea es tener en el equipo siempre los jugadores con mas puntos para la fecha
* Los de mas puntaje son titulares en la fecha determinada, el resto son suplentes
* Si hay empate de puntos se selecciona segun orden alfabetico inverso (Z-A) en el campo nombre de manera innsensitive
* El capitan es el de mas puntos en la fecha
'''

LIMITS_BY_POSITION = {"ARQ": 2, "DEL": 3, "DEF": 5, "VOL": 5}
FIRST_DATE_INDEX = 3
LAST_DATE_INDEX = 19
CHANGES_LIMIT = 4 # Solo puedo comprar/vender hasta 4 jugadores
BUDGET = 65000000
SECOND_DATE = 2
LAST_DATE = 16
MAX_SAME_CLUB = 3

def sort_by_date(data, date):
    '''
    Ordena la data por fecha date
    (es + 3 porque la primera fecha es la columna 4)
    '''
    return sorted(data, key=lambda row: (row["points"][date - 1], row["name"].lower()), reverse=True)

def parse_csv(csv_file):
    '''
    Parsea el csv y retorna los datos como una lista de dicts
    '''
    with open(csv_file) as csv_file:
        reader = csv.reader(csv_file, delimiter=",")
        next(reader) # ignore header
        parsed_data = []
        for player in reader:
            parsed_data.append(
                {
                    "name": player[0],
                    "position": player[1],
                    "club": player[2],
                    "cost": int(player[3]),
                    "points": [int(points) for i, points in enumerate(player) if i > FIRST_DATE_INDEX and i < LAST_DATE_INDEX],
                    "captain": False
                }
            )
    return parsed_data

def check_club(team, player):
    '''
    Devuelve True si se cumple la restriccion de clubes, False en caso contrario
    '''
    count = 0
    for players in team.values():
        count += len([member for member in players if member["club"] == player["club"]])
    return count + 1 <= MAX_SAME_CLUB

def fill_position(position, data, team, current_money):
    '''
    Llena la posicion con la cantidad de jugadores correspondientes, y devuelve lo que se gasto
    '''
    ordered_data = sort_by_date(data, 1)
    spend = 0
    current_index = 0
    while len(team[position]) < LIMITS_BY_POSITION[position]:
        player = ordered_data[current_index]

        same_position = player["position"] == position
        can_afford = current_money - int(player["cost"]) >= 0
        club_restriction = check_club(team, player)

        if same_position and can_afford and club_restriction:
            team[position].append(player)
            spend += int(player["cost"])
        current_index += 1
    return spend

def select_captain(team, date):
    '''
    Selecciona el capitan como aquel de mayor puntaje en la fecha date
    '''
    candidates = {}
    for players in team.values():
        candidate = sorted(players, key=lambda player: (player["points"][date - 1], player["name"].lower()), reverse=True)[0]
        candidates[candidate["name"]] = {"points": candidate["points"][date - 1], "position": candidate["position"]}

    choosen = sorted(candidates.items(), key=lambda player: (player[1]["points"], player[0].lower()), reverse=True)[0]

    for player in team[choosen[1]["position"]]:
        player["captain"] = player["name"] == choosen[0]

def calculate_points_for_date(date, team):
    total = 0
    for players in team.values():
        total += sum([player["points"][date - 1] for player in players])
        total += sum([player["points"][date - 1] for player in players if player["captain"]])
    return total

def check_team(team, budget, data, date):
    '''
    Chequea si hay algun jugador que se pueda comprar que tenga mas puntos que
    los de la posicion en la fecha date. Si no lo hay, elije entre el titular y el suplente
    Si lo hay, se vende el que menos puntos tenga en la fecha.
    Devuelve la plata que sobra
    '''
    current_money = budget
    changes_count = 0

    for player in data:
        if changes_count >= CHANGES_LIMIT:
            break

        position = player["position"]

        in_team = [member for member in team[position] if member["name"] == player["name"]] != []
        has_more_points = not [member for member in team[position] if member["points"][date - 1] > player["points"][date - 1]]
        club_restriction = check_club(team, player)

        if not in_team and has_more_points and club_restriction:
            player_to_sell = sorted(team[position], key=lambda player: (player["points"][date - 1], player["name"].lower()))[0]
            if player_to_sell["cost"] + current_money >= player["cost"]:
                team[position][:] = [member for member in team[position] if member["name"] != player_to_sell["name"]]
                team[position].append(player)
                #print("Cambio {sold} por {bought} en la fecha {date}".format(sold=player_to_sell["name"], bought=player["name"], date=date))
                current_money += player_to_sell["cost"] - player["cost"]
                changes_count += 1

        # se ordena por puntaje en la fecha, los de menos puntaje quedan de suplentes
        for players in team.values():
            players = sorted(players, key=lambda player: player["points"][date - 1], reverse=True)

    return current_money

def calculate_team_for_match(csv_file, budget):
    team = {
        "ARQ": [],
        "DEF": [],
        "VOL": [],
        "DEL": [],
    }

    data = parse_csv(csv_file)

    # Se arma el equipo para la primera fecha
    total_points = 0
    current_money = budget
    for position in team.keys():
        current_money -= fill_position(position, data, team, current_money)

    select_captain(team, 1)
    total_points = calculate_points_for_date(1, team)
    # Se arma el equipo para las fechas restantes, comprando y vendiendo segun convenga
    for date in range(SECOND_DATE, LAST_DATE):
        money = check_team(team, current_money, data, date)
        select_captain(team, date)
        total_points += calculate_points_for_date(date, team)
    print(total_points)

def to_latex_table(data):
    pass

calculate_team_for_match("./NoNulos.csv", BUDGET)
