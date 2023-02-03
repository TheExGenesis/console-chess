"""
Unicode chess symbols

# 8	♜	♞	♝	♛	♚	♝	♞	♜
# 7	♟︎	 ♟︎	  ♟︎   ♟︎	♟︎	 ♟︎   ♟︎   ♟
# 6	
# 5	
# 4	
# 3	
# 2	♙	♙	♙	♙	♙	♙	♙	♙
# 1	♖	♘	♗	♕	♔	♗	♘	♖
#   a	 b	  c    d	e	f	 g	  h

"""
from stockfish import Stockfish


WHITE = 1
BLACK = 0


def make_white_square(char):
    return f"\033[48;5;15m {char} \033[0m"


def make_black_square(char):
    return f"\033[48;5;7m {char} \033[0m"


def is_cell_black(row, col):
    return (row + col) % 2 == 0


def make_printable_cell(cell, row, col):
    piece = cell
    # piece = map_piece_to_unicode(cell)
    if is_cell_black(row, col):
        return make_black_square(piece)
    else:
        return make_white_square(piece)


def map_piece_to_unicode(piece):
    if piece == " ":
        return " "
    elif piece == "p":
        return "♟︎"
    elif piece == "P":
        return "♙"
    elif piece == "r":
        return "♜"
    elif piece == "R":
        return "♖"
    elif piece == "n":
        return "♞"
    elif piece == "N":
        return "♘"
    elif piece == "b":
        return "♝"
    elif piece == "B":
        return "♗"
    elif piece == "q":
        return "♛"
    elif piece == "Q":
        return "♕"
    elif piece == "k":
        return "♚"
    elif piece == "K":
        return "♔"
    else:
        return " "


def print_board(board):
    print("   a  b  c  d  e  f  g  h")
    for row in range(8):
        print(f"{8 - row} ", end="")
        for col in range(8):
            printable_cell = make_printable_cell(board[row][col], row, col)
            print(f"{printable_cell}", end="")
        print(f" {8 - row}")
    print("   a  b  c  d  e  f  g  h")


def print_board_with_black_and_white_squares(board):
    """colors emp"""


def create_board():
    board = []
    for row in range(8):
        board.append([])
        for col in range(8):
            board[row].append(" ")
    return board


def set_board(board):
    board[0] = ["r", "n", "b", "q", "k", "b", "n", "r"]
    board[1] = ["p"] * 8
    board[6] = ["P"] * 8
    board[7] = ["R", "N", "B", "Q", "K", "B", "N", "R"]
    return board


def move_piece(board, start, end):
    """start and end are tuples (row, col)"""
    start_row, start_col = start
    end_row, end_col = end
    board[end_row][end_col] = board[start_row][start_col]
    board[start_row][start_col] = " "
    return board


def translate_move(move):
    """translate move from algebraic notation to tuple
    e.g. e2e4 -> (4, 4), (4, 5)
    """
    start_col = ord(move[0]) - ord("a")
    start_row = 8 - int(move[1])
    end_col = ord(move[2]) - ord("a")
    end_row = 8 - int(move[3])
    return (start_row, start_col), (end_row, end_col)


def is_valid_pawn_move(board, start, end):
    start_row, start_col = start
    end_row, end_col = end
    if board[start_row][start_col] == "P":
        if start_col == end_col:
            if start_row - end_row == 1:
                return True
            elif start_row == 6 and start_row - end_row == 2:
                return True
        elif abs(start_col - end_col) == 1:
            if start_row - end_row == 1:
                return True
    elif board[start_row][start_col] == "p":
        if start_col == end_col:
            if end_row - start_row == 1:
                return True
            elif start_row == 1 and end_row - start_row == 2:
                return True
        elif abs(start_col - end_col) == 1:
            if end_row - start_row == 1:
                return True
    return False


def is_valid_rook_move(board, start, end):
    start_row, start_col = start
    end_row, end_col = end
    if start_col == end_col:
        if start_row < end_row:
            for row in range(start_row + 1, end_row):
                if board[row][start_col] != " ":
                    return False
        else:
            for row in range(end_row + 1, start_row):
                if board[row][start_col] != " ":
                    return False
        return True
    elif start_row == end_row:
        if start_col < end_col:
            for col in range(start_col + 1, end_col):
                if board[start_row][col] != " ":
                    return False
        else:
            for col in range(end_col + 1, start_col):
                if board[start_row][col] != " ":
                    return False
        return True
    return False


def is_valid_knight_move(board, start, end):
    start_row, start_col = start
    end_row, end_col = end
    if abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1:
        return True
    elif abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2:
        return True
    return False


