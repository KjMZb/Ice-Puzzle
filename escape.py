"""
This module reads a text file to create a frozen
pond puzzle and then solves it for every position
using Djikstra's Algorithm. The implementation of
Djikstra's Algorithm is taken from the code cited
below and modified so as to find the shortest
path from the starting position to the exit of
the pond.

CSCI-603: Graphs
Authors:  (11/16/2016) Adam Purtee @ RIT CS
                       -- added hasPath, pathFinder, and findDJI
          (Original Version) Sean Strout @ RIT CS
"""

__author__ = 'Amit Maller', 'Kyle McGlynn'

import heap

class Node(object):
    """
    This class is used to represent a position of a
    frozen pond puzzle in a graph representation of that
    puzzle.
    """

    __slots__ = 'row','column','left', 'right', 'up', 'down'

    def __init__ ( self, row=0, column=0, left = None, right = None,
                   up = None, down = None ):
        """
        The initialization method. Every value is, by default, set
        to zero or None.
        :param row: The row value of this position
        :param column: The column value of this position
        :param left: The node representing the position to the left
        :param right: The node representing the position to the right
        :param up: The node representing the position above
        :param down: The node representing the position below
        :return: None
        """
        self.row = row
        self.column = column
        self.left = left
        self.right = right
        self.up = up
        self.down = down

    def __str__(self):
        """
        This method returns a string representation of this node
        as a pair of x ( column ) and y ( row ) coordinates.
        :return: A string representation of this node.
        """
        return "(" + str(self.column) + ", " + str(self.row) + ")"

def readTest( fileName ):
    """
    This function reads the dimensions, properties, and layout
    of the frozen pond puzzle from a text file and returns
    those values.
    :param fileName: The name of the file we want to read from
    :return: The dimensions, properties, and layout of the
            frozen pond puzzle
    """

    # Open the file
    with open( fileName ) as file:

        # Get the lines of the file
        lines = file.readlines()

        # Get the dimensions and escape row
        numbers = lines[0].split()
        height = int(numbers[0])
        width = int(numbers[1])
        escape = int(numbers[2])

        # Create a 2d array to hold the textual representation of the puzzle
        text = [[' ' for column in range(width)] for row in range(height)]
        for line in range( height):
            text[line] = list(lines[line+1])

    return height, width, escape, text

def buildPuzzle( puzzleText, puzzleWidth,
                 puzzleHeight, escapeRow ):
    """
    This function builds a 2d array of nodes that serves as a
    representation of the frozen pond puzzle.

    Note, we assume that the escape position is always on the
    right side of the puzzle.

    :param puzzleText: the text representing the puzzle as
                       a 2d array of strings
    :param puzzleWidth: the width of the puzzle
    :param puzzleHeight: the height of the puzzle
    :param escapeRow: the row where the escape node is located
    :return: the 2d array of nodes that represents the puzzle
    """

    # Puzzle represented as a 2d array of nodes
    puzzle =[[None for column in range(puzzleWidth+1)] for row in range(puzzleHeight)]

    # Loop over the positions in the text of the puzzle
    for row in range( puzzleHeight ):
        for column in range( puzzleWidth ):

            # If the position in the text is not a rock ( '*' )
            if puzzleText[row][column] == '.':

                position = Node(row,column)

                # Check left, right, up, and down
                if column - 1 >= 0 and puzzleText[row][column - 1] == '.':
                    position.left = puzzle[row][column - 1]
                    if puzzle[row][column - 1] != None:
                        puzzle[row][column - 1].right = position

                if column + 1 < puzzleWidth and puzzleText[row][column + 1] == '.':
                    position.right = puzzle[row][column + 1]
                    if puzzle[row][column + 1] != None:
                        puzzle[row][column + 1].left = position

                if row - 1 >= 0 and puzzleText[row - 1][column] == '.':
                    position.up = puzzle[row - 1][column]
                    if puzzle[row - 1][column] != None:
                        puzzle[row - 1][column].down = position

                if row + 1 < puzzleHeight and puzzleText[row + 1][column] == '.':
                    position.down = puzzle[row + 1][column]
                    if puzzle[row + 1][column] != None:
                        puzzle[row + 1][column].up = position

                # If we have reached the spot to place the escape node
                if column == puzzleWidth-1 and row == escapeRow:
                    puzzle[escapeRow][column+1] = Node(escapeRow, column+1)
                    position.right = puzzle[escapeRow][column + 1]

                puzzle[row][column] = position
    return puzzle

def slide( start, direction):
    """
    This function simulates sliding along a frozen
    pond from a starting position until hitting
    a rock or the edge of the pond.
    :param start: The starting position
    :param direction: The direciton in which we are sliding
    :return: The position where we stop sliding
    """

    # The current position, initialized to the
    # starting position
    current = start

    # So long as we have not hit the edge of
    # the pond or a rock ( represented in the
    # nodes of the graph by "None" ) keep sliding
    if direction == 'left':
        while current.left != None:
            current = current.left
    if direction == 'right':
        while current.right != None:
            current = current.right
    if direction == 'up':
        while current.up != None:
            current = current.up
    if direction == 'down':
        while current.down != None:
            current = current.down

    return current

def backtrack(start, current, prev):
    """
    Helper function to follow backpointers and build a path list.
    :param start:    The source node.
    :param current:  An intermediate node in the path.
    :param prev:     A dictionary from nodes to previous nodes.
    :return:         A list of node objects.
    """
    if current != start:
        v = prev[current]
        return backtrack(start, v, prev) + [current]
    else:
        return [start]


