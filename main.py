import pygame
import sys
import random
import time

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_SIZE = 15

# Scores & Settings
global left_score, right_score
left_score = 0
right_score = 0
player_speed = 7
ai_speed = 5
ai_last_move_time = 0
ai_move_delay = 0.017

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

FPS = 60

class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BALL_SIZE, BALL_SIZE)
        self.speed_x = random.choice([-5, 5])
        self.speed_y = random.choice([-5, 5])

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Bounce off top and bottom
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y = -self.speed_y

    def draw(self, screen):
        pygame.draw.ellipse(screen, WHITE, self.rect)

class Paddle:
    def __init__(self, x, y, speed):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = speed

    def move(self, up=True):
        if up:
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed

        # Keep paddle within screen bounds
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

def ai_move_logic(ball, right_paddle):
    global ai_last_move_time
    global ai_move_delay

    current_time = time.time()
    if current_time - ai_last_move_time > ai_move_delay:
        # Do movement logic
        if ball.rect.centery < right_paddle.rect.centery:
            right_paddle.move(up=True)
        elif ball.rect.centery > right_paddle.rect.centery:
            right_paddle.move(up=False)

        # Update last move time
        ai_last_move_time = current_time

def score_display(screen, left_score, right_score):
    left_text = font.render(f"{left_score}", 1, BLUE)
    right_text = font.render(f"{right_score}", 1, RED)
    screen.blit(left_text, (WIDTH // 4 - left_text.get_width() // 2, 20))
    screen.blit(right_text, (3 * WIDTH // 4 - right_text.get_width() // 2, 20))

def reset_ball(ball):
    ball.rect.x = WIDTH // 2 - BALL_SIZE // 2
    ball.rect.y = HEIGHT // 2 - BALL_SIZE // 2
    ball.speed_x = random.choice([-5, 5])
    ball.speed_y = random.choice([-5, 5])

def ball_out_of_bounds(ball):
    global left_score, right_score
    if ball.rect.left <= 0:
        right_score += 1
        reset_ball(ball)
    elif ball.rect.right >= WIDTH:
        left_score += 1
        reset_ball(ball)

def collide(ball, paddle):
    if ball.rect.colliderect(paddle.rect):
        ball.speed_x = -ball.speed_x

def won_game():
    global left_score, right_score
    if left_score >= 10:
        return "Left Player Wins!"
    elif right_score >= 10:
        return "Right Player Wins!"
    return None

# screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game @Kallisto")
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsans", 50)

def main():
    global left_score, right_score
    # Main Menu
    while True:
        screen.fill(BLACK)
        title_text = font.render("PONG GAME", 1, WHITE)
        instruction_text = font.render("Press SPACE to Start", 1, WHITE)
        vs_ai_text = font.render("Press Y for Player vs AI", 1, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
        screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2))
        screen.blit(vs_ai_text, (WIDTH // 2 - vs_ai_text.get_width() // 2, HEIGHT // 2 + 50))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    p_vs_p_loop()
                    return
                if event.key == pygame.K_y:
                    p_vs_ai_loop()
                    return

def p_vs_ai_loop():
    global left_score, right_score
    left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, player_speed)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, ai_speed)
    ball = Ball(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2)

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()

        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            left_paddle.move(up=True)
        if key[pygame.K_s]:
            left_paddle.move(up=False)

        ai_move_logic(ball, right_paddle)

        screen.fill(BLACK)

        score_display(screen, left_score, right_score)

        left_paddle.draw(screen)
        right_paddle.draw(screen)

        ball.move()
        ball.draw(screen)

        ball_out_of_bounds(ball)

        collide(ball, left_paddle)
        collide(ball, right_paddle)

        winner = won_game()
        if winner:
            win_text = font.render(winner, 1, WHITE)
            screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - win_text.get_height() // 2))
            pygame.display.flip()
            pygame.time.delay(3000)
            left_score = 0
            right_score = 0

        pygame.display.flip()

def p_vs_p_loop():
    global left_score, right_score
    left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, player_speed)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, player_speed)
    ball = Ball(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2)

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()

        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            left_paddle.move(up=True)
        if key[pygame.K_s]:
            left_paddle.move(up=False)
        if key[pygame.K_UP]:
            right_paddle.move(up=True)
        if key[pygame.K_DOWN]:
            right_paddle.move(up=False)

        screen.fill(BLACK)

        score_display(screen, left_score, right_score)

        left_paddle.draw(screen)
        right_paddle.draw(screen)

        ball.move()
        ball.draw(screen)

        ball_out_of_bounds(ball)

        collide(ball, left_paddle)
        collide(ball, right_paddle)

        winner = won_game()
        if winner:
            win_text = font.render(winner, 1, WHITE)
            screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - win_text.get_height() // 2))
            pygame.display.flip()
            pygame.time.delay(3000)
            left_score = 0
            right_score = 0

        pygame.display.flip()
    

if __name__ == "__main__":
    main()
    pygame.quit()