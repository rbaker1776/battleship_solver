#include <ctime>
#include <cstdlib>



constexpr int height = 9;
constexpr int width = 9;

constexpr int num_ships = 8;
constexpr int ship_sizes[num_ships] = { 3, 3, 3, 3, 3, 5, 5, 5 };

enum class Cell
{
	EMPTY = 0,
};

Cell board[height][width] = {{ Cell::EMPTY }};


void place_ships()
{
	srand(time(NULL));

	for (int ship = 0; ship < num_ships; ++ship)
	{
		bool placed = false;
		while (!placed)
		{
			int x = rand() % B
}


int main()
{
	return 0;
}

