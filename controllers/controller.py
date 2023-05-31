from models import data as data
from views import cli as v
from controllers import verifyGame as ver
from controllers import playGame as play
from controllers import gameTools as tools
import json

def register_user_rj(user_input:list[str], players:dict) -> dict:
    player_name:str = user_input[1]

    if player_name in players:
        v.print_message("Jogador existente.") ## verificar este error
    else:
        data.creating_player_record(player_name, players)
        v.print_message("Jogador registado com sucesso.")
        
    return players



def save_game(players:dict, game_status:list) -> None:
    list_to_dict:dict = {}

    save_game_file:open = open(r"Save Game.txt", "w")

    list_to_dict.update({'file' : game_status})

    save_game_file.write(json.dumps(players)+"\n")
    save_game_file.write(json.dumps(list_to_dict))
    v.print_message("Jogo gravado com sucesso.")



def load_saved_game() -> None:
    load_data:list = []
    players:dict = {}
    game_status:list = []

    with open('Save Game.txt') as save_game_file:
        load_data = save_game_file.read().split("\n")

    players = json.loads(load_data[0])
    game_status = json.loads(load_data[1]).get('file')
    v.print_message("Jogo lido com sucesso.")

    return players, game_status



def prepare_to_initialize_game_ij(user_input:list, player:dict, game_status:list) -> list:
    players_list:list[str] = [user_input[1], user_input[2]]

    is_safe_to_start_game:bool = 0

    is_safe_to_start_game = ver.verify_if_every_thing_is_ok_before_start_game(players_list, player, game_status)

    if is_safe_to_start_game == 1:
        play.start_game(players_list, game_status)
        v.print_message('Jogo iniciado com sucesso.')

    return game_status



def prepare_to_initialize_automatic_game_ija(user_input:list, players:dict, game_status:list) -> None:
    players_list: list = [user_input[1], user_input[2]]

    player_exists:bool = ver.verify_if_players_exists(user_input[1], players)
    if player_exists == 1:
        v.print_message("Jogador inexistente.")

    game_on: bool = ver.verify_if_game_is_on(game_status)
    if game_on == 1:
        v.print_message("Existe um jogo em curso.")

    if player_exists == 0 and game_on == 0: 
        if user_input[2] == "Normal":
            v.print_message(f"Jogo automático de nível {user_input[2]} iniciado com sucesso.")
            play.start_game(players_list, game_status)

        elif user_input[2] == "Avançado":
            v.print_message(f"Jogo automático de nível {user_input[2]} iniciado com sucesso.")
            play.start_game(players_list, game_status)



def prepare_to_play_game(user_input:list, players:dict, game_status:list) -> list:
    is_safe_to_make_move:bool = 0
    game_is_finished:bool = 0
    keep_playing:bool = 0

    player:str = str(user_input[1])
    position:int = int(user_input[2])
    board:list[int] = game_status[3]

    human_player_keep_play:bool = 1
    cpu_player_keep_play:bool = 1
 
    is_safe_to_make_move = ver.verifications_before_make_move(player, players, game_status)

    if is_safe_to_make_move == 1:
    
        while human_player_keep_play == 1:  
            human_player_keep_play = 0

            player1_or_player2 = ver.verify_if_player1_or_2(player, game_status)
            position = tools.get_board_index_for_inputed_position(player1_or_player2, position)
            board, keep_playing, game_is_finished = play.make_play(player1_or_player2, position, board)
            game_status[3] = board

            if keep_playing == 1:
                cpu_player_keep_play = 0
                v.print_message(f"O jogador {player} tem direito a outra jogada.")

        while cpu_player_keep_play == 1:  
            cpu_player_keep_play = 0     

            if game_status[1] == "Normal":
                player1_or_player2 = ver.verify_if_player1_or_2(game_status[1], game_status)
                keep_playing = play.normal_ai_play(player1_or_player2, board)
                game_status[3] = board

            elif game_status[1] == "Avançado":
                player1_or_player2 = ver.verify_if_player1_or_2(game_status[1], game_status)
                keep_playing = play.advanced_ai_play(player1_or_player2, board)
                game_status[3] = board


            if keep_playing == 1:
                cpu_player_keep_play = 1

        if game_is_finished == 1:
            play.finish_game(players, game_status)

        elif game_is_finished == 0 and keep_playing == 0:
            v.print_message("Jogada efetuada com sucesso.")

    return game_status, players