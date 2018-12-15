from graphics import *
import time


square_size = 35

road_type = 'r'
grass_type = 'g'
forest_type = 'f'
mountain_type = 'm'
water_type = 'w'
start_point = 'A'
goal_point = 'B'

openSet = []
closeSet = []
start = []
goal = []
cellGrid = []
path = []


filepath = 'maps/board-2-4.txt'

#GUI
win = GraphWin("A* - Dusan Jakovic", 1400, 500, autoflush=False)
win.setBackground(color_rgb(206, 141, 14))

openSet_text = Text(Point(100,385), "Open Set Score: ")
openSet_text.setTextColor(color="white")
openSet_text.setSize(10)
openSet_text.setStyle("bold")
openSet_text.draw(win)

openSet_score = Text(Point(175,385), openSet.__len__())
openSet_score.setTextColor(color="white")
openSet_score.setSize(10)
openSet_score.setStyle("bold")
openSet_score.draw(win)

closedSet_text = Text(Point(100,410), "Closed Set Score: ")
closedSet_text.setTextColor(color="white")
closedSet_text.setSize(10)
closedSet_text.setStyle("bold")
closedSet_text.draw(win)

closedSet_score = Text(Point(175,410), closeSet.__len__())
closedSet_score.setTextColor(color="white")
closedSet_score.setSize(10)
closedSet_score.setStyle("bold")
closedSet_score.draw(win)

pathLength_text = Text(Point(100,435), "Path Length Score: ")
pathLength_text.setTextColor(color="white")
pathLength_text.setSize(10)
pathLength_text.setStyle("bold")
pathLength_text.draw(win)

pathLength_text = Text(Point(175,435),'')
pathLength_text.setTextColor(color="white")
pathLength_text.setSize(10)
pathLength_text.setStyle("bold")
pathLength_text.draw(win)

pathCost_text = Text(Point(100,460), "Path Cost Score: ")
pathCost_text.setTextColor(color="white")
pathCost_text.setSize(10)
pathCost_text.setStyle("bold")
pathCost_text.draw(win)

pathCost_text = Text(Point(175,460),'')
pathCost_text.setTextColor(color="white")
pathCost_text.setSize(10)
pathCost_text.setStyle("bold")
pathCost_text.draw(win)

a_rect = Rectangle(Point(1300,400),Point(1350,450))
a_rect.setOutline(color="white")
a_rect.setWidth(3)
a_rect.draw(win)

#white_rect = Rectangle(Point(950,400),Point(1000,450))
#white_rect.setOutline(color="white")
#white_rect.setFill(color="white")
#white_rect.draw(win)

Astar_text = Text(Point(1325,425), "A*")
Astar_text.setSize(25)
# Astar_text = Text(Point(1325,425), "BFS")
# Astar_text.setSize(15)
# Astar_text = Text(Point(1325,425), "DiJ")
# Astar_text.setSize(15)
Astar_text.setTextColor(color="white")
#Astar_text.setTextColor(color_rgb(66, 134, 244))
Astar_text.setStyle("bold")
Astar_text.draw(win)

#for updating cell-color
##keeps track of already updated cells. Updates only if not already updated
open_update = []
closed_update = []

class Cell():
    def __init__(self, i, j, type, cost):
        self.i = i
        self.j = j
        self.g = cost
        self.h = 0
        self.f = 0
        self.cost = cost
        self.costSoFar = cost
        self.type = type
        self.parent = None
        self.neighbors = []

    def addNeighbors(self, i, j):
        if j < cellGrid[i].__len__() - 1:
            self.neighbors.append(cellGrid[i][j + 1])
        if j > 0:
            self.neighbors.append(cellGrid[i][j - 1])
        if i < cellGrid.__len__() - 1:
            self.neighbors.append(cellGrid[i + 1][j])
        if i > 0:
            self.neighbors.append(cellGrid[i - 1][j])


    def getNeighbors(self):
        return self.neighbors

    def rectangle(self, i, j):
        rect = Rectangle(Point(j * square_size, i * square_size),
                         Point(j * square_size + square_size, i * square_size + square_size))
        rect.setWidth(3)
        if self.type is grass_type:
            rect.setFill(color_rgb(25, 255, 102))
        if self.type is forest_type:
            rect.setFill(color_rgb(0, 135, 45))
        if self.type is water_type:
            rect.setFill(color_rgb(0, 81, 196))
        if self.type is mountain_type:
            rect.setFill(color_rgb(109, 109, 109))
        if self.type is road_type:
            rect.setFill(color_rgb(132, 104, 58))
        if self.type is start_point:
            rect.setFill(color_rgb(18, 206, 53))
        if self.type is goal_point:
            rect.setFill(color_rgb(206, 18, 34))
        return rect

    def hScoreText(self, i, j):
        displayScore = manhattan_with_cost(self,goal)
        text = Text(Point(cellGrid[i][j].j * square_size + square_size / 2,
                          cellGrid[i][j].i * square_size + square_size / 2), displayScore)
        text.setSize(10)
        return text

    def fScoreText(self, i, j):
        text = Text(Point(cellGrid[i][j].j * square_size + square_size / 2,
                          cellGrid[i][j].i * square_size + square_size / 2), self.f)
        text.setSize(10)
        return text


