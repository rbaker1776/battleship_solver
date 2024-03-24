import numpy as np
import random
import time



dimension = 9
board = np.zeros((dimension, dimension), dtype=int)
gamestate = np.zeros((dimension, dimension), dtype=int)
probabilities = np.zeros((dimension, dimension), dtype=float)

directions = ["NORTH", "EAST", "SOUTH", "WEST"]

EMPTY = 0
SUNK = 1
PADDED = 2
HIT = 3
MISS = 4

ships =\
{
    "Linear-1": 0,
    "Linear-2": 0,
    "Linear-3": 5,
    "Linear-4": 3,
    "Linear-5": 0,
}

ship_sizes =\
{
    "Linear-1": 1,
    "Linear-2": 2,
    "Linear-3": 3,
    "Linear-4": 4,
    "Linear-5": 5,
}


def place_all_ships() -> bool:
    global ships

    ships_list = []
    for key, value in ships.items():
        ships_list.extend([key] * value)
    random.shuffle(ships_list)

    for ship in ships_list:
        success = place_ship(ship)

        if not success:  # ship could not be placed
            return False

    return True


def place_ship(ship: str) -> bool:
    global board
    global dimension
    global directions

    hit_squares = [(i, j) for i in range(dimension) for j in range(dimension) if board[i][j] == HIT]
    empty_squares = [(i, j) for i in range(dimension) for j in range(dimension) if board[i][j] == EMPTY]

    random.shuffle(hit_squares)
    random.shuffle(empty_squares)
    random.shuffle(directions)

    offsets = list(range(ship_sizes[ship]))
    random.shuffle(offsets)

    for square in hit_squares:
        row = square[0]
        col = square[1]

        for direction in directions:
            if direction in ["NORTH", "SOUTH"]:
                for offset in offsets:
                    if row + ship_sizes[ship] - offset > dimension or row - offset < 0:
                        continue
                     
                    if any(board[i][col] not in [EMPTY, HIT] for i in range(row - offset, row + ship_sizes[ship] - offset)):
                        continue
                   
                    for i in range(row - offset, row + ship_sizes[ship] - offset):
                        board[i][col] = SUNK

                    pad_board()  
                    return True

            elif direction in ["EAST", "WEST"]:
                for offset in offsets:
                    if col + ship_sizes[ship] - offset > dimension or col - offset < 0:
                        continue
                            
                    if any(board[row][i] not in [EMPTY, HIT] for i in range(col - offset, col + ship_sizes[ship] - offset)):
                        continue

                    for i in range(col - offset, col + ship_sizes[ship] - offset):
                        board[row][i] = SUNK

                    pad_board()
                    return True


    for square in empty_squares:
        row = square[0]
        col = square[1]

        for direction in directions:
            if direction == "NORTH":
                if (row < ship_sizes[ship] - 1) or any(
                        board[i][col] != EMPTY for i in range(row, row - ship_sizes[ship], -1)):
                    continue

                for i in range(ship_sizes[ship]):
                    board[row - i][col] = SUNK 

                pad_board()
                return True

            elif direction == "EAST":
                if (col > dimension - ship_sizes[ship]) or any(
                        board[row][j] != EMPTY for j in range(col, col + ship_sizes[ship])):
                    continue

                for i in range(ship_sizes[ship]):
                    board[row][col + i] = SUNK 

                pad_board()
                return True

            elif direction == "SOUTH":
                if (row > dimension - ship_sizes[ship]) or any(
                        board[i][col] != EMPTY for i in range(row, row + ship_sizes[ship])):
                    continue

                for i in range(ship_sizes[ship]):
                    board[row + i][col] = SUNK
                
                pad_board()
                return True

            elif direction == "WEST":
                if (col < ship_sizes[ship] - 1) or any(
                        board[row][j] != EMPTY for j in range(col, col - ship_sizes[ship], -1)):
                    continue

                for i in range(ship_sizes[ship]):
                    board[row][col - i] = SUNK

                pad_board()
                return True

    return False


def pad_board() -> None:

    global gamestate

    for row in range(dimension):
        for col in range(dimension):
            if gamestate[row, col] != EMPTY:
                continue

            for x in range(max(0, row - 1), min(dimension, row + 2)):
                for y in range(max(0, col - 1), min(dimension, col + 2)):
                    if (x != row or y != col) and gamestate[x, y] == SUNK:
                        gamestate[row, col] = PADDED
                        break
                else:
                    continue

                break


def print_board() -> None:
    """ attempted format:
    A) . . . .
    B) X X X .
    C) . . . .
    D) . . . .
       1 2 3 4
    """

    global board
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    markers = ['.', '#', '-', 'X', 'O']

    for row in range(dimension):
        print("{}) ".format(alphabet[row]), end="")
        for col in range(dimension):
            print(markers[board[row][col]], end=" ")
        print("\n", end="")

    print("   ", end="")
    for col in range(dimension):
        print(f"{col + 1:01}", end=" ")

    print("\n")


def reset_board() -> None:
    global board
    global gamestate

    board = gamestate.copy()


def calculate_probabilities() -> None:

    global board
    global probabilities
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    num_iter = 0
    probabilities = np.zeros((dimension, dimension), dtype=int)

    start = time.time()
    while (time.time() < start + 1):
        num_iter += 1
        success: bool = False

        while not success:
            reset_board()
            success = place_all_ships() 

        for row in range(dimension):
            for col in range(dimension):
                if board[row, col] == SUNK and gamestate[row, col] == EMPTY:
                    probabilities[row, col] += 1

    best_square = np.argmax(probabilities)
    best_row, best_col = np.unravel_index(best_square, probabilities.shape)

    for row in range(dimension):
        print("{}) ".format(alphabet[row]), end="")
        for col in range(dimension):
            if row == best_row and col == best_col:
                print("\x1b[33m", end = "")
            print((f"{min(int(probabilities[row, col] * 100 / num_iter), 99):02}\x1b[0m"), end = " ")
        print("\n", end = "")

    print("    ", end = "")
    for col in range(dimension):
        print(f"{col+1:01}  ", end = "")

    print("\n\n", end = "")
    print(f"Best Square: {alphabet[best_row]}{best_col + 1}")
    print(f"{(probabilities[best_row, best_col] * 100 / num_iter):.2f}% chance of hit")
    print(f"{num_iter} positions searched")

    reset_board()


def sink_ship(row, col) -> None: 
    if row < 0 or row >= dimension or col < 0 or col >= dimension or gamestate[row, col] != HIT:
        return

    gamestate[row, col] = SUNK

    sink_ship(row - 1, col)
    sink_ship(row + 1, col)
    sink_ship(row, col - 1)
    sink_ship(row, col + 1)

    reset_board()


def accept_input() -> None:
    print()
    print()
    print()
    event = input("Enter the game event: ")
    try:
        square, action = event.split(" ")
        row, col = str(square[0]), int(square[1])
        row = ord(row) - ord('A')
        col -= 1

        if action == "hit":
            gamestate[row, col] = HIT

        elif action == "miss":
            gamestate[row, col] = MISS

        elif action == "sink":
            gamestate[row, col] = HIT
            sink_ship(row, col) 
            pad_board()


    except:
        print("Error: invalid input.")
        print("Please enter an event in square-action format.")
        print("For example: A1 hit")
        print("Acceptable actions are: hit, miss, sink")
        print()
        accept_input()


def main():
    while True:
        calculate_probabilities()
        print_board()
        accept_input()


if __name__ == "__main__":
    main()

