import pygame
import random

class Pipe:
    def __init__(self, x, screen_height, gap_height=200, width=120, speed=200):
        self.x = x
        self.screen_height = screen_height
        self.gap_height = gap_height
        self.width = width
        self.speed = speed

        self.gap_y = random.randint(100, screen_height - 100 - gap_height)
        self.scored = False

    def update(self, dt):
        self.x -= self.speed * dt

    def draw(self, screen):
        # --- COLORS FOR SPOOKY FUTURISTIC VIBE ---
        body_color = (30, 255, 200)        # neon cyan
        border_color = (0, 150, 100)       # darker teal
        cap_color = (100, 255, 220)        # glowing edge

        # --- CALCULATE RECTANGLES ---
        top_rect = pygame.Rect(self.x, 0, self.width, self.gap_y)
        bottom_rect = pygame.Rect(self.x, self.gap_y + self.gap_height,self.width, self.screen_height - (self.gap_y + self.gap_height))

        # --- DRAW TOP PIPE ---
        pygame.draw.rect(screen, body_color, top_rect, border_radius=15)
        pygame.draw.rect(screen, border_color, top_rect, width=4, border_radius=15)
        # Cap at gap
        cap_height = 15
        pygame.draw.rect(screen, cap_color, (self.x, self.gap_y - cap_height, self.width, cap_height))

        # --- DRAW BOTTOM PIPE ---
        pygame.draw.rect(screen, body_color, bottom_rect, border_radius=15)
        pygame.draw.rect(screen, border_color, bottom_rect, width=4, border_radius=15)
        # Cap at gap
        pygame.draw.rect(screen, cap_color, (self.x, self.gap_y + self.gap_height, self.width, cap_height))
                                             
    def recycle(self, new_x):
        self.x = new_x
        self.gap_y = random.randint(100, self.screen_height - 100 - self.gap_height)
        self.scored = False

    def get_rect(self):
        top_rect = pygame.Rect(self.x, 0, self.width, self.gap_y)

        bottom_y = self.gap_y + self.gap_height
        bottom_rect = pygame.Rect(self.x, bottom_y, self.width, self.screen_height - bottom_y)

        return top_rect, bottom_rect