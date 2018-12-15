from graphics import *
import time

square_size = 50

walking_space = '.'
obstacle_type = '#'
start_point = 'A'
goal_point = 'B'

openSet = []
closeSet = []
start = []
goal = []
cellGrid = []
path = []

# The Map File
filepath = 'maps/board-1-2.txt'

#GUI
win = GraphWin("A* - Dusan Jakovic", 1000, 500)
win.setBackground(color_rgb(66, 134, 244))

openSet_text = Text(Point(100,405), "Open Set Score: ")
openSet_text.setTextColor(color="white")
openSet_text.setSize(10)
openSet_text.setStyle("bold")
openSet_text.draw(win)

openSet_score = Text(Point(175,405), openSet.__len__())
openSet_score.setTextColor(color="white")
openSet_score.setSize(10)
openSet_score.setStyle("bold")
openSet_score.draw(win)

closedSet_text = Text(Point(100,430), "Closed Set Score: ")
closedSet_text.setTextColor(color="white")
closedSet_text.setSize(10)
closedSet_text.setStyle("bold")
closedSet_text.draw(win)

closedSet_score = Text(Point(175,430), closeSet.__len__())
closedSet_score.setTextColor(color="white")
closedSet_score.setSize(10)
closedSet_score.setStyle("bold")
closedSet_score.draw(win)

pathLength_text = Text(Point(100,455), "Path Length Score: ")
pathLength_text.setTextColor(color="white")
pathLength_text.setSize(10)
pathLength_text.setStyle("bold")
pathLength_text.draw(win)

pathLength_text = Text(Point(175,455),'')
pathLength_text.setTextColor(color="white")
pathLength_text.setSize(10)
pathLength_text.setStyle("bold")
pathLength_text.draw(win)

a_rect = Rectangle(Point(900, 400), Point(950, 450))
a_rect.setOutline(color="white")
a_rect.setWidth(3)
a_rect.draw(win)

Astar_text = Text(Point(925,425), "A*")
Astar_text.setSize(25)
# Astar_text = Text(Point(925,425), "BFS")
# Astar_text.setSize(15)
# Astar_text = Text(Point(925,425), "DiJ")
# Astar_text.setSize(15)
Astar_text.setTextColor(color="white")
#Astar_text.setTextColor(color_rgb(66, 134, 244))
Astar_text.setStyle("bold")
Astar_text.draw(win)

# for updating cell-color. Keeps track of already updated cells. Updates only if not already updated
open_update = []
closed_update = []

# Cell class that includes coordinates, type, g-value, h-value, f-value, neighbors and the parent
# It includes methods:
#                       - addNeighbors() to add 0-4 neighbors to each cell
#                       - getNeighbors() return 0-4 neighbors
#                       - rectangle() represents the cell in the grid
#                       - hScoreText() is the cells h-value
class Cell():
    def __init__(self, i, j, type):
        self.i = i
        self.j = j
        self.g = 0
        self.h = 0
        self.f = 0
        self.type = type
        self.parent = None
        self.neighbors = []

    def addNeighbors(self, i, j):
        if i < cellGrid.__len__() - 1:
            if cellGrid[i + 1][j].type != obstacle_type:
                self.neighbors.append(cellGrid[i + 1][j])
        if i > 0:
            if cellGrid[i - 1][j].type != obstacle_type:
                self.neighbors.append(cellGrid[i - 1][j])
        if j < cellGrid[i].__len__() - 1:
            if cellGrid[i][j + 1].type != obstacle_type:
                self.neighbors.append(cellGrid[i][j + 1])
        if j > 0:
            if cellGrid[i][j - 1].type != obstacle_type:
                self.neighbors.append(cellGrid[i][j - 1])

    def getNeighbors(self):
        return self.neighbors

    def rectangle(self, i, j):
        rect = Rectangle(Point(j * square_size, i * square_size),
                         Point(j * square_size + square_size, i * square_size + square_size))
        if self.type is walking_space:
            rect.setFill(color='white')
        if self.type is obstacle_type:
            rect.setFill(color_rgb(10, 10, 10))
        if self.type is start_point:
            rect.setFill(color_rgb(18, 206, 53))
        if self.type is goal_point:
            rect.setFill(color_rgb(206, 18, 34))
        return rect

    def hScoreText(self, i, j):
        displayScore = manhattan(self, goal)
        text = Text(Point(cellGrid[i][j].j * square_size + square_size / 2,
                          cellGrid[i][j].i * square_size + square_size / 2), displayScore)
        text.setSize(10)
        return text

# Manhattan - Heuristic function
def manhattan(point, point2):
    return abs(point.i - point2.i) + abs(point.j - point2.j)


