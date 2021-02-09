#include <iostream>
#include <string>
#include <iostream>
#include <fstream>



int main(int argc, char *argv[]){
	/*
	Input: txt file with maze layout and txt file to store the maze solver
	First, the maze is created as a static 2D array, and all 0's are empty cells,
	while 1's are wall indicator.

	Using right hand following algorithm, the solution is created.
	i.e., having a direction of motion for an agent we follow a wall on the right and
	move towards cells where there is no wall.
	Once the last row is achieved, the agent stops.

	Output: void, but the solution for maze stored in txt file
	*/
	if (argc != 3){
		// Tell the user how to run the program
        std::cout << "Usage: \n ./mazesolver <maze file> <solution file>" << std::endl;
        return 1;
	}

	std::string maze_file = argv[1];
	std::string sol_file = argv[2];

	const int max_size = 201;
	int maze [max_size][max_size];
	int m,n;

	std::fstream f;
	int i = 0; 
	int j = 0;

	f.open(maze_file);
	if (f.is_open()){
		f >> m >> n;
		if (m > max_size or n>max_size){
			std::cout << "Not enought storage space for the maze array" << std::endl;
			return 1;
		}
		// populate static array with 0s
		for (i=0; i<m; i++){
			for ( j=0; j<n; j++){
				maze[i][j] = 0;
			}
		}
		while (f >> i >> j){
			// put 1 to inxicate the  wall
			maze[i][j] = 1;
		}

	}else{
		std::cout << "Failed to open maze file" << std::endl;
		return 1;
	}
	f.close();

	// write into a solution file
	f.open(sol_file, std::ofstream::out | std::ofstream::trunc);
	if (f.is_open()){
		// find the entrance to maze, index for first 0 element
		i=0; j=0;
		while (j < n and maze[i][j] == 1){
			++j;
		}
		if (j == n){
			std::cout << "Maze does not have an entrance in the top row" << std::endl;
			return 1;
		}

		char dir = 'd'; // direction of the maze solverm

		while (i < m-1){
			f << i << " " << j << std::endl;
			if (i == 0){
				// if currently in the first row
				if (i < m-1 and maze[i+1][j] == 0){ 
					++i;
					dir = 'd';
				}
			}else{
					switch (dir) {
						case 'd': {
							// if current direction is down, start finding exit by first turning left, proceed counterclockwise
							if (j > 0 and maze[i][j-1]==0){
								--j;
								dir = 'l';
							}else if (i < m-1 and maze[i+1][j] == 0){ 
								++i;
								dir = 'd';
							}else if (j < n-1 and maze[i][j+1] == 0){ 
								++j;
								dir = 'r';
							}else if (i > 0 and maze[i-1][j] == 0){ 
								--i;
								dir = 'u';
									}
							break;
						}
						case 'r': {
							// if current direction is right, start finding exit by first turning down, proceed counterclockwise
							if (i < m-1 and maze[i+1][j] == 0){ 
								++i;
								dir = 'd';
							}else if (j < n-1 and maze[i][j+1] == 0){ 
								++j;
								dir = 'r';
							}else if (i > 0 and maze[i-1][j] == 0){ 
								--i;
								dir = 'u';
							}else if (j > 0 and maze[i][j-1]==0){
								--j;
								dir = 'l';
							}
							break;
						}
						case 'u': {
							// if current direction is up, start finding exit by first turning right, proceed counterclockwise
							if (j < n-1 and maze[i][j+1] == 0){ 
								++j;
								dir = 'r';
							}else if (i > 0 and maze[i-1][j] == 0){ 
								--i;
								dir = 'u';
							}else if (j > 0 and maze[i][j-1]==0){
								--j;
								dir = 'l';
							}else if (i < m-1 and maze[i+1][j] == 0){ 
								++i;
								dir = 'd';
							} 
							break;
						}
						case 'l': {
							// if current direction is left, start finding exit by first turning up, proceed counterclockwise
							if (i > 0 and maze[i-1][j] == 0){ 
								--i;
								dir = 'u';
							}else if (j > 0 and maze[i][j-1]==0){
								--j;
								dir = 'l';
							}else if (i < m-1 and maze[i+1][j] == 0){ 
								++i;
								dir = 'd';
							}else if (j < n-1 and maze[i][j+1] == 0){ 
								++j;
								dir = 'r';
							} 
							break;
						}
					}
				

			}
		}

		f << i << " " << j << std::endl;


	}else{
		std::cout << "Failed to open solution file" << std::endl;
		return 1;
	}
	f.close();


	return 0;
}