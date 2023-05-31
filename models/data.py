
def creating_player_record(player_name:str, players:dict) -> dict:
    players.update({player_name : [0,0,0,0]})

    return players


def reset_game_status(game_status:list) -> list:
    game_status[0] = ""
    game_status[1] = ""
    game_status[2] = 0
    game_status[3] = [4,4,4,4,4,4,0,4,4,4,4,4,4,0]

    return game_status



def set_player_victory(player:str, players:dict) -> dict:
    if player in ["Normal", "Avançado"]:
        player = "CPU"

    player_classifications:list[int] = players.get(player)
    player_classifications[1] += 1
    player_classifications[0] += 1
    players[player] = player_classifications

    return players



def set_player_lost(player:str, players:dict) -> dict:
    if player in ["Normal", "Avançado"]:
        player = "CPU"

    player_classifications:list[int] = players.get(player)

    player_classifications[3] += 1
    player_classifications[0] += 1

    players[player] = player_classifications

    return players



def set_player_tie(player1:str, player2:str, players:dict) -> dict:
    if player2 in ["Normal", "Avançado"]:
        player2 = "CPU"
    
    player1_classifications:list[int] = players.get(player1)
    player2_classifications:list[int] = players.get(player2)

    player1_classifications[2] += 1
    player2_classifications[2] += 1
    player1_classifications[0] += 1
    player2_classifications[0] += 1

    players[player1] = player1_classifications
    players[player2] = player2_classifications

    return players
