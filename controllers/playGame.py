from controllers import verifyGame as ver
from controllers import gameTools as tools
from models import data
from views import cli as cli

def start_game(players_list:list, game_status:list) -> list:
    game_status[0] = players_list[0] # player 1
    game_status[1] = players_list[1] # player 2
    game_status[2] = 1               # game on or off

    return game_status



def start_move(board:list[int], position:int):
    seeds:int = board[position]
    board[position] = 0
    position += 1

    return seeds, board, position



def make_play(player_1_or_2:int, position:int, board:list[int]) -> list:
    keep_playing:bool = 0
    game_is_finished:bool = 0
    
    seeds, board, position = start_move(board, position)

    for i in range(1, seeds + 1):
        if (player_1_or_2 == 2 and position == 6) or (player_1_or_2 == 1 and position == 13):
            position += 1

        try:
            board[position] += 1
            if i == seeds: # verificar se na última jogada, o jogador tem direito a uma jogada especial
                game_is_finished = ver.verify_if_game_is_finnished(board)
                if game_is_finished == 0:
                    board, keep_playing = ver.verify_specials_moves(player_1_or_2, position, board, keep_playing)
                    game_is_finished = ver.verify_if_game_is_finnished(board)
            position += 1
        except:
            position = 0
            board[position] += 1
            if i == seeds: # verificar se na última jogada, o jogador tem direito a uma jogada especial
                game_is_finished = ver.verify_if_game_is_finnished(board)
                if game_is_finished == 0:
                    board, keep_playing = ver.verify_specials_moves(player_1_or_2, position, board, keep_playing)
                    game_is_finished = ver.verify_if_game_is_finnished(board)
            position += 1

    return board, keep_playing, game_is_finished



def make_play_with_position_in_front(player_1_or_2:int, position:int, position_in_front:int, board:list) -> list:
    if player_1_or_2 == 1:
        board[6] = board[position_in_front] + board[position] + board[6]
        board[position_in_front] = 0
        board[position] = 0 

    elif player_1_or_2 == 2:
            board[13] = board[position_in_front] + board[position] + board[13]
            board[position_in_front] = 0
            board[position] = 0 

    return board



def finish_game(players:dict, game_status:list):
    player1:str = game_status[0]
    player2:str = game_status[1]
    board = game_status[3]
    
    seeds_player1 = board[6] + board[0] + board[1] + board[2] + board[3] + board[4] + board[5]
    seeds_player2 = board[13] + board[7] + board[8] + board[9] + board[10] + board[11] + board[12]

    if seeds_player1 > seeds_player2:
       data.set_player_victory(player1, players)
       data.set_player_lost(player2, players)

    elif seeds_player2 > seeds_player1:
        data.set_player_victory(player2, players)
        data.set_player_lost(player1, players)

    elif seeds_player1 == seeds_player2:
        data.set_player_tie(player1, player2, players)

    cli.finish_game(player1, seeds_player1, seeds_player2, game_status)

    data.reset_game_status(game_status)

    return players, game_status



def normal_ai_play(player1_or_player2:int, board:list) -> bool:
    position = 7
    keep_playing = 0

    while board[position] == 0 and position in range(12, 8):
        position += 1

    make_play(player1_or_player2, position, board)

    return keep_playing



def advanced_ai_play(player1_or_player2:int, board:list) -> bool:
    full_circle:bool = 0
    enougt_seeds:bool = 0
    keep_playing:bool = 0
    position_to_play:int = 7

    full_circle, position_to_play = tools.can_it_go_full_circle(board)

    if full_circle == 1:
        make_play(player1_or_player2, position_to_play, board)
   
    elif full_circle == 0:
        enougt_seeds, position_to_play = tools.is_there_enought_seeds(board)
        if enougt_seeds == 1 :
            make_play(player1_or_player2, position_to_play, board)

        elif full_circle == 0 and enougt_seeds == 0:
            keep_playing, position_to_play = tools.can_it_replay(board)
            if keep_playing == 1:
                make_play(player1_or_player2, position_to_play, board)

            elif full_circle == 0 and enougt_seeds == 0 and keep_playing == 0:
                position = 12

                while board[position] == 0 and position in range(7, 13):
                    position -=1

                make_play (player1_or_player2, position, board)

    return keep_playing