import pygame
import sys

pygame.init()

width = 1080
height = 540
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('SkyHigh')
fps = 60
timer = pygame.time.Clock()

font = pygame.font.Font('game_font_7.ttf', 24)
menu_image = pygame.image.load('data/images/logos/GameTitle2.png')
player = pygame.transform.scale(pygame.image.load('data/images/logos/troll.png'), (90, 70))

# background image to fit screen
bg_img_original = pygame.image.load('data/images/logos/sky.png')
bg_img = pygame.transform.scale(bg_img_original, (width, height))  # Scale to screen size

# cloud image
cloud_img = pygame.image.load('data/images/logos/cloud1.png')

# variables
player_x = 170
player_y = 480
platforms = [[170, 480, 200, 20]]  # wide platform
jump = False
y_change = 0
x_change = 0
player_speed = 3


def update_player(y_pos):
    global jump, y_change
    jump_height = 10
    gravity = 1
    if jump:
        y_change -= jump_height
        jump = False
    y_pos += y_change
    
    # collision stuff
    if y_pos > height - 70:  # 70 is player height
        y_pos = height - 70
        y_change = 0
    
    # collision INCOMPLETE
    for platform in platforms:
        platform_rect = pygame.Rect(platform[0], platform[1], platform[2], platform[3])
        player_rect = pygame.Rect(player_x, y_pos, 90, 70)
        
        # player kept falling down
        if player_rect.colliderect(platform_rect) and y_change > 0:
            y_pos = platform[1] - 70 
            y_change = 0
            break  # Stop checking other platforms
    
    y_change += gravity
    return y_pos

class Button:
    def __init__(self, txt, pos):
        self.text = txt
        self.pos = pos
        self.button = pygame.rect.Rect((self.pos[0], self.pos[1]), (260, 40))
    
    def draw(self):
        pygame.draw.rect(screen, 'light gray', self.button, 0, 5)
        pygame.draw.rect(screen, 'dark gray', self.button, 5, 5)
        text = font.render(self.text, True, 'black')
        screen.blit(text, (self.pos[0] + 15, self.pos[1] + 7))

    def check_clicked(self):
        if self.button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return True
        else:
            return False

def draw_menu_screen():
    """Draw the main menu screen and return button click status"""
    # background
    screen.fill('light blue')
    
    # game logo 
    image_rect = menu_image.get_rect()
    image_x = width//2 - image_rect.width // 2
    screen.blit(menu_image, (image_x, 70))
    
    # button positions
    image_height = image_rect.height
    btn_start_y = 70 + image_height + 20
    
    # menu buttons
    btn_start = Button('Start Game', (width//2 - 130, btn_start_y))
    btn_settings = Button('Settings', (width//2 - 130, btn_start_y + 60))
    btn_credits = Button('Credits', (width//2 - 130, btn_start_y + 120))
    btn_quit = Button('Quit Game', (width//2 - 130, btn_start_y + 180))
    
    # Draw buttons
    btn_start.draw()
    btn_quit.draw()
    
    # Check button clicks and return state
    if btn_start.check_clicked():
        return "game"
    elif btn_quit.check_clicked():
        return "quit"
    
    return "menu"

def draw_game_screen():
    """Draw the game screen with background and clouds"""
    screen.blit(bg_img, (0, 0))
    
    screen.blit(cloud_img, (100, 100))
    screen.blit(cloud_img, (400, 150))
    screen.blit(cloud_img, (700, 80))
    
    # platforms
    for platform in platforms:
        pygame.draw.rect(screen, (100, 100, 100), platform)
    
    # player
    screen.blit(player, (player_x, player_y))
    
    # back to menu
    back_btn = Button('Back to Menu', (width - 280, height - 60))
    back_btn.draw()
    
    # game text
    game_text = font.render("Make to the end!", True, 'white')
    screen.blit(game_text, (width//2 - 200, 50))
    
    return back_btn.check_clicked()

class Game:
    def __init__(self):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.state = "menu"  # "menu" or "game"
        
    def run(self):
        global player_x, player_y, x_change, jump, y_change  # Add global declarations
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = "menu" if self.state == "game" else "game"
                    if event.key == pygame.K_a:
                        x_change = -player_speed  # Move left
                    if event.key == pygame.K_d:
                        x_change = player_speed   # Move right
                    if event.key == pygame.K_SPACE and y_change == 0:  # Only jump when on ground/platform
                        jump = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a and x_change < 0:
                        x_change = 0
                    if event.key == pygame.K_d and x_change > 0:
                        x_change = 0
            
            # player position
            if self.state == "game":
                player_x += x_change
                player_y = update_player(player_y)
                
                # player on screen
                if player_x < 0:
                    player_x = 0
                if player_x > width - 90:  # 90 is player width
                    player_x = width - 90
            
            if self.state == "menu":
                # menu and button clicks
                menu_result = draw_menu_screen()
                if menu_result == "game":
                    self.state = "game"
                elif menu_result == "quit":
                    running = False
                    
            elif self.state == "game":
                # game screen
                if draw_game_screen():
                    self.state = "menu"
            
            pygame.display.update()
            self.clock.tick(fps)
        
        pygame.quit()
        sys.exit()

# Run the game
if __name__ == "__main__":
    game = Game()
    game.run()