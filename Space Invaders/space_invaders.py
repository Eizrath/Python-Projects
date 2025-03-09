import pygame, random, math, sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 150, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
DARK_GRAY = (30, 30, 30)
GLOW_YELLOW = (255, 255, 150)

# Load background
bg_image = pygame.image.load('Space Invaders/assets/images/background.jpg')
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

# Load assets
player_img = pygame.transform.scale(pygame.image.load("Space Invaders/assets/images/player.png"), (50, 50))
bullet_img = pygame.transform.scale(pygame.image.load("Space Invaders/assets/images/bullet1.png"), (30, 30))

# Enhanced loading
enemy_images = [
    pygame.transform.scale(pygame.image.load(f"Space Invaders/assets/images/enemy{i+1}.png"), (50, 50))
    for i in range(5)
]

# Try to load fonts to see if working
try:
    font_large = pygame.font.Font("Space Invaders/assets/fonts/PixeloidMono-d94EV.ttf", 72)
    font_medium = pygame.font.Font("Space Invaders/assets/fonts/PixeloidMono-d94EV.ttf", 48)
    font_small = pygame.font.Font("Space Invaders/assets/fonts/PixeloidMono-d94EV.ttf", 24)
except:
    font_large = pygame.font.Font(None, 72)
    font_medium = pygame.font.Font(None, 48)
    font_small = pygame.font.Font(None, 36)

#
difficulties = {
    "easy": {"num_enemies": 4, "enemy_speed": 3},
    "medium": {"num_enemies": 6, "enemy_speed": 4},
    "hard": {"num_enemies": 8, "enemy_speed": 5}
}

# Game variables
player_x, player_y = WIDTH // 2 - 25, HEIGHT - 80
player_speed = 5
bullet_x, bullet_y = 0, player_y
bullet_speed = 8
bullet_state = "ready"
score = 0
clock = pygame.time.Clock()
difficulty = None


def draw_text(text, x, y, font, color=WHITE):
    render = font.render(text, True, color)
    text_rect = render.get_rect(center=(x, y))
    screen.blit(render, text_rect)

def main_menu():
    """Displays the main menu with animated difficulty selection."""
    menu_running = True

    # Button properties
    buttons = [
        {"text": "1 - Easy", "y": HEIGHT // 2, "color": GREEN},
        {"text": "2 - Medium", "y": HEIGHT // 2 + 60, "color": BLUE},
        {"text": "3 - Hard", "y": HEIGHT // 2 + 120, "color": RED}
    ]

    while menu_running:
        screen.fill(DARK_GRAY)
        screen.blit(bg_image, (0, 0))

        draw_text("SPACE INVADERS", WIDTH // 2, HEIGHT // 4, font_large)
        draw_text("Select Difficulty", WIDTH // 2, HEIGHT // 2 - 80, font_medium, WHITE)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        for button in buttons:
            rect = pygame.Rect(WIDTH // 2 - 100, button["y"], 200, 50)
            color = button["color"]

            # Hover effect
            if rect.collidepoint(mouse_x, mouse_y):
                color = (min(color[0] + 50, 255), min(color[1] + 50, 255), min(color[2] + 50, 255))

            pygame.draw.rect(screen, color, rect, border_radius=15)
            draw_text(button["text"], WIDTH // 2, button["y"] + 25, font_small, BLACK)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "easy"
                elif event.key == pygame.K_2:
                    return "medium"
                elif event.key == pygame.K_3:
                    return "hard"
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(buttons):
                    rect = pygame.Rect(WIDTH // 2 - 100, button["y"], 200, 50)
                    if rect.collidepoint(mouse_x, mouse_y):
                        return ["easy", "medium", "hard"][i]



def create_enemies():
    num_enemies = difficulties[difficulty]["num_enemies"]
    enemy_speed = difficulties[difficulty]["enemy_speed"]
    return [{
        "x": random.randint(50, WIDTH - 50),
        "y": random.randint(50, 150),
        "speed": enemy_speed * (-1 if random.random() > 0.5 else 1),
        "image": random.choice(enemy_images)
    } for _ in range(num_enemies)]

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

    
def game_loop():
    global player_x, bullet_x, bullet_y, bullet_state, score
    enemies = create_enemies()
    running = True

    while running:
        screen.fill(BLACK)
        screen.blit(bg_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_x > 0:
            player_x -= player_speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_x < WIDTH - 50:
            player_x += player_speed
        if keys[pygame.K_SPACE] and bullet_state == "ready":
            bullet_x = player_x
            bullet_state = "fire"

        if bullet_state == "fire":
            screen.blit(bullet_img, (bullet_x + 20, bullet_y - 20))
            bullet_y -= bullet_speed
            if bullet_y <= 0:
                bullet_y = player_y
                bullet_state = "ready"

        for enemy in enemies:
            enemy["x"] += enemy["speed"]
            if enemy["x"] <= 0 or enemy["x"] >= WIDTH - 50:
                enemy["speed"] *= -1
                enemy["y"] += 40

            if math.sqrt((enemy["x"] - bullet_x) ** 2 + (enemy["y"] - bullet_y) ** 2) < 27:
                bullet_y = player_y
                bullet_state = "ready"
                score += 1
                enemy["x"] = random.randint(50, WIDTH - 50)
                enemy["y"] = random.randint(50, 150)

            screen.blit(enemy["image"], (enemy["x"], enemy["y"]))

        if is_player_hit(enemy["x"], enemy["y"], player_x, player_y):
            game_over()       

        screen.blit(player_img, (player_x, player_y))
        draw_text(f"Score: {score}", 80, 30, font_small, WHITE)
        pygame.display.update()
        clock.tick(60)


# Run game
difficulty = main_menu()
game_loop()
