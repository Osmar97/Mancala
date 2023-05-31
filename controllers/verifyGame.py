from views import cli as v
from controllers import playGame as play
from controllers import gameTools as tools

def verifications_before_make_move(player:str, players:dict, game_status:list) -> bool:
    is_safe_to_make_move:bool = 0

    player_does_not_exists:bool = verify_if_players_exists(player, players)
    if player_does_not_exists == 1:
        v.print_message("Jogador inexistente.")
        return game_status

    game_on:bool = verify_if_game_is_on(game_status)
    if game_on == 0:
        v.print_message("Não existe jogo em curso.")
        return game_status

    player_is_gaming:bool = verify_if_choosed_player_is_gaming(player, game_status)
    if player_is_gaming == 0:
        v.print_message("Jogador não participa no jogo em curso.")
        return game_status

    if player_does_not_exists == 0 and game_on == 1 and player_is_gaming == 1:
        is_safe_to_make_move = 1
    
    return is_safe_to_make_move



def verify_if_every_thing_is_ok_before_start_game(players_list:list[str], player:dict, game_status:list) -> bool:
    is_safe_to_start_game:bool = 0

    player_does_not_exists:bool = verify_if_players_exists(players_list, player)
    if player_does_not_exists == 1:
        v.print_message("Jogador inexistente.")
        return game_status

    game_on:bool = verify_if_game_is_on(game_status)
    if game_on == 1:
        v.print_message("Existe um jogo em curso.")
        return game_status
    
    if player_does_not_exists == 0 and game_on == 0:
        is_safe_to_start_game = 1
    
    return is_safe_to_start_game



def verify_if_players_exists(player, players:dict) -> bool:
    player_does_not_exists:bool = 0

    type_is_list:bool = isinstance(player, list) #verify if player function parameter is list or string in order to choose better option to find if player exists

    if type_is_list == True:
        for element in player:
            found_match:int = 0

            for key in players:
                if element == key:
                    found_match +=1
                    break
            if found_match > 0:
                continue
            else:
                player_does_not_exists = 1
                break
    else:
        if player not in players:
            player_does_not_exists = 1
    
    return player_does_not_exists



def verify_if_game_is_on(game_status:list) -> bool:
    game_on:bool = 0

    if game_status[2] == 1:
        game_on = 1
    else:
        game_on = 0

    return game_on



def verify_if_choosed_player_is_gaming(player_name:str, game_status:list) -> bool:
    player_is_gaming:bool = 0

    if player_name in game_status:
        player_is_gaming = 1
    else:
        player_is_gaming = 0

    return player_is_gaming



def verify_if_player1_or_2(player:str, game_status:list) -> int:
    player_is_player1:int = 0

    index:int = game_status.index(player)

    if index == 0:
        player_is_player1 = 1
    else:
        player_is_player1 = 2
    
    return player_is_player1



def verify_if_game_is_finnished(board:list[int]) -> bool:
    game_is_finished:bool = 0
    zero_count:int = 0

    for i in range(len(board)):
        if i < 7:
            if board[i] == 0:
                zero_count += 1
                if zero_count == 6:
                    game_is_finished = 1
                    break
            if i == 6 and zero_count > 0:
                zero_count = 0

        elif i > 6 and i < 13:       
            if board[i] == 0:
                zero_count += 1
                if zero_count == 6:
                    game_is_finished = 1
                    break

    return game_is_finished



def verify_specials_moves(player_1_or_2:int, position:int, board:list[int], keep_playing:bool):
    if (position == 6 and player_1_or_2 == 1) or (position == 13 and player_1_or_2 == 2):
        keep_playing = 1
       
    else:
        position_in_front =  tools.get_position_in_front(player_1_or_2, position)

        if board[position] == 1 and board[position_in_front] > 0:
            if player_1_or_2 == 1 and position in [0,1,2,3,4,5]:
                play.make_play_with_position_in_front(player_1_or_2, position, position_in_front, board)

            elif player_1_or_2 == 2 and position in [7,8,9,10,11,12]:
                play.make_play_with_position_in_front(player_1_or_2, position, position_in_front, board) 

    return board, keep_playing