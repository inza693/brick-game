import pygame
import random
import math

# Initialize pygame
pygame.init()

# Global variables
size = (600, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Brick Breaker Game")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (252, 3, 152)
LIGHT_PINK = (255, 182, 193)
LIGHT_PURPLE = (200, 162, 200)
RED = (255, 0, 0)
BLUE = (3, 152, 252)
YELLOW = (252, 252, 28)
GREEN = (28, 252, 106)
ORANGE = (252, 170, 28)

class FireworkParticle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.angle = random.uniform(0, 2 * math.pi)
        self.speed = random.uniform(2, 6)
        self.size = random.randint(2, 4)
        self.lifetime = 100

    def update(self):
        self.lifetime -= 1
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)
        self.speed *= 0.98  # Slow down over time
        self.size *= 0.98  # Shrink over time

    def draw(self, screen):
        if self.lifetime > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))

def draw_button(rect, color, text, font):
    pygame.draw.rect(screen, color, rect, border_radius=10)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def welcome_screen():
    play_button = pygame.Rect(200, 300, 200, 50)
    how_to_play_button = pygame.Rect(200, 400, 200, 50)

    while True:
        screen.fill(BLACK)
        font = pygame.font.Font(pygame.font.match_font('comicsansms'), 36)
        text = font.render("WELCOME TO BRICK GAME!", True, LIGHT_PINK)
        screen.blit(text, (50, 100))

        button_font = pygame.font.Font(pygame.font.match_font('comicsansms'), 24)
        draw_button(play_button, LIGHT_PURPLE, "PLAY", button_font)
        draw_button(how_to_play_button, LIGHT_PURPLE, "HOW TO PLAY", button_font)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    return True
                if how_to_play_button.collidepoint(event.pos):
                    show_instructions()

def show_instructions():
    instructions = [
        "1. Use the LEFT and RIGHT arrow keys to move the paddle.",
        "2. Break all the bricks to win the game.",
        "3. If the ball hits the bottom, the game is over.",
        "4. Each brick broken gives you one point.",
        "5. Enjoy the game!"
    ]

    while True:
        screen.fill(BLACK)
        font = pygame.font.Font(pygame.font.match_font('comicsansms'), 20)
        y = 80

        for line in instructions:
            text = font.render(line, True, LIGHT_PINK)
            screen.blit(text, (20, y))
            y += 40

        return_font = pygame.font.Font(pygame.font.match_font('comicsansms'), 24)
        text = return_font.render("Press ENTER to go back", True, LIGHT_PINK)
        screen.blit(text, (150, 500))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

def game_loop():
    floor = pygame.Rect(100, 550, 200, 10)
    ball = pygame.Rect(50, 250, 10, 10)
    ball_radius = 5
    score = 0
    move = [3, 3]
    continueGame = True

    # Bricks
    b1 = [pygame.Rect(1 + i * 100, 60, 98, 38) for i in range(6)]
    b2 = [pygame.Rect(1 + i * 100, 100, 98, 38) for i in range(6)]
    b3 = [pygame.Rect(1 + i * 100, 140, 98, 38) for i in range(6)]

    def draw_brick(bricks, color):
        for brick in bricks:
            pygame.draw.rect(screen, color, brick)

    clock = pygame.time.Clock()

    while continueGame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and floor.x < 400:
            floor.x += 5
        if keys[pygame.K_LEFT] and floor.x > 0:
            floor.x -= 5

        screen.fill(BLACK)
        pygame.draw.rect(screen, PINK, floor)
        font = pygame.font.Font(pygame.font.match_font('comicsansms'), 24)
        text = font.render("CURRENT SCORE: " + str(score), 1, LIGHT_PINK)
        screen.blit(text, (180, 10))

        draw_brick(b1, ORANGE)
        draw_brick(b2, BLUE)
        draw_brick(b3, YELLOW)

        ball.x += move[0]
        ball.y += move[1]

        if ball.x > 590 or ball.x < 0:
            move[0] = -move[0]
        if ball.y <= 3:
            move[1] = -move[1]
        if floor.collidepoint(ball.x, ball.y):
            move[1] = -move[1]

        if ball.y >= 590:
            font = pygame.font.Font(pygame.font.match_font('comicsansms'), 48)
            text = font.render("Game Over!", 1, RED)
            screen.blit(text, (150, 300))
            font = pygame.font.Font(pygame.font.match_font('comicsansms'), 36)
            text = font.render("YOUR FINAL SCORE: " + str(score), 1, LIGHT_PINK)
            screen.blit(text, (100, 350))
            pygame.display.flip()
            pygame.time.wait(2000)
            return True

        pygame.draw.circle(screen, WHITE, (ball.x + ball_radius, ball.y + ball_radius), ball_radius)

        for bricks in [b1, b2, b3]:
            for brick in bricks:
                if brick.collidepoint(ball.x, ball.y):
                    bricks.remove(brick)
                    move[1] = -move[1]
                    score += 1

        if score == 18:
            run_fireworks()
            return True

        pygame.display.flip()
        clock.tick(60)

    return False

def run_fireworks():
    particles = []
    for _ in range(100):
        particles.append(FireworkParticle(300, 300, random.choice([RED, GREEN, BLUE, YELLOW, PINK, ORANGE, WHITE])))

    for _ in range(100):
        screen.fill(BLACK)
        for particle in particles:
            particle.update()
            particle.draw(screen)

        font = pygame.font.Font(pygame.font.match_font('comicsansms'), 48)
        text = font.render("YOU WON!", 1, LIGHT_PINK)
        screen.blit(text, (150, 250))

        pygame.display.flip()
        pygame.time.wait(20)

def ask_play_again():
    yes_button = pygame.Rect(200, 350, 80, 50)
    no_button = pygame.Rect(320, 350, 80, 50)

    while True:
        screen.fill(BLACK)
        font = pygame.font.Font(pygame.font.match_font('comicsansms'), 24)
        text = font.render("Do you want to play the game again?", True, LIGHT_PINK)
        screen.blit(text, (100, 250))

        button_font = pygame.font.Font(pygame.font.match_font('comicsansms'), 24)
        draw_button(yes_button, LIGHT_PURPLE, "Yes", button_font)
        draw_button(no_button, LIGHT_PURPLE, "No", button_font)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if yes_button.collidepoint(event.pos):
                    return True
                if no_button.collidepoint(event.pos):
                    return False

# Main program loop
while True:
    if not welcome_screen():
        break
    if not game_loop():
        break
    if not ask_play_again():
        break
pygame.quit()