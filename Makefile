CC = g++
STD = -std=c++20
CFLAGS = -Wall -Wextra -Werror -pedantic -O0

SRC = battleship.cpp

run: $(SRC)
	$(CC) $(STD) $(CFLAGS) $(SRC) $(TEST) -o battleship && ./battleship
