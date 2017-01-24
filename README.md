# Ice-Puzzle
This is an ice puzzle solver written in Python. In an ice puzzle, there is a frozen, square pond. The goal is to find the shortest path from any starting position to the exit. However, since the pond is frozen, movement in any NEWS direction will continue until hitting the edge of the pond or a rock. 

Each test text file represents a different frozen pond. Some files test edge cases while others are simply more complex, yet solvable puzzles. Each text file represents the puzzle with . as empty spaces and * as rocks. The first line of each file contains three separate numbers. The first two are the height and width of the puzzle, while the last number is the row number that contains the exit. All exits are assumed to be on the right hand side.

heap.py is a heap that has been modified by Prof. Adam Purtee from code originally posted by Prof. Sean Strout at Rochester Institute of Technology's Computer Science Department. It has been modified to optimize Dijkstra's Algorithm.   

escape.py implements a version of Dijsktra's Algorithm to solve the ice puzzle. It does so by finding all possible paths to the exit from the given starting position and keeps track of the shortest path, that is the path with the fewest movements. So, rather than finding the shortest path by keeping track of a shortest distance value, this version keeps track of the path that required the fewest movements. 
