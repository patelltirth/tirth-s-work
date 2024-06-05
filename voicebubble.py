import pygame
import sys
import random
import speech_recognition as sr
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 30
BUBBLE_RADIUS = 20
BUBBLE_COLOR = (0, 0, 255)
BG_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
LINE_LENGTH = 20
DASH_LENGTH = 10

# Bubble class
class Bubble:
    def __init__(self):
        self.radius = BUBBLE_RADIUS
        self.start_x = WIDTH // 2
        self.start_y = HEIGHT // 2
        self.x = self.start_x
        self.y = self.start_y
        self.dx = 0
        self.dy = 0
        self.move_enabled = False
        self.trail = []

    def move(self):
        if self.move_enabled:
            self.x += self.dx
            self.y += self.dy
            self.trail.append((int(self.x), int(self.y)))

            # Bounce off the walls
            if self.x - self.radius <= 0 or self.x + self.radius >= WIDTH:
                self.dx *= -1
            if self.y - self.radius <= 0 or self.y + self.radius >= HEIGHT:
                self.dy *= -1

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.trail = []

# Create bubbles
bubble = Bubble()

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bubble Screen Saver")

# Buttons
start_button = pygame.Rect(50, HEIGHT - 50, 100, 40)
stop_button = pygame.Rect(200, HEIGHT - 50, 100, 40)
horizontal_button = pygame.Rect(350, HEIGHT - 50, 150, 40)
vertical_button = pygame.Rect(520, HEIGHT - 50, 150, 40)
reset_button = pygame.Rect(690, HEIGHT - 50, 100, 40)

# Button colors
BUTTON_COLOR = (0, 255, 0)
BUTTON_HOVER_COLOR = (0, 200, 0)

# Main loop
clock = pygame.time.Clock()

def voice_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        if "start" in text.lower():
            start_bubble()
        elif "stop" in text.lower():
            stop_bubble()
        elif "horizontal" in text.lower():
            horizontal_bubble()
        elif "vertical" in text.lower():
            vertical_bubble()
        elif "reset" in text.lower():
            reset_bubble()
    except Exception as e:
        print(f"Error: {e}")

def start_bubble():
    bubble.dx = random.choice([1, -1]) * random.randint(1, 10)
    bubble.dy = random.choice([1, -1]) * random.randint(1, 10)
    bubble.move_enabled = True

def stop_bubble():
    bubble.move_enabled = False

def reset_bubble():
    bubble.reset()

def horizontal_bubble():
    bubble.dx = random.choice([1, -1]) * random.randint(1, 10)
    bubble.dy = 0
    bubble.move_enabled = True

def vertical_bubble():
    bubble.dx = 0
    bubble.dy = random.choice([1, -1]) * random.randint(1, 10)
    bubble.move_enabled = True

# Game loop
running = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if start_button.collidepoint(x, y):
                start_bubble()
            elif stop_button.collidepoint(x, y):
                stop_bubble()
            elif horizontal_button.collidepoint(x, y):
                horizontal_bubble()
            elif vertical_button.collidepoint(x, y):
                vertical_bubble()
            elif reset_button.collidepoint(x, y):
                reset_bubble()

    bubble.move()

    screen.fill(BG_COLOR)

    # Draw buttons
    pygame.draw.rect(screen, BUTTON_COLOR, start_button)
    pygame.draw.rect(screen, BUTTON_COLOR, stop_button)
    pygame.draw.rect(screen, BUTTON_COLOR, horizontal_button)
    pygame.draw.rect(screen, BUTTON_COLOR, vertical_button)
    pygame.draw.rect(screen, BUTTON_COLOR, reset_button)

    # Draw button text
    font = pygame.font.Font(None, 36)
    start_text = font.render("Start", True, (0, 0, 0))
    stop_text = font.render("Stop", True, (0, 0, 0))
    horizontal_text = font.render("Horizontal", True, (0, 0, 0))
    vertical_text = font.render("Vertical", True, (0, 0, 0))
    reset_text = font.render("Reset", True, (0, 0, 0))
    screen.blit(start_text, (start_button.x + 25, start_button.y + 10))
    screen.blit(stop_text, (stop_button.x + 30, stop_button.y + 10))
    screen.blit(horizontal_text, (horizontal_button.x + 10, horizontal_button.y + 10))
    screen.blit(vertical_text, (vertical_button.x + 30, vertical_button.y + 10))
    screen.blit(reset_text, (reset_button.x + 20, reset_button.y + 10))

    # Draw bubbles
    pygame.draw.circle(screen, BUBBLE_COLOR, (int(bubble.x), int(bubble.y)), bubble.radius)

    # Draw trailing line
    if len(bubble.trail) > 1:
        pygame.draw.lines(screen, LINE_COLOR, False, bubble.trail, 2)
        pygame.draw.lines(screen, LINE_COLOR, False, bubble.trail, DASH_LENGTH)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

    # Voice commands
    if not running:
        running = True
        while running:
            voice_command()
            time.sleep(1)
            running = False
