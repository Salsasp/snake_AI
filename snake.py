import pygame
import sys
import random

# Constants
GRID_SIZE = 20
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 15

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)



class Snake:
    def __init__(self):
        self.snake = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.food = (random.randint(0, SCREEN_WIDTH - 1) // GRID_SIZE * GRID_SIZE, random.randint(0, SCREEN_HEIGHT - 1) // GRID_SIZE * GRID_SIZE)
        self.direction = pygame.K_RIGHT

    def draw_snake(self):
        for segment in self.snake:
            pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE))

    def is_colliding_with_self(self):
        return len(self.snake) != len(set(self.snake))

    def draw_food(self):
        pygame.draw.rect(screen, RED, pygame.Rect(self.food[0], self.food[1], GRID_SIZE, GRID_SIZE))

    def move(self):
        if self.direction == pygame.K_UP:
            self.snake.insert(0, (self.snake[0][0], self.snake[0][1] - GRID_SIZE))
        elif self.direction == pygame.K_DOWN:
            self.snake.insert(0, (self.snake[0][0], self.snake[0][1] + GRID_SIZE))
        elif self.direction == pygame.K_LEFT:
            self.snake.insert(0, (self.snake[0][0] - GRID_SIZE, self.snake[0][1]))
        elif self.direction == pygame.K_RIGHT:
            self.snake.insert(0, (self.snake[0][0] + GRID_SIZE, self.snake[0][1]))

        if self.snake[0] == self.food:
            self.food = (random.randint(0, SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE * GRID_SIZE, random.randint(0, SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE * GRID_SIZE)
        else:
            self.snake.pop()

        if self.snake[0][0] < 0 or self.snake[0][0] >= SCREEN_WIDTH or self.snake[0][1] < 0 or self.snake[0][1] >= SCREEN_HEIGHT: #check OOB
            pygame.quit()
            sys.exit()

        if self.is_colliding_with_self():
            pygame.quit()
            sys.exit()

    def run(self):
        # Game loop
        while True:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                        snake.change_direction(event.key)
            screen.fill(WHITE)
            self.move()
            self.draw_snake()
            self.draw_food()
            pygame.display.flip()
            clock.tick(FPS)

    def change_direction(self, new_direction):
        if new_direction == pygame.K_UP and self.direction != pygame.K_DOWN:
            self.direction = pygame.K_UP
        elif new_direction == pygame.K_DOWN and self.direction != pygame.K_UP:
            self.direction = pygame.K_DOWN
        elif new_direction == pygame.K_LEFT and self.direction != pygame.K_RIGHT:
            self.direction = pygame.K_LEFT
        elif new_direction == pygame.K_RIGHT and self.direction != pygame.K_LEFT:
            self.direction = pygame.K_RIGHT

# Initialize Pygame
pygame.init()

# Set up some variables
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

snake = Snake()
snake.run()
