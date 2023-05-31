from controllers import controller as con
from controllers import gameTools as tools

def main() -> None:
    #main variables
    players = {"CPU" : [0,0,0,0]} # dictionary with registred players
    game_status = ["player1", "player", "gameIsOn", [4,4,4,4,4,4,0,4,4,4,4,4,4,0]] #list where game information and mancala board game will be saved

    valid_awnser:bool = 0
    
    while True:
        user_input, valid_awnser = get_instruction()
        if valid_awnser == 1:

            if user_input[0] == "RJ" and len(user_input) == 2:
                con.register_user_rj(user_input, players)

            elif user_input[0] == "LJ" and len(user_input) == 1:
                list_players_lj(players)

            elif user_input[0] == "IJ" and len(user_input) == 3:
                con.prepare_to_initialize_game_ij(user_input, players, game_status)

            elif user_input[0] == "IJA" and len(user_input) == 3:
                con.prepare_to_initialize_automatic_game_ija(user_input, players, game_status)

            elif user_input[0] == "J" and len(user_input) == 3:
                con.prepare_to_play_game(user_input, players, game_status)

            elif user_input[0] == "DJ" and len(user_input) == 1:
                details_of_game_dj(game_status)

            elif user_input[0] == "D" and (len(user_input) == 2 or len(user_input) == 3):
                tools.quit_game_d(user_input, players, game_status)

            elif user_input[0] == "G" and len(user_input) == 1:
                con.save_game(players, game_status)

            elif user_input[0] == "L" and len(user_input) == 1:
                players, game_status = con.load_saved_game()

            elif user_input[0] in ["", " "]:
                pass

            else:
                print("Instrução inválida.")



def get_instruction():
        user_input = (input()).split(" ")
        if user_input[0] in ["RJ", "LJ", "IJ", "IJA", "DJ", "J", "D", "G", "L", " ", ""]:
            valid_awnser = 1
            return user_input, valid_awnser
        else:
            print("Instrução inválida.")
            return user_input, 0



def print_message(message:str) -> None:
    print(message)



def list_players_lj(players:dict) -> None:
    player_sort:list = [[k, players[k]] for k in players]

    if player_sort:
        for i in range(len(player_sort)):
           for j in range(len(player_sort)-i-1):
               if player_sort[j][1][1] < player_sort[j+1][1][1]:
                   tmp = player_sort[j+1]
                   player_sort[j+1] = player_sort[j]
                   player_sort[j] = tmp
               elif player_sort[j][1][1] == player_sort[j+1][1][1] and player_sort[j][0] > player_sort[j+1][0]:
                   tmp = player_sort[j+1]
                   player_sort[j+1] = player_sort[j]
                   player_sort[j] = tmp

        for i in range(len(player_sort)):
            print (f" {player_sort[i][0]} {player_sort[i][1][0]} {player_sort[i][1][1]} {player_sort[i][1][2]} {player_sort[i][1][3]}")
      
    else:
        print_message("Sem jogadores registados.")



def finish_game(player1:str, seeds_player1:int, seeds_player2:int, games_status: list) -> None:
    second_player: str = games_status[1]

    if second_player in ["Normal", "Avançado"]:
        second_player = "CPU"

    print("Jogo terminado.")
    print(f"{player1} {seeds_player1}")
    print(f"{second_player} {seeds_player2}")



def details_of_game_dj(games_status:list) -> None:
    second_player: str = games_status[1]

    if second_player in ["Normal", "Avançado"]:
        second_player = "CPU"

    if games_status[2] == 1:
        board = games_status[3]

        print (f" {games_status[0]} [{board[5]}] [{board[4]}] [{board[3]}] [{board[2]}] [{board[1]}] [{board[0]}] ({board[6]})")
        print (f" {second_player} [{board[7]}] [{board[8]}] [{board[9]}] [{board[10]}] [{board[11]}] [{board[12]}] ({board[13]})")

    else:
        print("Não existe jogo em curso.")