import pygame 
import cv2
from pipe import Pipe
from bird import Bird

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1289, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
game_started = False
game_active = True
dt = 0

score = 0
high_score = 0
prev_score = 0

font = pygame.font.Font(None, 50)
game_over_font = pygame.font.Font(None, 50)

background = pygame.image.load("background.png").convert()
background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))

pygame.mixer.music.load("background.mp3")
pygame.mixer.music.set_volume(0.3)  # 50% volume

point_sound = pygame.mixer.Sound("point.mp3")
point_sound.set_volume(0.3)

game_over_sound = pygame.mixer.Sound("game over.mp3")
game_over_sound.set_volume(0.3)


x1 = 0
x2 = WIDTH
speed = 2

bird_image = pygame.image.load("bird.png").convert_alpha()
bird_width,bird_height = 160, 160
bird_image = pygame.transform.scale(bird_image, (bird_height, bird_width))
bird_tilt =0

pipes = [Pipe(1200, screen.get_height()), Pipe(1800, screen.get_height()), Pipe(2400, screen.get_height()), Pipe(3000,screen.get_height())]

bird = Bird(screen.get_width() / 4, screen.get_height() / 2)

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_started:
        x1 -= speed
        x2 -= speed

        if x1 <= -WIDTH:
            x1 =WIDTH
        if x2 <= -WIDTH:
            x2 = WIDTH

    screen.blit(background, (x1,0))
    screen.blit(background, (x2,0))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_SPACE]:
        if not game_started:
            game_started = True
            game_active = True
            pygame.mixer.music.play(loops=-1)
        else :
            bird.flap()

    if game_started:
        bird.update(dt, screen.get_height())

        if bird.velocity < 0:
            bird_tilt = 10
        elif bird.velocity > 0:
            bird_tilt = -20
        else:
            bird_tilt = 0
    
        for pipe in pipes:
            pipe.update(dt)
            pipe.draw(screen)
            farthest_pipe = max(pipes, key=lambda p : p.x).x
            top_rect, bottom_rect = pipe.get_rect()
        
            if not pipe.scored and bottom_rect.left < bird.rect.left:
                score += 1
                pipe.scored = True
                point_sound.play()

            if bird.rect.colliderect(top_rect) or bird.rect.colliderect(bottom_rect):
                bird.reset(screen.get_width() / 4, screen.get_height() / 2)
                game_started = False
                game_active = False
                pygame.mixer.music.pause()
                game_over_sound.play()

                for i, pipe in enumerate(pipes):
                    pipe.recycle(screen.get_width() + i * 600)
                    if score > high_score:
                        high_score = score
                    prev_score = score
                    score = 0

            if pipe.x + pipe.width < 0:
                new_x = farthest_pipe + 400
                pipe.recycle(new_x)
        
        if bird.rect.bottom >= screen.get_height():
            game_started = False
            game_active = False
            bird.reset(screen.get_width() / 4, screen.get_height() / 2)
            pygame.mixer.music.pause()
            game_over_sound.play()

            if score > high_score:
                high_score = score
            prev_score=score
            score=0

            for i, pipe in enumerate(pipes):
                pipe.recycle(screen.get_width() + i * 600)

    if not game_active:
        game_over_surface = game_over_font.render("GAME OVER", True, (255, 0, 0))
        game_over_rect = game_over_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 30 ))
        screen.blit(game_over_surface, game_over_rect)

        # high_score_surface = font.render(f"Your Score: {prev_score}", True, (255,0,0))
        # high_score_rect = high_score_surface.get_rect(center =(screen.get_width() // 2, screen.get_height() // 2 + 80))
        # screen.blit(high_score_surface, high_score_rect)

        restart_surface = font.render("Press SPACE to restart", True, (255, 255, 255))
        restart_rect = restart_surface.get_rect(center = (screen.get_width()// 2, screen.get_height()//2 + 80))
        screen.blit(restart_surface, restart_rect)

    bird_rotated = pygame.transform.rotate(bird_image, bird_tilt)
    rotated_rect = bird_rotated.get_rect(center=bird.rect.center)
    screen.blit(bird_rotated, rotated_rect.topleft)

    score_surface = font.render(f"Score: {score}  High Score: {high_score}", True, (0,0,0))
    score_rect = score_surface.get_rect(center=(200,50))
    screen.blit(score_surface, score_rect)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
