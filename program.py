import pygame
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battlefields")

BG = pygame.transform.scale(pygame.image.load("bg.png"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 40

PLAYER_VEL = 10
BULLET_WIDTH = 10
BULLET_HEIGHT = 10
BULLET_VEL = 20

FONT = pygame.font.SysFont("comicsans", 30)

def draw(player, rounds, bullets, healthbar):
    WIN.blit(BG, (0, 0))
    
    round_count = FONT.render(f"Fired Rounds: {round(rounds)}", 1, "white")
    WIN.blit(round_count, (10, 10))

    pygame.draw.rect(WIN, "dark green", player)

    pygame.draw.rect(WIN, "green", healthbar)

    for bullet in bullets:
        pygame.draw.rect(WIN, "black", bullet)

    pygame.display.update()

def reset_game():
    player = pygame.Rect(WIDTH / 2, HEIGHT - PLAYER_HEIGHT - 40, PLAYER_WIDTH, PLAYER_HEIGHT)
    rounds = 0
    health = 100
    healthbar = pygame.Rect(10, HEIGHT - 30, health, 10)
    star_add_increment = 2000
    star_count = 0
    bullets = []
    hit = False
    dead = False
    return player, rounds, health, healthbar, star_add_increment, star_count, bullets, hit, dead

def main():
    run = True
    clock = pygame.time.Clock()
    start_time = time.time()
    player, rounds, health, healthbar, star_add_increment, star_count, bullets, hit, dead = reset_game()

    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(12):
                star_x = random.randint(0, WIDTH - BULLET_WIDTH)
                bullet = pygame.Rect(star_x, -BULLET_HEIGHT, BULLET_WIDTH, BULLET_HEIGHT)
                bullets.append(bullet)
            rounds += 1
            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and dead:
                    player, rounds, health, healthbar, star_add_increment, star_count, bullets, hit, dead = reset_game()
                    start_time = time.time()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL

        for bullet in bullets[:]:
            bullet.y += BULLET_VEL
            if bullet.y > HEIGHT:
                bullets.remove(bullet)
            elif bullet.y + bullet.height >= player.y and bullet.colliderect(player):
                bullets.remove(bullet)
                hit = True
                break

        if hit:
            damage = random.randint(1,10)
            health -= damage * 10
            health = max(health, 0)
            healthbar = pygame.Rect(10, HEIGHT - 30, health, 10)
            if health <= 0:
                dead = True
            hit = False

        if dead:
            lost_text = FONT.render("You were fatally shot! Press R to restart", 1, "red")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
        else:
            draw(player, rounds, bullets, healthbar)

    pygame.quit()

if __name__ == "__main__":
    main()