# Parse map into grid array specified by the text-file
def parseMap():
    with open(filepath) as mapFile:
        mapArray = mapFile.readlines()
    return mapArray

# TODO: Clean up. Put this in parseMap function
# Populate elements with Cells specified in the
map = parseMap()
for i in range(map.__len__()):
    subGrid = []
    cellGrid.append(subGrid)
    for j in range(map[i].__len__() - 1):
        if map[i][j] == obstacle_type:
            subGrid.append(Cell(i, j, obstacle_type))
        elif map[i][j] is start_point:
            c = Cell(i, j, start_point)
            start = c
            subGrid.append(c)
        elif map[i][j] == goal_point:
            c = Cell(i, j, goal_point)
            goal = c
            subGrid.append(c)
        else:
            c = Cell(i, j, walking_space)
            subGrid.append(c)
openSet.append(start)

# give the cekks neighbors
def create_neighbors():
    for i in range(cellGrid.__len__()):
        for j in range(cellGrid[i].__len__()):
            cellGrid[i][j].addNeighbors(i, j)

# Draws the board with the cells
def draw_board():
    for y in range(cellGrid.__len__()):
        for x in range(cellGrid[y].__len__()):
            cell = cellGrid[y][x]
            rect = cell.rectangle(y, x)
            rect.draw(win)
            text = cell.hScoreText(y, x)
            text.draw(win)
    win.getMouse()

# Updates the board by the number of seconds specified by the argument
def update_board(second_per_update):
    # A*
    current = min(openSet, key=lambda o: o.f)
    # BFS
    # current = openSet[0]
    # DIJKSTRA
    # current = min(openSet, key=lambda o: o.g)
    for i in openSet:
        if i not in open_update:
            rect = i.rectangle(i.i, i.j)
            rect.setFill(color_rgb(167, 239, 180))
            rect.draw(win)
            open_update.append(i)
            text = i.hScoreText(i.i, i.j)
            text.setOutline(color_rgb(19, 10, 200))
            text.setStyle("bold")
            text.draw(win)
        dot = Circle(Point(current.j * square_size + square_size / 2, current.i * square_size + square_size / 2), 10)
        dot.setOutline(color_rgb(19, 10, 200))
        dot.draw(win)
    for i in closeSet:
        if i not in closed_update:
            rect = i.rectangle(i.i, i.j)
            rect.setFill(color_rgb(239, 167, 167))
            rect.draw(win)
            closed_update.append(i)
            text = i.hScoreText(i.i, i.j)
            text.setOutline(color_rgb(19, 10, 200))
            text.setStyle("bold")
            text.draw(win)
    openSet_score.setText(openSet.__len__())
    closedSet_score.setText(closeSet.__len__())
    time.sleep(second_per_update)


# Draws the path after the final path is found
def draw_path(final_path):
    for i in final_path:
        dot = Circle(Point((i.j * square_size) + square_size / 2,
                           (i.i * square_size) + square_size / 2), 10)
        dot.setFill(color_rgb(66, 134, 244))
        dot.draw(win)


# A* algorithm that finds the shortest path. It includes the update_board method
# which updates the board as long as the algorithm runs
def aStar():
    while openSet:
        update_board(1)
        # A*
        current = min(openSet, key=lambda o: o.f)
        # BFSDEee
        # current = openSet[0]
        # DIJKSTRA
        # current = min(openSet, key=lambda o: o.g)
        if current == goal:
            while current.parent:
                path.append(current)
                current = current.parent
            path.append(current)
            pathLength_text.setText(path.__len__())
            print("GOAL REACHED")
            return path[::-1]

        openSet.remove(current)
        closeSet.append(current)

        neighbors = current.neighbors
        for neighbor in neighbors:
            if neighbor not in closeSet:
                tempG = current.g + 1
                if neighbor in openSet:
                    if tempG < neighbor.g:
                        neighbor.g = tempG
                        neighbor.parent = current
                else:
                    neighbor.h = manhattan(neighbor, goal)
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.parent = current
                    openSet.append(neighbor)

    raise ValueError('--- NO PATH FOUND! ----\n --- '
                     'CHECK IF THE GOAL/END-POINT IS ACCESSIBLE')


# Runs the application
def run():
    draw_board()
    create_neighbors()
    aStar()
    draw_path(path)
    win.getMouse()

run()

############################### TESTING ##################################

# print(openSet[0].neighbors)

# Neighbor test
# print(cellGrid[3][13].neighbors)

# print(start.i, " ", start.j)

# for x in openSet:
#    print(x.type,": x =",x.x, ", y =",x.y)
# while openSet:
# openSet.pop(0)


# print(start.x)
# print(goal)

# for x in cellGrid:
#    print(x)
