import pygame
import random
import os
import time

# Initialize Pygame
pygame.init()

# Load Sounds
pygame.mixer.init()
bg_song = pygame.mixer.Sound("Sounds/background.mp3")  # Background music
start_sound = pygame.mixer.Sound("Sounds/start.mp3")  # Sound when the game starts
eat_sound = pygame.mixer.Sound("Sounds/eat.mp3")  # Sound when food is eaten
gameover_sound = pygame.mixer.Sound("Sounds/end.wav")  # Sound when the game is over
bg_song.set_volume(5)  # Set background music volume

# Game Constants
SCREEN_W, SCREEN_H = 1000, 600  # Screen dimensions
SNAKE_SIZE = 25  # Size of snake segments
INITIAL_SPEED = 15  # Initial speed of the snake

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
VIOLET = (238, 130, 238)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Initialize display
gamewindow = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Snake Game By Shivam Pathak")
clock = pygame.time.Clock()

def text_screen(text, color, x, y ,name="Arial", size=40):
    """Function to display text on the screen."""
    font = pygame.font.SysFont(name ,size,bold=True)
    screen_text = font.render(text, True, color)
    gamewindow.blit(screen_text, (x, y))

def plot_snake(snake_list, snake_size):
    """Function to draw the snake on the screen."""
    for x, y in snake_list:
        pygame.draw.rect(gamewindow, BLACK, [x, y, snake_size, snake_size])
 
def homescreen():
    """Function to display the home screen of the game."""
    start_sound.play()
    
    while True:
        gamewindow.fill(PURPLE)
        text_screen("Welcome to Snake Game", WHITE, 200, 180 ,"Segoe Script",50)
        text_screen("Press SPACE to Play", WHITE, 280, 250,"Segoe Script")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bg_song.play(-1)  # Loop background music
                    gameloop()
                    return

        pygame.display.update()
        clock.tick(60)

def gameloop():
    """Main game loop where the game logic runs."""
    global INITIAL_SPEED
    pt = 0  # Variable to play GameOver sound once
    
    # Initialize snake position
    snake_x, snake_y = 40, 55
    
    # Generate random food position
    foodx = random.randint(0, (SCREEN_W - SNAKE_SIZE)//SNAKE_SIZE) * SNAKE_SIZE
    foody = random.randint(0, (SCREEN_H - SNAKE_SIZE)//SNAKE_SIZE) * SNAKE_SIZE
    
    score = 0  # Initialize score
    velocity_x, velocity_y = 0, 0  # Movement variables
    snake_list = []
    snake_length = 1
    
    # Load high score
    if not os.path.exists("highscore.txt"):
        with open("highscore.txt", "w") as f:
            f.write("0")
    
    with open("highscore.txt", "r") as f:
        highscore = int(f.read())

    running, game_over = True, False
    
    while running:
        
        if game_over:
            
            if pt == 0:
                INITIAL_SPEED = 15
                bg_song.stop()
                gameover_sound.play()
                time.sleep(1)
                gameover_sound.stop()
                pt += 1
            
            with open("highscore.txt", "w") as f:
                f.write(str(max(score, highscore)))
            
            gamewindow.fill(RED)
            text_screen("Game Over! Press ENTER to restart", YELLOW, 110, 200, "Tahoma", 45)
            text_screen(f"Score: {score}  Highscore: {max(score, highscore)}", BLACK, 250, 270,"Microsoft YaHei")
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        bg_song.play(-1)
                        gameloop()
                        return
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    # Control snake movement
                    if event.key == pygame.K_RIGHT and velocity_x == 0:
                        velocity_x, velocity_y = SNAKE_SIZE, 0
                    if event.key == pygame.K_LEFT and velocity_x == 0:
                        velocity_x, velocity_y = -SNAKE_SIZE, 0
                    if event.key == pygame.K_DOWN and velocity_y == 0:
                        velocity_y, velocity_x = SNAKE_SIZE, 0
                    if event.key == pygame.K_UP and velocity_y == 0:
                        velocity_y, velocity_x = -SNAKE_SIZE, 0

            # Update snake position
            snake_x += velocity_x
            snake_y += velocity_y

            # Check for collision with walls
            if snake_x < 0 or snake_x >= SCREEN_W or snake_y < 0 or snake_y >= SCREEN_H:
                game_over = True

            # Check if snake eats food
            if abs(snake_x - foodx) < SNAKE_SIZE and abs(snake_y - foody) < SNAKE_SIZE:
                eat_sound.play()
                foodx = random.randint(0, (SCREEN_W - SNAKE_SIZE)//SNAKE_SIZE) * SNAKE_SIZE
                foody = random.randint(0, (SCREEN_H - SNAKE_SIZE)//SNAKE_SIZE) * SNAKE_SIZE
                score += 10
                snake_length += 1
                
                # Increase speed at every 50 points
                if score % 50 == 0:
                    INITIAL_SPEED += 1
                
                # Update highscore
                if score > highscore:
                    highscore = score

            snake_head = [snake_x, snake_y]
            snake_list.append(snake_head)
            
            # Remove tail segment to keep snake size constant
            if len(snake_list) > snake_length:
                del snake_list[0]

            # Check if snake collides with itself
            if snake_head in snake_list[:-1]:
                game_over = True

            gamewindow.fill(VIOLET)
            pygame.draw.rect(gamewindow, RED, [foodx, foody, SNAKE_SIZE, SNAKE_SIZE])  # Draw food
            plot_snake(snake_list, SNAKE_SIZE)  # Draw snake
            text_screen(f"Score: {score}  Highscore: {highscore}", BLACK, 12, 10 )

        pygame.display.update()
        clock.tick(INITIAL_SPEED)

    pygame.quit()

homescreen()