def is_valid_bishop_move(board, start, end):
    start_row, start_col = start
    end_row, end_col = end
    if abs(start_row - end_row) == abs(start_col - end_col):
        if start_row < end_row and start_col < end_col:
            for i in range(1, abs(start_row - end_row)):
                if board[start_row + i][start_col + i] != " ":
                    return False
        elif start_row < end_row and start_col > end_col:
            for i in range(1, abs(start_row - end_row)):
                if board[start_row + i][start_col - i] != " ":
                    return False
        elif start_row > end_row and start_col < end_col:
            for i in range(1, abs(start_row - end_row)):
                if board[start_row - i][start_col + i] != " ":
                    return False
        elif start_row > end_row and start_col > end_col:
            for i in range(1, abs(start_row - end_row)):
                if board[start_row - i][start_col - i] != " ":
                    return False
        return True
    return False


def is_valid_queen_move(board, start, end):
    return is_valid_rook_move(board, start, end) or is_valid_bishop_move(
        board, start, end
    )


def is_valid_king_move(board, start, end):
    start_row, start_col = start
    end_row, end_col = end
    if abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1:
        return True
    return False


def is_valid_move(board, start, end):
    start_row, start_col = start
    end_row, end_col = end
    if board[start_row][start_col] == "P" or board[start_row][start_col] == "p":
        return is_valid_pawn_move(board, start, end)
    elif board[start_row][start_col] == "R" or board[start_row][start_col] == "r":
        return is_valid_rook_move(board, start, end)
    elif board[start_row][start_col] == "N" or board[start_row][start_col] == "n":
        return is_valid_knight_move(board, start, end)
    elif board[start_row][start_col] == "B" or board[start_row][start_col] == "b":
        return is_valid_bishop_move(board, start, end)
    elif board[start_row][start_col] == "Q" or board[start_row][start_col] == "q":
        return is_valid_queen_move(board, start, end)
    elif board[start_row][start_col] == "K" or board[start_row][start_col] == "k":
        return is_valid_king_move(board, start, end)
    return False


def is_piece_white(board, start, end):
    start_row, start_col = start
    end_row, end_col = end
    if (
        board[start_row][start_col] == "P"
        or board[start_row][start_col] == "R"
        or board[start_row][start_col] == "N"
        or board[start_row][start_col] == "B"
        or board[start_row][start_col] == "Q"
        or board[start_row][start_col] == "K"
    ):
        return True
    return False


def is_valid_move_color(board, start, end, player_color):
    # white=1, black=0
    if player_color == 1:
        if is_piece_white(board, start, end):
            return True
        return False
    elif player_color == 0:
        if not is_piece_white(board, start, end):
            return True
        return False
    return False


def is_game_over(board):
    white_king = False
    black_king = False
    for row in range(8):
        for col in range(8):
            if board[row][col] == "K":
                white_king = True
            elif board[row][col] == "k":
                black_king = True
    if white_king and black_king:
        return False
    return True


def does_white_win(board):
    for row in range(8):
        for col in range(8):
            if board[row][col] == "k":
                return False
    return True


def is_input_valid(move):
    move = move.strip().lower()
    if len(move) != 4:
        return False
    if move[0] not in "abcdefgh":
        return False
    if move[1] not in "12345678":
        return False
    if move[2] not in "abcdefgh":
        return False
    if move[3] not in "12345678":
        return False
    return True


def white_turn(board):
    while True:
        white_move = input("White's move:")
        if is_input_valid(white_move):
            start, end = translate_move(white_move)
            if is_valid_move_color(board, start, end, WHITE) and is_valid_move(
                board, start, end
            ):
                break
            else:
                print("Invalid move. Try again.")
        else:
            print(f"Invalid input {white_move}. Try again.")
    board = move_piece(board, start, end)
    return board, white_move


def black_turn(board):
    while True:
        black_move = input("Black's move:")
        if is_input_valid(black_move):
            start, end = translate_move(black_move)
            if is_valid_move_color(board, start, end, BLACK) and is_valid_move(
                board, start, end
            ):
                break
            else:
                print("Invalid move. Try again.")
        else:
            print(f"Invalid input {black_move}. Try again.")
    board = move_piece(board, start, end)
    return board, black_move


def stockfish_turn(stockfish, board, history):
    # stockfish.set_fen_position(board_to_fen(board))
    stockfish.make_moves_from_current_position(history)
    move = stockfish.get_best_move()
    start, end = translate_move(move)
    board = move_piece(board, start, end)
    return board, move


def main(p2_AI=True):
    stockfish = Stockfish()
    move_input_history = []
    board = create_board()
    board = set_board(board)
    print_board(board)
    while True:

        board, move_input = white_turn(board)
        move_input_history.append(move_input)
        print_board(board)

        if p2_AI:
            board, move_input = stockfish_turn(board)
            move_input_history.append(move_input)
            print_board(board)

        else:
            board, move_input = black_turn(board)
            move_input_history.append(move_input)
            print_board(board)

        if is_game_over(board):
            if does_white_win(board):
                print("White wins!")
            else:
                print("Black wins!")
            break


main()
