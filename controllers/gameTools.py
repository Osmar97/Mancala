from controllers import verifyGame as ver
from controllers import gameTools as tools
from models import data
from views import cli as cli


def get_board_index_for_inputed_position(player1_or_player2:int, position:int) -> int:
    if player1_or_player2 == 1:
        position -= 1
    else:
        position += 6

    return position



def get_position_in_front(player_1_or_2:int, position:int) -> int:
    position_in_front:int

    if player_1_or_2 == 1:
        position_in_front = (7 - (position + 1)) + 6
    else:
        position_in_front = 12 - position

    return position_in_front



def can_it_go_full_circle(board: list) -> bool:
    for position in range (7,13):
        if board[position] in [13, 26, 39]:
            full_circle: bool = 1
            break
        else:
            full_circle = 0

    return full_circle, position



def is_there_enought_seeds(board: list):
    initial_position = 7
    enougth_seeds: bool = 0
    position_to_play: int = 0


    for i in range (7,13):
        if enougth_seeds == 1:
                break
     
        if board[i] == 0:
            position = i
            position_diference = position - initial_position

            if position_diference > 0:
                for j in range (position_diference):
                    seeds = board[initial_position]

                    if seeds == position_diference:
                        enougth_seeds = 1
                        position_to_play = initial_position
                        break
                    else:
                        initial_position += 1

                if enougth_seeds == 0:
                    position_diference = position + 1

                    for j in range (position_diference, 13):
                        seeds = board[position_diference]

                        if seeds == 13 - (position_diference - position):
                            enougth_seeds: bool = 1
                            position_to_play = position_diference
                            break
                        else:
                            position_diference += 1

    return enougth_seeds, position_to_play



def can_it_replay(board: list):
    keep_playing: bool = 0
    position_to_play: int = 7

    for position in range (7, 13):
        seeds = board[position]

        if (position + seeds) == 13:
            position_to_play = position
            keep_playing = 1
            break

    return keep_playing, position_to_play



def quit_game_d(user_input:list, players:dict, game_status:list):
    player_list:list[str] = []
    i:int = 0 # variable control

    game_is_not_on : bool = ver.verify_if_game_is_on(game_status)
    if game_is_not_on == 0:
        cli.print_message("Não existe jogo em curso.")

    for j in range(1,len(user_input)):
        player_list.append(user_input[j])

        player_doesnt_exit : bool = ver.verify_if_players_exists(player_list[i], players)
        if player_doesnt_exit == 1:
            cli.print_message("Jogador inexistente.")
            break

        player_playing : bool = ver.verify_if_choosed_player_is_gaming(player_list[i] , game_status)
        if player_playing == 0:
            cli.print_message("Jogador não participa no jogo em curso.")
            break 

        i += 1

    if game_is_not_on == 1 and player_doesnt_exit == 0 and player_playing == 1:
        if len(player_list) == 1:
            player_lost:str = 0

            player_lost:int = ver.verify_if_player1_or_2(player_list[0], game_status)

            if player_lost == 1:
                data.set_player_lost (player_list[0], players)
                data.set_player_victory(game_status[1], players)
            else:
                data.set_player_lost (player_list[0], players)
                data.set_player_victory(game_status[0], players)
        else:
             data.set_player_lost (player_list[0], players)
             data.set_player_lost (player_list[1], players)

        data.reset_game_status(game_status)

    return players, game_status