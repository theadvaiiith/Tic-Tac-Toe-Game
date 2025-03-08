import tkinter as tk
from tkinter import messagebox
import math

root = tk.Tk()
root.title("Tic-Tac-Toe")

board = [
    [' ', ' ', ' '],
    [' ', ' ', ' '],
    [' ', ' ', ' ']
]

current_player = 'X'
move_history = []

def is_moves_left(board):
    for row in board:
        if ' ' in row:
            return True
    return False

def evaluate(board):
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] != ' ':
            if board[row][0] == 'X':
                return 1
            elif board[row][0] == 'O':
                return -1

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != ' ':
            if board[0][col] == 'X':
                return 1
            elif board[0][col] == 'O':
                return -1

    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != ' ':
        if board[0][0] == 'X':
            return 1
        elif board[0][0] == 'O':
            return -1

    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != ' ':
        if board[0][2] == 'X':
            return 1
        elif board[0][2] == 'O':
            return -1

    return 0

def minimax(board, depth, is_max):
    score = evaluate(board)
    if score == 1:
        return score - depth  
    if score == -1:
        return score + depth  
    if not is_moves_left(board):
        return 0  

    if is_max:
        best = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    best = max(best, minimax(board, depth + 1, False))
                    board[i][j] = ' '  
        return best
    else:
        best = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    best = min(best, minimax(board, depth + 1, True))
                    board[i][j] = ' '  
        return best

def find_best_move(board):
    best_val = -math.inf
    best_move = (-1, -1)

    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'X'
                move_val = minimax(board, 0, False)
                board[i][j] = ' '  

                if move_val > best_val:
                    best_move = (i, j)
                    best_val = move_val

    return best_move

def button_click(row, col):
    global current_player

    if board[row][col] == ' ':
        board[row][col] = current_player
        buttons[row][col].config(text=current_player, fg='white', font=('normal', 40, 'bold'))
        move_history.append((row, col))

        if evaluate(board) == 1:
            messagebox.showinfo("Game Over", "Player X wins!")
            reset_board()
        elif evaluate(board) == -1:
            messagebox.showinfo("Game Over", "Player O wins!")
            reset_board()
        elif not is_moves_left(board):
            messagebox.showinfo("Game Over", "It's a draw!")
            reset_board()
        else:
            current_player = 'O' if current_player == 'X' else 'X'

def reset_board():
    global board, current_player, move_history
    board = [
        [' ', ' ', ' '],
        [' ', ' ', ' '],
        [' ', ' ', ' ']
    ]
    current_player = 'X'
    move_history = []
    for row in range(3):
        for col in range(3):
            buttons[row][col].config(text=' ', bg='black')

def undo_move():
    if move_history:
        row, col = move_history.pop()
        board[row][col] = ' '
        buttons[row][col].config(text=' ', bg='black')
        global current_player
        current_player = 'O' if current_player == 'X' else 'X'

buttons = [[None for _ in range(3)] for _ in range(3)]
for row in range(3):
    for col in range(3):
        buttons[row][col] = tk.Button(root, text=' ', font=('normal', 40), width=5, height=2, bg='black',
                                      command=lambda row=row, col=col: button_click(row, col))
        buttons[row][col].grid(row=row, column=col)

undo_button = tk.Button(root, text='Undo', font=('normal', 20), command=undo_move)
undo_button.grid(row=3, column=1)

print("GUI created successfully")

root.mainloop()