#Manhattan method for finding the heuristic cost (f(h)
def manhattan(point, point2):
    return abs(point.i - point2.i) + abs(point.j - point2.j)

#This euqlidian Manhattan method is used to show the h from
#current cell to the Goal, including the cost for the given cell
def manhattan_with_cost(point, point2):
    return abs(point.i - point2.i) + abs(point.j - point2.j) + point.cost

# Parse map into grid array
def parseMap():
    with open(filepath) as mapFile:
        mapArray = mapFile.readlines()
    return mapArray

map = parseMap()

#TODO: Clean up. Put this in parseMap function
# Populate elements with Cells
for i in range(map.__len__()):
    subGrid = []
    cellGrid.append(subGrid)
    for j in range(map[i].__len__() - 1):
        if map[i][j] == grass_type:
            subGrid.append(Cell(i, j, grass_type, 5))
        elif map[i][j] == forest_type:
            subGrid.append(Cell(i, j, forest_type, 10))
        elif map[i][j] == water_type:
            subGrid.append(Cell(i, j, water_type, 100))
        elif map[i][j] == mountain_type:
            subGrid.append(Cell(i, j, mountain_type, 50))
        elif map[i][j] == road_type:
            subGrid.append(Cell(i, j, road_type, 1))
        elif map[i][j] is start_point:
            c = Cell(i, j, start_point, 0)
            start = c
            subGrid.append(c)
        elif map[i][j] == goal_point:
            c = Cell(i, j, goal_point, 0)
            goal = c
            subGrid.append(c)

openSet.append(start)

# give neighbors
def create_neighbors():
    for i in range(cellGrid.__len__()):
        for j in range(cellGrid[i].__len__()):
            cellGrid[i][j].addNeighbors(i, j)


def draw_board():
    for y in range(cellGrid.__len__()):
        for x in range(cellGrid[y].__len__()):
            cell = cellGrid[y][x]
            rect = cell.rectangle(y, x)
            rect.draw(win)
    win.getMouse()


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
            rect.setOutline(color_rgb(167, 239, 180))
            rect.setWidth(3)
            rect.draw(win)
            open_update.append(i)
            #text = i.fScoreText(i.i, i.j)
            #text.setOutline(color_rgb(19, 10, 200))
            #text.setStyle("bold")
            #text.draw(win)
        dot = Circle(Point(current.j * square_size + square_size / 2, current.i * square_size + square_size / 2), 10)
        dot.setOutline(color_rgb(66, 134, 244))
        dot.setWidth(3)
        dot.draw(win)
    for i in closeSet:
        if i not in closed_update:
            rect = i.rectangle(i.i, i.j)
            rect.setOutline(color_rgb(239, 167, 167))
            rect.setWidth(3)
            rect.draw(win)
            closed_update.append(i)
            #text = i.fScoreText(i.i, i.j)
            #text.setOutline(color_rgb(19, 10, 200))
            #text.setStyle("bold")
            #text.draw(win)
    openSet_score.setText(openSet.__len__())
    closedSet_score.setText(closeSet.__len__())
    # remove update method-call to skip animation
    win.update()
    time.sleep(second_per_update)




def draw_path(final_path):
    for i in final_path:
        dot = Circle(Point((i.j * square_size) + square_size / 2,
                           (i.i * square_size) + square_size / 2), 10)
        dot.setFill(color_rgb(66, 134, 244))
        dot.setOutline(color="white")
        dot.setWidth(3)
        dot.draw(win)

def aStar():
    while openSet:
        update_board(0)
        # A* STAR
        current = min(openSet, key=lambda o: o.f)
        # BFS
        # current = openSet[0]
        # DIJKSTRA
        # current = min(openSet, key=lambda o: o.g)
        if current == goal:
            while current.parent:
                path.append(current)
                current = current.parent
            path.append(current)
            pathLength_text.setText(path.__len__())
            #Initilized as 1 becaus goal is in the path
            path_cost = 1
            for cell in path:
                path_cost += cell.costSoFar
            pathCost_text.setText(path_cost)
            print("GOAL REACHED")
            return path[::-1]

        openSet.remove(current)
        closeSet.append(current)

        if current.parent:
            current.cost = current.parent.cost + current.cost

        neighbors = current.neighbors
        for neighbor in neighbors:
            if neighbor not in closeSet:
                tempG = current.g + current.cost
                if neighbor in openSet:
                    if tempG < neighbor.g:
                        neighbor.g = tempG
                        neighbor.parent = current
                else:
                    neighbor.h = manhattan(neighbor, goal)
                    neighbor.f = neighbor.g + neighbor.h + current.cost
                    neighbor.parent = current
                    openSet.append(neighbor)
    raise ValueError('--- NO PATH FOUND! ----\n --- '
                     'CHECK IF THE GOAL/END-POINT IS ACCESSIBLE')


def run():
    draw_board()
    create_neighbors()
    aStar()
    draw_path(path)
    win.getMouse()

run()
