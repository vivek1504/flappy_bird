import pygame

screen = pygame.display.set_mode((1500, 820))

bird_velocity = 0
gravity = 1000
flapstrength = 300

bird_height = 40
bird_width = 40
bird_pos = pygame.Vector2(screen.get_width() /4, screen.get_height() / 2)
bird_rect = pygame.Rect(bird_pos.x, bird_pos.y, bird_height, bird_width)


class Bird:
    def __init__(self, x, y, width=60, height=60, gravity=1000, flap_strength = 300):
        self.pos = pygame.Vector2(x,y)
        self.width = width
        self.height = height
        self.gravity = gravity
        self.flap_strength = flap_strength
        self.velocity = 0

    @property
    def rect(self):
        return pygame.Rect(self.pos.x,self.pos.y, self.width, self.height)
    
    def flap(self):
        self.velocity = -self.flap_strength

    def update(self, dt, screen_height):
        self.velocity += self.gravity * dt
        self.pos.y += self.velocity * dt

        if self.pos.y < 0:
            self.pos.y = 0
            self.velocity = 0

        elif self.pos.y + self.height > screen_height:
            self.pos.y = screen_height - self.height
            self.velocity = 0

    
    def draw(self, screen, bird_image):
        bird_rect = bird_image.get_rect(center = (int(self.pos.x + self.width/2),int(self.pos.y + self.height/2)))
        screen.blit(bird_image, bird_rect)

    
    def reset(self, x, y):
        self.pos = pygame.Vector2(x,y)
        self.velocity = 0