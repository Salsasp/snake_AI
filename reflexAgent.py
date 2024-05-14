import pygame
import sys
import random
import math
import queue
import stack
import priorityQueue
import time
#my attempt at a simple implementation of various reflex agent algorithms such as BFS, DFS, and UCS
#This agent of course does not have any access to the location of the food or its other segements, so it must search

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
GRID_SIZE = 15 #N x M dimension of grid
UNIT_SIZE = SCREEN_WIDTH//GRID_SIZE #tile sizes scaled off screen size and specified tile amount
FPS = 60
LOGIC_TICK_RATE = 10

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)

# Initialize Pygame
pygame.init()

# Set up some variables
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

class ReflexSnake: #TODO: MODIFY SNAKE CLASS TO FIT REFLEX AGENT REQUIREMENTS (E.G. FOOD LOCATION UNKNOWN)
    def __init__(self):
        self.snake = [pixelPosToTilePos(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)] #list of tiles containing snake segments, start in middle of screen
        self.positions = [x for x in range(GRID_SIZE**2)] #list of 0 through GRID_SIZE
        self.direction = pygame.K_RIGHT #start snake going right
        self.food = [random.randint(0,GRID_SIZE**2)] #for game logic, not for agent use
        self.logic_tick_counter = 0
        self.tileBounds = {}
        for i in range(GRID_SIZE**2):
            self.tileBounds[i] = [((i%GRID_SIZE)*UNIT_SIZE,(i%GRID_SIZE)*(UNIT_SIZE)+UNIT_SIZE), ((i//GRID_SIZE)*UNIT_SIZE, (i//GRID_SIZE)*(UNIT_SIZE)+UNIT_SIZE)]

    def generateFood(self):
        tileIndex = random(0,GRID_SIZE**2)
        self.positions[tileIndex] = True
        self.food.append(tileIndex)

    def draw_snake(self):
        for tilePos in self.snake:
            pygame.draw.rect(screen, GREEN, pygame.Rect(self.tileBounds[tilePos][0][0], self.tileBounds[tilePos][1][0], UNIT_SIZE, UNIT_SIZE))

    def is_colliding_with_self(self):
        return len(self.snake) != len(set(self.snake))

    def draw_food(self):
        pygame.draw.rect(screen, RED, pygame.Rect(self.tileBounds[self.food[0]][0][0], self.tileBounds[self.food[0]][1][0], UNIT_SIZE, UNIT_SIZE))

    def move(self):
        if self.logic_tick_counter == LOGIC_TICK_RATE:
            if self.direction == pygame.K_UP:
                newPos = tileUp(self.snake[0])
                if newPos == -1:
                    pygame.quit()
                    sys.exit()
                self.snake.insert(0, newPos)

            elif self.direction == pygame.K_DOWN:
                newPos = tileDown(self.snake[0])
                if newPos == -1:
                    pygame.quit()
                    sys.exit()
                self.snake.insert(0, newPos)

            elif self.direction == pygame.K_LEFT:
                newPos = tileLeft(self.snake[0])
                if newPos == -1:
                    pygame.quit()
                    sys.exit()
                self.snake.insert(0, newPos)

            elif self.direction == pygame.K_RIGHT:
                newPos = tileRight(self.snake[0])
                if newPos == -1:
                    pygame.quit()
                    sys.exit()
                self.snake.insert(0, newPos)

            if self.snake[0] == self.food[0]:
                self.food.pop()
                self.food.append(random.randint(0,GRID_SIZE**2))
            else:
                self.snake.pop()

            if self.is_colliding_with_self():
                pygame.quit()
                sys.exit()
            self.logic_tick_counter = 0

        self.logic_tick_counter += 1

    def run(self):
        # Game loop
        while True:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                        self.direction = event.key
            screen.fill(WHITE)
            self.move()
            self.draw_snake()
            self.draw_food()
            pygame.display.flip()
            clock.tick(FPS)

    def displayTraversal(self, moves):
        if len(moves) == 0:
            print("moves empty")
            return
        screen.fill(WHITE)
        pygame.draw.rect(screen, RED, pygame.Rect(self.tileBounds[self.food[0]][0][0], self.tileBounds[self.food[0]][1][0], UNIT_SIZE, UNIT_SIZE))
        for move in moves:
            pygame.draw.rect(screen, PURPLE, pygame.Rect(self.tileBounds[move][0][0], self.tileBounds[move][1][0], UNIT_SIZE, UNIT_SIZE))
            pygame.display.flip()
            clock.tick(15)


def BFS(reflexSnake):
    q = queue.Queue()
    q.put(reflexSnake.snake[0])
    goal = reflexSnake.food[0]
    visited = set()
    traversalOrder = []
    while not q.empty(): #loop through pos tuples of grid
        currPos = q.get()
        if currPos == goal:
            traversalOrder.append(currPos)
            return traversalOrder
        if currPos == -1 or currPos in visited:
            continue
        visited.add(currPos)
        traversalOrder.append(currPos)
        q.put(tileLeft(currPos))
        q.put(tileUp(currPos))
        q.put(tileRight(currPos))
        q.put(tileDown(currPos))
    return[]

def DFS(reflexSnake):
    s = stack.Stack()
    s.push(reflexSnake.snake[0])
    goal = reflexSnake.food[0]
    visited = set()
    traversalOrder = []
    while not s.empty(): #loop through pos tuples of grid
        currPos = s.pop()
        if currPos == goal:
            traversalOrder.append(currPos)
            return traversalOrder
        if currPos == -1 or currPos in visited:
            continue
        visited.add(currPos)
        traversalOrder.append(currPos)
        s.push(tileLeft(currPos))
        s.push(tileUp(currPos))
        s.push(tileRight(currPos))
        s.push(tileDown(currPos))
    return[]

def UCS(reflexSnake):
    q = priorityQueue.PriorityQueue()
    goal = reflexSnake.food[0]
    q.put(reflexSnake.snake[0], manhattanDistance(reflexSnake.snake[0], goal))
    visited = set()
    traversalOrder = []
    while not q.empty(): #loop through pos tuples of grid
        currPos = q.get()
        if currPos == goal:
            traversalOrder.append(currPos)
            return traversalOrder
        if currPos == -1 or currPos in visited:
            continue
        visited.add(currPos)
        traversalOrder.append(currPos)
        q.put(tileLeft(currPos),manhattanDistance(currPos, goal))
        q.put(tileUp(currPos),manhattanDistance(currPos, goal))
        q.put(tileRight(currPos),manhattanDistance(currPos, goal))
        q.put(tileDown(currPos),manhattanDistance(currPos, goal))
    return[]

def manhattanDistance(currPos, goal):
    xDist1 = currPos%GRID_SIZE
    yDist1 = currPos//GRID_SIZE
    xDist2 = goal%GRID_SIZE
    yDist2 = goal//GRID_SIZE
    return abs(xDist2-xDist1) + abs(yDist2 - yDist1)
    
def pixelPosToTilePos(x, y):
    return x//UNIT_SIZE + (y//UNIT_SIZE)*GRID_SIZE #convert pixel to corresponding tile index

def tileUp(currPos):
        if(currPos >= 0 and currPos <= GRID_SIZE): #if currentPos on top row and movement is up
            return -1 #return -1 if OOB
        newPos = currPos - GRID_SIZE
        return newPos
def tileDown(currPos):
    if(currPos >= (GRID_SIZE**2 - GRID_SIZE) and currPos < GRID_SIZE**2): #if currentPos on bottom row and movement is down
        return -1 #return -1 if OOB
    return currPos + GRID_SIZE
def tileLeft(currPos):
    if(currPos%GRID_SIZE == 0):
        return -1
    return currPos - 1
def tileRight(currPos):
    if(currPos%GRID_SIZE == GRID_SIZE-1):
        return -1
    return currPos + 1

def main(): #where shit happens
    snake = ReflexSnake()
    snake.displayTraversal(UCS(snake))
    #snake.run()
    

main()
