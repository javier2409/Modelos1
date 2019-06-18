import csv
import pandas as pd

'''
* La idea es tener en el equipo siempre los jugadores con mas puntos para la fecha
* Los de mas puntaje son titulares en la fecha determinada, el resto son suplentes
* Si hay empate de puntos se selecciona segun orden alfabetico inverso (Z-A) (porque dio mejor) en el campo nombre de manera innsensitive
* El capitan es el de mas puntos en la fecha
'''

STRATEGY = {"ARQ": 1, "DEL": 3, "DEF": 3, "VOL": 4}
FIRST_DATE_INDEX = 3
LAST_DATE_INDEX = 19
CHANGES_LIMIT = 4 # Solo puedo comprar/vender hasta 4 jugadores
BUDGET = 65000000
SECOND_DATE = 2
LAST_DATE = 16
MAX_SAME_CLUB = 3
CSV_FILE = "./NoNulos.csv"
OUTPUT_FILE = "./results.csv"
SUBSTITUTES_COUNT = 6

def sort_players(players, date, **kwargs):
    '''
    Ordena por puntos en la fecha date y por nombre alfabetico inverso
    '''
    reverse = kwargs["reverse"] if "reverse" in kwargs else True
    return sorted(players, key=lambda player: (player["points"][date - 1], player["name"].lower()), reverse=reverse)

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

def fill_position(position, position_limit, data, team, current_money):
    '''
    Llena la posicion con la cantidad de jugadores correspondientes,
    y devuelve lo que sobro de dinero
    '''
    ordered_data = sort_players(data, 1)
    spend = 0
    current_index = 0
    while len(team[position]) < position_limit:
        player = ordered_data[current_index]

        same_position = player["position"] == position
        can_afford = current_money - int(player["cost"]) >= 0
        club_restriction = check_club(team, player)

        if same_position and can_afford and club_restriction:
            team[position].append(player)
            spend += int(player["cost"])
        current_index += 1
    return current_money - spend

def select_captain(team, date):
    '''
    Selecciona el capitan como aquel de mayor puntaje en la fecha date
    '''
    candidates = {}
    for players in team.values():
        candidate = sort_players(players, date)[0]
        candidates[candidate["name"]] = {"points": candidate["points"][date - 1], "position": candidate["position"]}

    choosen = sorted(candidates.items(), key=lambda player: (player[1]["points"], player[0].lower()), reverse=True)[0]

    for player in team[choosen[1]["position"]]:
        player["captain"] = player["name"] == choosen[0]

def calculate_points_for_date(date, team):  
    total = 0
    for position in team:
        players = []
        for i in range(STRATEGY[position]):
            players.append(team[position][i])
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
    data = sort_players(data,date)
    for player in data:
        if changes_count >= CHANGES_LIMIT:
            break

        position = player["position"]

        in_team = [member for member in team[position] if member["name"] == player["name"]] != []
        has_more_points = not [member for member in team[position] if member["points"][date - 1] > player["points"][date - 1]]
        club_restriction = check_club(team, player)

        if not in_team and has_more_points and club_restriction:
            player_to_sell = sort_players(team[position], date, reverse=False)[0]
            if player_to_sell["cost"] + current_money >= player["cost"]:
                team[position][:] = [member for member in team[position] if member["name"] != player_to_sell["name"]]
                team[position].append(player)
                #print("Cambio {sold} por {bought} en la fecha {date}".format(sold=player_to_sell["name"], bought=player["name"], date=date))
                current_money += player_to_sell["cost"] - player["cost"]
                changes_count += 1

        # se ordena por puntaje en la fecha, los de menos puntaje quedan de suplentes
        for position in team:
            team[position] = sort_players(team[position], date)

    return current_money

def get_limits_by_position(data):
    '''
    Devuelve los limites para cada posicion, si los suplentes son dispares asigna a las posiciones con mejor promedio
    de puntos la mayor cantidad de suplentes posibles
    '''
    limits_by_positions = {
        "ARQ": STRATEGY["ARQ"],
        "DEF": STRATEGY["DEF"],
        "VOL": STRATEGY["VOL"],
        "DEL": STRATEGY["DEL"]
    }
    avg_by_position = {"ARQ": 0, "DEF": 0, "VOL": 0, "DEL": 0}
    positions_count = {"ARQ": 0, "DEF": 0, "VOL": 0, "DEL": 0}
    # suma todos los puntos por posicion
    for player in data:
        avg_by_position[player["position"]] += sum(player["points"])
        positions_count[player["position"]] += 1

    # calcula los promedios
    for position in avg_by_position.keys():
        avg_by_position[position] = avg_by_position[position] / positions_count[position]

    sorted_by_avg = sorted(avg_by_position.items(), key=lambda avg_by_position: avg_by_position[1], reverse=True)
    sorted_positions = [position[0] for position in sorted_by_avg]

    substitutes_added_count = 0
    while substitutes_added_count < SUBSTITUTES_COUNT:
        position_to_add = sorted_positions[substitutes_added_count % len(sorted_positions)]
        limits_by_positions[position_to_add] += 1
        substitutes_added_count += 1

    return limits_by_positions

def print_as_latex_table(data):
    tit_df = []
    sup_df = []
    for position in data:
        for i,player in enumerate(data[position]):

            full_name = player["name"]
            first_name = full_name.split(',')[0]
            last_name = full_name.split(',')[1]
            position = player["position"]
            p = [first_name,last_name,position]
            if i < STRATEGY[position]:
                tit_df.append(p)
            else:
                sup_df.append(p)
            command = "{}         & {}         & {}      \\\ \\hline".format(
                first_name, last_name, position
            )
            #print(command)
    df1 = pd.DataFrame(tit_df)
    df1.columns = ['Nombre','Apellido','Posicion']
    print('Titulares \n')
    print(df1.to_latex(longtable=True,multicolumn=True,index_names=False,index=False))
    if SUBSTITUTES_COUNT > 0:
        df2 = pd.DataFrame(sup_df)
        df2.columns = ['Nombre','Apellido','Posicion']
        print('Suplentes\n')
        print(df2.to_latex(longtable=True,multicolumn=True,index_names=False,index=False))

def print_as_table(team):
    print("Nombre Apellido Posicion")
    for players in team.values():
        for player in players:
            print("{} {}".format(player["name"], player["position"]))

def calculate_team_for_match():
    team = {"ARQ": [], "DEF": [], "VOL": [], "DEL": []}
    total_points = 0
    current_money = BUDGET
    data = parse_csv(CSV_FILE)
    limits_by_positions = get_limits_by_position(data)
    first_date = 1

    # Se arma el equipo para la primera fecha
    for position in team.keys():
        current_money = fill_position(position, limits_by_positions[position], data, team, current_money)
    select_captain(team, first_date)
    total_points = calculate_points_for_date(first_date, team)
    print("\\textbf{Fecha 1}\n")
    print_as_latex_table(team)
    # Se arma el equipo para las fechas restantes, comprando y vendiendo segun convenga
    for date in range(SECOND_DATE, LAST_DATE):
        current_money = check_team(team, current_money, data, date)
        select_captain(team, date)
        total_points += calculate_points_for_date(date, team)
        print("\\textbf{Fecha "+str(date)+"}\n")
        print_as_latex_table(team)

    print("\nPuntos totales con {} suplentes: {}".format(SUBSTITUTES_COUNT, total_points))

calculate_team_for_match()
