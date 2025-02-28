import pygame, random, math, sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

#Add bg and resize
bg_image = pygame.image.load('Space Invaders/assets/background.jpg')
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

# Load and scale images for player, enemy, and bullet
player_img = pygame.image.load("Space Invaders/assets/player.png")
enemy_img = pygame.image.load("Space Invaders/assets/enemy.png")
bullet_img = pygame.image.load("Space Invaders/assets/bullet.jpg")

player_img = pygame.transform.scale(player_img, (50, 50))
enemy_img = pygame.transform.scale(enemy_img, (50, 50))
bullet_img = pygame.transform.scale(bullet_img, (30, 30))

# Player properties
player_x = WIDTH // 2 - 25  # Center player horizontally
player_y = HEIGHT - 80  # Position player near the bottom
player_speed = 5

# Enemy properties
num_enemies = 5
enemies = []
for _ in range(num_enemies):
    enemy_x = random.randint(50, WIDTH - 50)
    enemy_y = random.randint(50, 150)
    enemy_speed = 3
    enemies.append([enemy_x, enemy_y, enemy_speed])

# Bullet properties
bullet_x = 0
bullet_y = player_y
bullet_speed = 7
bullet_state = "ready"  # "ready" means bullet can be fired, "fire" means bullet is in motion

# Score tracking
score = 0
font = pygame.font.Font(None, 36)

# Game loop control variables
running = True
clock = pygame.time.Clock()

def draw_player(x, y):
    """Draws the player on the screen."""
    screen.blit(player_img, (x, y))
    
def draw_enemy(x, y):
    """Draws an enemy on the screen."""
    screen.blit(enemy_img, (x, y))

def fire_bullet(x, y):
    """Fires the bullet from the player's position."""
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 20, y - 20))

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    """Checks if a bullet has hit an enemy using distance formula."""
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2)))
    return distance < 27  # If distance is small enough, it's a hit

def is_player_hit(enemy_x, enemy_y, player_x, player_y):
        """Collision Hitbox/Box"""
        player_width, player_height = 50, 50
        enemy_width, enemy_height = 50, 50
        
        if (player_x < enemy_x + enemy_width and
            player_x + player_width > enemy_x and
            player_y < enemy_y + enemy_height and
            player_y + player_height > enemy_y):
            return True
        return False

def game_over():
    """Game Over Screen"""
    global running
    screen.fill(BLACK)
    font_large = pygame.font.Font(None, 72)
    text = font_large.render("GAME OVER", True, RED)
    screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
    pygame.display.update()
    pygame.time.delay(5000)  # Pause for 5 seconds
    running = False  # Stop the game

# Main game loop
while running:
    screen.fill(BLACK)  # Clear screen every frame
    screen.blit(bg_image, (0,0))
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Quit the game if window is closed
            running = False

    # Player movement controls
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_x > 0:
        player_x -= player_speed
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_x < WIDTH - 50:
        player_x += player_speed
    if keys[pygame.K_SPACE] and bullet_state == "ready":  # Fire bullet
        bullet_x = player_x
        fire_bullet(bullet_x, bullet_y)
        
    # Bullet movement
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_speed
    
    # Reset bullet when it reaches the top
    if bullet_y <= 0:
        bullet_y = player_y
        bullet_state = "ready"
        
    # Enemy movement
    for enemy in enemies:
        enemy[0] += enemy[2]  # Move enemy left or right
        
        # Reverse direction and move down when reaching screen edges
        if enemy[0] <= 0 or enemy[0] >= WIDTH - 50:
            enemy[2] *= -1
            enemy[1] += 40  # Move down
        
        # Check for collision
        if is_collision(enemy[0], enemy[1], bullet_x, bullet_y):
            bullet_y = player_y
            bullet_state = "ready"
            score += 1
            enemy[0] = random.randint(50, WIDTH - 50)  # Respawn enemy at new position
            enemy[1] = random.randint(50, 150)
            
        draw_enemy(enemy[0], enemy[1])

        if is_player_hit(enemy[0], enemy[1], player_x, player_y):
            game_over()        
        
    # Draw player on screen
    draw_player(player_x, player_y)
    
    # Display score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    pygame.display.update()  # Update the display
    clock.tick(144)  # Limit frame rate to 30 FPS
    
pygame.quit()  # Exit game when loop ends

