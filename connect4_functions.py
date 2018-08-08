#!/usr/bin/env python
# -*- coding: utf-8 -*-


def c4_check(board):
    check_conditions = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6],
                        [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6],
                        [2, 0], [2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6],
                        [3, 0], [3, 1], [3, 2], [3, 3], [3, 4], [3, 5], [3, 6],
                        [4, 0], [4, 1], [4, 2], [4, 3], [4, 4], [4, 5], [4, 6],
                        [5, 0], [5, 1], [5, 2], [5, 3], [5, 4], [5, 5], [5, 6]]

    winner = 0
    for i in check_conditions:
        player_check = board[i[1]][i[0]]
        if player_check != 0:

            # vertical
            if i[0] < 3:
                if board[i[1]][i[0]+1] == player_check and board[i[1]][i[0]+2] == player_check and board[i[1]][i[0]+3] == player_check:
                    winner = player_check
                    break

            # horizontal
            if i[1] < 4:
                if board[i[1]+1][i[0]] == player_check and board[i[1]+2][i[0]] == player_check and board[i[1]+3][i[0]] == player_check:
                    winner = player_check
                    break

            # diagonal down
            if i[1] < 4 and i[0] < 3:
                if board[i[1]+1][i[0]+1] == player_check and board[i[1]+2][i[0]+2] == player_check and board[i[1]+3][i[0]+3] == player_check:
                    winner = player_check
                    break

            # diagonal up
            if i[1] < 4 and i[0] > 2:
                if board[i[1]+1][i[0]-1] == player_check and board[i[1]+2][i[0]-2] == player_check and board[i[1]+3][i[0]-3] == player_check:
                    winner = player_check
                    break

            # draw
            if board[0][0] != 0 and board[1][0] != 0 and board[2][0] != 0 and board[3][0] != 0 and board[4][0] != 0 and board[5][0] != 0 and board[6][0] != 0:
                return 'draw'

    return winner


def print_board(board):
    line = ""
    for i in range(0, 6):
        for j in range(0, 7):
            if board[j][i] == 0:
                 line += ":white_circle:"
            elif board[j][i] == 1:
                line += ":red_circle:"
            else:
                line += ":large_blue_circle:"
        line += "\n"
    return line
