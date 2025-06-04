import pygame
import random

# Initialize Pygame
pygame.init()

# Define constants
WIDTH = 800
HEIGHT = 600
BLOCK_SIZE = 20
SNAKE_SPEED = 15

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Font for score and game over text
font = pygame.font.SysFont(None, 50)

def draw_snake(snake_list):
    for segment in snake_list:
        pygame.draw.rect(screen, GREEN, [segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE])

def display_score(score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, [10, 10])

def game_over_message(score):
    message = font.render(f"Game Over! Score: {score} Press SPACE to Restart", True, WHITE)
    screen.blit(message, [WIDTH // 6, HEIGHT // 3])
    pygame.display.flip()

def generate_food(snake_list):
    while True:
        x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        food_pos = [x, y]
        if food_pos not in snake_list:
            return food_pos

def game_loop():
    game_over = False
    game_close = False

    # Snake starting position and movement
    x1 = WIDTH // 2
    y1 = HEIGHT // 2
    x1_change = 0
    y1_change = 0

    # Initialize snake and food
    snake_list = []
    snake_length = 1
    food_pos = generate_food(snake_list)

    score = 0

    while not game_over:
        while game_close:
            screen.fill(BLACK)
            game_over_message(score)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return game_loop()  # Restart the game

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -BLOCK_SIZE
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = BLOCK_SIZE
                    x1_change = 0

        # Update snake position
        x1 += x1_change
        y1 += y1_change

        # Check for wall collision
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True

        # Update snake head
        snake_head = [x1, y1]
        snake_list.append(snake_head)

        # Maintain snake length
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Check for self-collision
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        # Check for food collision
        if x1 == food_pos[0] and y1 == food_pos[1]:
            food_pos = generate_food(snake_list)
            snake_length += 1
            score += 1

        # Draw everything
        screen.fill(BLACK)
        pygame.draw.rect(screen, RED, [food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE])
        draw_snake(snake_list)
        display_score(score)
        pygame.display.flip()

        # Control game speed
        clock.tick(SNAKE_SPEED)

    pygame.quit()

# Start the game
game_loop()