def findDJI(startVert, endVert ):
    """
    An implementation of Djikstra's algorithm for computing
    shortest paths.   Given a binomial heap supporting decreaseKey
    in O(log N) time, the run time of this algorithm is O((V + E)*log(V)).

    Note that this does not work with negative cost edges.

    #####################################################################
    Modification by Amit Maller and Kyle McGlynn:
    This method has been altered to find the shortest path
    between a given position on the frozen pond and the exit.
    #####################################################################

    :param startVert:  the source node object
    :param endVert:    the destination node object
    :return:           A list of node objects corresponding to the
                       shortest weighted path if a path exists.  Otherwise,
                       returns None.
    """

    dist = {}
    dist[startVert] = 0
    prev = {}
    prev[startVert] = None
    q = heap.Heap()
    q.insert(startVert, dist[startVert])

    last = None

    while (q):

        # current is the next unvisited, closest node to start
        current = q.pop()

        # A list of positions that can be reached from
        # current by moving left, up, right, or down.
        stops = list()

        # Use the slide method to determine where
        # we will stop after moving from the current position
        stops.append( slide( current, 'left' ) )
        stops.append( slide( current, 'up' ) )
        stops.append( slide( current, 'right' ) )
        stops.append( slide( current, 'down' ) )

        # check to see if we found a better path to any
        # of current's neighbors
        for n in stops:

            # we found a new node
            if n not in dist:

                # Add one to the distance recorded for this
                # position. We use one since sliding from a
                # starting position until we hit something is
                # considered one movement.
                dist[n] = dist[current] + 1
                prev[n] = current
                q.insert(n, dist[n])

            # we found a better path
            if dist[current] + 1 < dist[n]:
                dist[n] = dist[current] + 1
                prev[n] = current
                q.decreaseKey(n, dist[n])
    if endVert in dist:
        return backtrack(startVert, endVert, prev)
    else:
        return None

def testingSpots( testFileName ):
    """
    This function builds a frozen pond puzzle and finds
    the shortest paths for every point on the pond, if
    they exist.
    :param testFileName: the name of the test file from
                         which the puzzle shall be built
    :return: A dictionary containing the points on the
             frozen pond for which there is a path to
             the exit, and a special list for points
             with no path
    """

    # The dictionary that stores the successful and
    # unsuccessful points. The keys correspond to the
    # length of a given positions shortest path, while
    # values are lists containing the positions. Note,
    # positions for which there is no path are stored at key 0.
    steps = {}

    # Get the different properties of the puzzle and
    # the puzzle's layout from the given text file
    height, width, escape, text = readTest( testFileName )

    # Represent the puzzle as a graph made of nodes
    puzzle = buildPuzzle(text, width, height, escape)

    # Loop over every spot in the puzzle
    for column in range( width ):
        for row in range( height ):

            # If the position is not a rock
            if puzzle[row][column] != None:

                startVert = puzzle[row][column]
                endVert = puzzle[escape][width]
                path = findDJI(startVert,endVert)

                # If there was a path to the end,
                # add the position to one of the
                # successful lists
                if path != None:

                    # If the length of this path has not been
                    # encountered so far
                    if steps.get(len(path)-1) != None:
                        steps[ len(path)-1 ].append( "(" + str(column) + ", " + str(row) + ")" )
                    else:
                        steps[len(path)-1] = list()
                        steps[len(path)-1].append( "(" + str(column) + ", " + str(row) + ")" )

                # If there was no path
                else:
                    if steps.get(0) != None:
                        steps[0].append( "(" + str(column) + ", " + str(row) + ")" )
                    else:
                        steps[0] = list()
                        steps[0].append( "(" + str(column) + ", " + str(row) + ")" )
    return steps

def printResults( paths ):
    """
    This function prints out the results of
    the frozen pond puzzle. If there was not starting
    position, this prints out a message telling
    the user so.
    :param paths: the spots that were tested on
                  the frozen pond, grouped by
                  length of path to the exit in
                  a dictionary. Spots with no path
                  are grouped under a zero length path.
    :return: None
    """

    # If there was at least a starting positions
    if len( paths ) > 0:

        # The keys of the passed in dictionary. They
        # must be put into a list, otherwise they can not
        # be iterated over.
        keys = list(paths.keys())

        # Loop over the keys
        for i in keys :

            # Print out the spots that had a shortest distance
            if i != 0:
                stringResult = str(i) + ": " + str( paths[i])
                print (stringResult)

        # Print out the spots that had no shortest distance
        stringResult = "No path: " + str( paths[keys[0]])
        print (stringResult)

    else:
        print( "No starting square." )

def main():
    """
    The main function. It builds and tests three different
    forzen pond puzzles.
    :return: None
    """

    # Test number 1
    firstTest = 'test1'
    paths1 = testingSpots( firstTest )
    print( "\n" + "Test 1: ")
    printResults( paths1 )

    # Test number 2
    secondTest = 'test2'
    paths2 = testingSpots( secondTest )
    print( "\n" + "Test 2: ")
    printResults( paths2 )

    # Test number 3
    thirdTest = 'test3'
    paths3 = testingSpots( thirdTest )
    print( "\n" + "Test 3: ")
    printResults( paths3 )

    # Test number 4
    fourthTest = 'test4.txt'
    paths4 = testingSpots( fourthTest )
    print( "\n" + "Test 4: ")
    printResults( paths4 )

    # Test number 5
    fifthTest = 'test5.txt'
    paths5 = testingSpots( fifthTest )
    print( "\n" + "Test 5: ")
    printResults( paths5 )

if __name__ == '__main__':
    main()