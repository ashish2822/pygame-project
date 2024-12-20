

from turtle import Screen
import cv2
import pygame
import time
import random
import sys
from button import Button


pygame.font.init()

clock = pygame.time.Clock()
pygame.mixer.init()
background_music = pygame.mixer.Sound('SkyFire (Title Screen).ogg')
level_clr_music = pygame.mixer.Sound('lvl_clr.mp3')

background_music.play(-1)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")

video = cv2.VideoCapture('BO LD.mp4')
video2 = cv2.VideoCapture('bg2.mp4')
video3 = cv2.VideoCapture('level2bg.mp4')
video4 = cv2.VideoCapture('level3bg.mp4')
BG = pygame.transform.scale(pygame.image.load('bg.png'), (WIDTH, HEIGHT))
BOSS = pygame.transform.scale(pygame.image.load('boss.png'), (100, 100))
BOSS2 = pygame.transform.scale(pygame.image.load('lv2boss.png'), (100, 100))
BOSS3 = pygame.transform.scale(pygame.image.load('boss3.png'), (100, 100))


PLAYER_WIDTH = 60
PLAYER_HEIGHT = 50

PLAYER = pygame.transform.scale(pygame.image.load('spaceship.png'), (70, 60))
FIREBALL = pygame.transform.scale(pygame.image.load('enemy.png'), (40, 50))
FIREBALL2 = pygame.transform.scale(pygame.image.load('enemy2.png'), (50, 60))
FIREBALL3 = pygame.transform.scale(pygame.image.load('enemy3.png'), (40, 50))
FIREBALL4 = pygame.transform.scale(pygame.image.load('enemy4.png'), (40, 50))
FIREBALL5 = pygame.transform.scale(pygame.image.load('enemy5.png'), (40, 50))
FIREBALL6 = pygame.transform.scale(pygame.image.load('enemy6.png'), (40, 50))
BULLET = pygame.transform.scale(pygame.image.load('bullet.png'),(20,30))


PLAYER_VEL = 5
BULLET_VEL = 10

STAR_WIDTH = 40
STAR_HEIGHT = 50
STAR2_WIDTH = 50
STAR2_HEIGHT = 60
STAR3_WIDTH = 40
STAR3_HEIGHT = 50
STAR4_WIDTH = 40
STAR4_HEIGHT = 50
STAR5_WIDTH = 40
STAR5_HEIGHT = 50
STAR6_WIDTH = 40
STAR6_HEIGHT = 50

STAR_VEL = 3
STAR2_VEL = 5
STAR3_VEL = 3
STAR4_VEL = 5
STAR5_VEL = 3
STAR6_VEL = 5

level = 1

FONT = pygame.font.SysFont("goudystout",20)


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 10, 20)

    def move(self):
        self.y -= BULLET_VEL
        self.rect.y = self.y

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1,6):
            img = pygame.image.load(f"img/exp{num}.png")
            img = pygame.transform.scale(img, (50,50))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 4

        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()


explosion_group = pygame.sprite.Group()


class Boss:
    def __init__(self, level):
        self.x = WIDTH / 2
        self.y = -BOSS.get_height()
        self.rect = pygame.Rect(self.x, self.y, BOSS.get_width(), BOSS.get_height())
        self.vel = 2
        self.health = 100 + (level - 1) * 50 # boss health

    def move(self):
        self.y += self.vel
        self.rect.y = self.y

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0

class Boss2:
    def __init__(self, level):
        self.x = WIDTH / 2
        self.y = -BOSS2.get_height()
        self.rect = pygame.Rect(self.x, self.y, BOSS2.get_width(), BOSS2.get_height())
        self.vel = 2
        self.health = 100 + (level - 1) * 50 # boss health

    def move(self):
        self.y += self.vel
        self.rect.y = self.y

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0

class Boss3:
    def __init__(self, level):
        self.x = WIDTH / 2
        self.y = -BOSS3.get_height()
        self.rect = pygame.Rect(self.x, self.y, BOSS3.get_width(), BOSS3.get_height())
        self.vel = 2
        self.health = 100 + (level - 1) * 50 # boss health

    def move(self):
        self.y += self.vel
        self.rect.y = self.y

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0

def draw_boss_health_bar(boss, x, y):
    health_bar_width = 100
    health_bar_height = 10
    health_bar_x = x - health_bar_width / 2 + 50
    health_bar_y = y - health_bar_height - 10
    pygame.draw.rect(WIN, "black", (health_bar_x, health_bar_y, health_bar_width, health_bar_height), 2)
    health_bar_fill_width = (boss.health / 100) * health_bar_width
    pygame.draw.rect(WIN, "red", (health_bar_x, health_bar_y, health_bar_fill_width, health_bar_height))


def draw_home_page():
    while True:
        # Get the current frame from the video
        ret, frame = video.read()
        if not ret:
            # If the video ends, restart it
            video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = video.read()

        
        rotetade_frame = cv2.rotate(frame,cv2.ROTATE_90_CLOCKWISE)
        flip_frame = cv2.flip(rotetade_frame,1)
        # Convert the resized frame to a Pygame surface
        frame_surface = pygame.surfarray.make_surface(flip_frame)

        # Blit the surface to the screen
        WIN.blit(frame_surface, (0,0))

        
        start_button = Button("start button.png",(525, 350),1)
        start_button.draw(WIN)

        quit_button = Button("quit button.png",(525, 450),1)
        quit_button.draw(WIN)


        pygame.display.update()
        clock.tick(60)

        # Check for events (e.g. mouse click on start button)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                # sys.exit()
            if start_button.is_pressed():
                main()  # Restart the game
            elif quit_button.is_pressed():
                pygame.quit()
                sys.exit()
                return


def levelClear():
    WIN.fill(BLACK)
    levelcleared = FONT.render("Level Cleared!", True, WHITE)
    WIN.blit(levelcleared, ((WIDTH/2 - (levelcleared.get_width()/2)),(HEIGHT/2 - (levelcleared.get_height()/2))))
    pygame.display.update()
    level_clr_music.play()
    pygame.time.delay(2000)

    level2()

def levelClear2():
    WIN.fill(BLACK)
    levelcleared = FONT.render("Level Cleared!", True, WHITE)
    WIN.blit(levelcleared, ((WIDTH/2 - (levelcleared.get_width()/2)),(HEIGHT/2 - (levelcleared.get_height()/2))))
    pygame.display.update()
    level_clr_music.play()
    pygame.time.delay(2000)

    level3()

def level2():
    global level
    run = True

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT,
                         PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0

    stars = []
    stars2 = []
    stars3 = []
    stars4 = []
    stars5 = []
    stars6 = []
    bullets = []
    hit = False
    global boss
    boss = None
    boss_time = 30

    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        # Get the current frame from the video
        ret, frame = video3.read()
        if not ret:
            # If the video ends, restart it
            video3.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = video3.read()

        rotetade_frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        flip_frame = cv2.flip(rotetade_frame, 1)
        # Convert the resized frame to a Pygame surface
        rgb_frame = cv2.cvtColor(flip_frame, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.surfarray.make_surface(rgb_frame)

        # Blit the surface to the screen
        WIN.blit(frame_surface, (0, 0))

        if elapsed_time > boss_time and boss is None:
            boss = Boss2(level)
            stars3 = []
            stars4 = []

        if boss:
            boss.move()
            WIN.blit(BOSS2, (boss.x, boss.y))

            if boss.y > HEIGHT:
                boss = None

            for bullet in bullets:
                if bullet.rect.colliderect(boss.rect):
                    bullets.remove(bullet)
                    pos = bullet.x, bullet.y
                    explosion = Explosion(pos[0], pos[1])
                    explosion_group.add(explosion)
                    boss.take_damage(10)
                    if boss.health <= 0:
                        boss = None
                        level +=1
                        levelClear2()
                        

            if boss.rect.colliderect(player):
                hit = True
                draw_restart_page()
            draw_boss_health_bar(boss, boss.x, boss.y)

        level_text = FONT.render(f"Level: {level}", 1, "white")
        WIN.blit(level_text, (WIDTH - level_text.get_width() - 10, 10))

        explosion_group.draw(WIN)
        explosion_group.update()

        if star_count > star_add_increment:
            for _ in range(2):
                star3_x = random.randint(0, WIDTH - STAR3_WIDTH)
                star3 = pygame.Rect(star3_x, -STAR3_HEIGHT, STAR3_WIDTH, STAR3_HEIGHT)
                stars3.append(star3)

                star4_x = random.randint(0, WIDTH - STAR4_WIDTH)
                star4 = pygame.Rect(star4_x, -STAR4_HEIGHT, STAR4_WIDTH, STAR4_HEIGHT)
                stars4.append(star4)

                star_add_increment = max(200, star_add_increment - 20)
                star_count = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shoot(player, bullets)
                    fire_sound()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL

        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL

        if keys[pygame.K_UP] and player.y + PLAYER_VEL >= 0:
            player.y -= PLAYER_VEL

        if keys[pygame.K_DOWN] and player.y - PLAYER_VEL - player.height <= HEIGHT:
            player.y += PLAYER_VEL

        for star3 in stars3[:]:
            star3.y += STAR3_VEL
            if star3.y > HEIGHT:
                stars3.remove(star3)
            else:
                for bullet in bullets[:]:
                    if star3.y >= bullet.y and star3.colliderect(bullet):
                        stars3.remove(star3)
                        bullets.remove(bullet)
                        pos = star3.x, star3.y
                        explosion = Explosion(pos[0], pos[1])
                        explosion_group.add(explosion)
                        break
            if star3.y + star3.height >= player.y and star3.colliderect(player):
                stars3.remove(star3)
                hit = True
                break

        for star4 in stars4[:]:
            star4.y += STAR4_VEL
            if star4.y > HEIGHT:
                stars4.remove(star4)
            else:
                for bullet in bullets[:]:
                    if star4.y >= bullet.y and star4.colliderect(bullet):
                        stars4.remove(star4)
                        bullets.remove(bullet)
                        pos = star4.x, star4.y
                        explosion = Explosion(pos[0], pos[1])
                        explosion_group.add(explosion)
                        break
            if star4.y + star4.height >= player.y and star4.colliderect(player):
                stars4.remove(star4)
                hit = True
                break

        for bullet in bullets[:]:
            bullet.move()
            if bullet.y < 0:
                bullets.remove(bullet)

        if hit:
            
            draw_restart_page()

        draw(player, elapsed_time, stars, bullets, stars2, stars3, stars4, stars5, stars6)

    pygame.quit()


    pygame.quit()

def level3():
    global level
    run = True

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT,
                         PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0

    stars = []
    stars2 = []
    stars3 = []
    stars4 = []
    stars5 = []
    stars6 = []
    bullets = []
    hit = False
    global boss
    boss = None
    boss_time = 30

    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        # Get the current frame from the video
        ret, frame = video4.read()
        if not ret:
            # If the video ends, restart it
            video4.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = video4.read()

        rotetade_frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        flip_frame = cv2.flip(rotetade_frame, 1)
        # Convert the resized frame to a Pygame surface
        rgb_frame = cv2.cvtColor(flip_frame, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.surfarray.make_surface(rgb_frame)

        # Blit the surface to the screen
        WIN.blit(frame_surface, (0, 0))

        if elapsed_time > boss_time and boss is None:
            boss = Boss3(level)
            stars5 = []
            stars6 = []

        if boss:
            boss.move()
            WIN.blit(BOSS3, (boss.x, boss.y))

            if boss.y > HEIGHT:
                boss = None

            for bullet in bullets:
                if bullet.rect.colliderect(boss.rect):
                    bullets.remove(bullet)
                    pos = bullet.x, bullet.y
                    explosion = Explosion(pos[0], pos[1])
                    explosion_group.add(explosion)
                    boss.take_damage(10)
                    if boss.health <= 0:
                        boss = None
                        level +=1

                        draw_restart_page()

            if boss.rect.colliderect(player):
                hit = True
                draw_restart_page()
            draw_boss_health_bar(boss, boss.x, boss.y)

        level_text = FONT.render(f"Level: {level}", 1, "white")
        WIN.blit(level_text, (WIDTH - level_text.get_width() - 10, 10))

        explosion_group.draw(WIN)
        explosion_group.update()

        if star_count > star_add_increment:
            for _ in range(2):
                star5_x = random.randint(0, WIDTH - STAR5_WIDTH)
                star5 = pygame.Rect(star5_x, -STAR5_HEIGHT, STAR5_WIDTH, STAR5_HEIGHT)
                stars5.append(star5)

                star6_x = random.randint(0, WIDTH - STAR6_WIDTH)
                star6 = pygame.Rect(star6_x, -STAR6_HEIGHT, STAR6_WIDTH, STAR6_HEIGHT)
                stars6.append(star6)

                star_add_increment = max(200, star_add_increment - 20)
                star_count = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shoot(player, bullets)
                    fire_sound()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL

        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL

        if keys[pygame.K_UP] and player.y + PLAYER_VEL >= 0:
            player.y -= PLAYER_VEL

        if keys[pygame.K_DOWN] and player.y - PLAYER_VEL - player.height <= HEIGHT:
            player.y += PLAYER_VEL

        for star5 in stars5[:]:
            star5.y += STAR5_VEL
            if star5.y > HEIGHT:
                stars5.remove(star5)
            else:
                for bullet in bullets[:]:
                    if star5.y >= bullet.y and star5.colliderect(bullet):
                        stars5.remove(star5)
                        bullets.remove(bullet)
                        pos = star5.x, star5.y
                        explosion = Explosion(pos[0], pos[1])
                        explosion_group.add(explosion)
                        break
            if star5.y + star5.height >= player.y and star5.colliderect(player):
                stars5.remove(star5)
                hit = True
                break

        for star6 in stars6[:]:
            star6.y += STAR6_VEL
            if star6.y > HEIGHT:
                stars6.remove(star6)
            else:
                for bullet in bullets[:]:
                    if star6.y >= bullet.y and star6.colliderect(bullet):
                        stars6.remove(star6)
                        bullets.remove(bullet)
                        pos = star6.x, star6.y
                        explosion = Explosion(pos[0], pos[1])
                        explosion_group.add(explosion)
                        break
            if star6.y + star6.height >= player.y and star6.colliderect(player):
                stars6.remove(star6)
                hit = True
                break

        for bullet in bullets[:]:
            bullet.move()
            if bullet.y < 0:
                bullets.remove(bullet)

        if hit:
            
            draw_restart_page()

        draw(player, elapsed_time, stars, bullets, stars2, stars3, stars4, stars5, stars6)

    pygame.quit()


    pygame.quit()



def draw_restart_page():
    while True:
        # Get the current frame from the video
        ret, frame = video.read()
        if not ret:
            # If the video ends, restart it
            video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = video.read()

        
        rotetade_frame = cv2.rotate(frame,cv2.ROTATE_90_CLOCKWISE)
        flip_frame = cv2.flip(rotetade_frame,1)
        # Convert the resized frame to a Pygame surface
        frame_surface = pygame.surfarray.make_surface(flip_frame)

        # Blit the surface to the screen
        WIN.blit(frame_surface, (0,0))
        
        # Add your home page elements (title, restart button, etc.)
        if boss is None:
            result = "YOU WON"
        else:
            result ="GAME OVER"
        title_text = FONT.render(f"{result}", 1, "white")
        WIN.blit(title_text, (WIDTH / 2 - title_text.get_width() / 2, HEIGHT / 2 - title_text.get_height() / 2 - 50))


      

        restart_button = Button("restart button.png",(525, 330),1)
        restart_button.draw(WIN)

        quit_button = Button("quit button.png",(525, 400),1)
        quit_button.draw(WIN)

        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if restart_button.is_pressed():
                main()  # Restart the game
            elif quit_button.is_pressed():
                pygame.quit()
                sys.exit()

def draw(player, elapsed_time, stars, bullets, stars2, stars3, stars4, stars5, stars6):
   
    time_text = FONT.render(f"Score: {round(elapsed_time)}", 1, "white")
    WIN.blit(time_text, (10, 10))

    WIN.blit(PLAYER, (player.x, player.y))

    for star in stars:
        WIN.blit(FIREBALL, (star.x, star.y))

    for star2 in stars2:
        WIN.blit(FIREBALL2,(star2.x, star2.y))

    for star3 in stars3:
        WIN.blit(FIREBALL3,(star3.x, star3.y))

    for star4 in stars4:
        WIN.blit(FIREBALL4,(star4.x, star4.y))

    for star5 in stars5:
        WIN.blit(FIREBALL5,(star5.x, star5.y))

    for star6 in stars6:
        WIN.blit(FIREBALL6,(star6.x, star6.y))
   
    for bullet in bullets:
        WIN.blit(BULLET, (bullet.x, bullet.y))

    pygame.display.update()

def shoot(player, bullets):
    bullet = Bullet(player.x + player.width / 2, player.y)
    bullets.append(bullet)

def fire_sound():
    pygame.mixer.init()
    fire_music = pygame.mixer.Sound('laser-gun-72558 (mp3cut.net).mp3')
  
    fire_music.play(0)


def main():
    global level
    run = True

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT,
                         PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0

    stars = []
    stars2 = []
    stars3 = []
    stars4 = []
    stars5 = []
    stars6 = []
    bullets = []
    hit = False

    global boss
    
    boss = None
    boss_time = 30

    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        # Get the current frame from the video
        ret, frame = video2.read()
        if not ret:
            # If the video ends, restart it
            video2.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = video2.read()

       
        rotetade_frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        flip_frame = cv2.flip(rotetade_frame, 1)
        # Convert the resized frame to a Pygame surface

        rgb_frame = cv2.cvtColor(flip_frame, cv2.COLOR_BGR2RGB)

        frame_surface = pygame.surfarray.make_surface(rgb_frame)

        # Blit the surface to the screen
        WIN.blit(frame_surface, (0, 0))

        if elapsed_time > boss_time and boss is None:
            boss = Boss(level)
            stars = []
            stars2 = []

        if boss:
            boss.move()
            WIN.blit(BOSS, (boss.x, boss.y))

            if boss.y > HEIGHT:
                boss = None

            for bullet in bullets:
                if bullet.rect.colliderect(boss.rect):
                    bullets.remove(bullet)
                    pos = bullet.x, bullet.y
                    explosion = Explosion(pos[0], pos[1])
                    explosion_group.add(explosion)
                    boss.take_damage(10)
                    if boss.health <= 0:
                        boss = None
                        level +=1
                        levelClear()

            if boss.rect.colliderect(player):
                hit = True
                draw_restart_page()
            draw_boss_health_bar(boss, boss.x, boss.y)

        level_text = FONT.render(f"Level: {level}", 1, "white")
        WIN.blit(level_text, (WIDTH - level_text.get_width() - 10, 10))

        if star_count > star_add_increment:
            for _ in range(2):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

                star2_x = random.randint(0, WIDTH - STAR2_WIDTH)
                star2 = pygame.Rect(star2_x, -STAR2_HEIGHT, STAR2_WIDTH, STAR2_HEIGHT)
                stars2.append(star2)

                star_add_increment = max(200, star_add_increment - 20)
                star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shoot(player, bullets)
                    fire_sound()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL

        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL

        if keys[pygame.K_UP] and player.y + PLAYER_VEL >= 0:
            player.y -= PLAYER_VEL

        if keys[pygame.K_DOWN] and player.y - PLAYER_VEL - player.height <= HEIGHT:
            player.y += PLAYER_VEL

        explosion_group.draw(WIN)
        explosion_group.update()

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            else:
                for bullet in bullets[:]:
                    if star.y >= bullet.y and star.colliderect(bullet):
                        stars.remove(star)
                        bullets.remove(bullet)
                        pos = star.x, star.y
                        explosion = Explosion(pos[0], pos[1])
                        explosion_group.add(explosion)
                        break
            if star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        for star2 in stars2[:]:
            star2.y += STAR2_VEL
            if star2.y > HEIGHT:
                stars2.remove(star2)
            else:
                for bullet in bullets[:]:
                    if star2.y >= bullet.y and star2.colliderect(bullet):
                        stars2.remove(star2)
                        bullets.remove(bullet)
                        pos = star2.x, star2.y
                        explosion = Explosion(pos[0], pos[1])
                        explosion_group.add(explosion)
                        break
            if star2.y + star2.height >= player.y and star2.colliderect(player):
                stars2.remove(star2)
                hit = True
                break

        for bullet in bullets[:]:
            bullet.move()
            if bullet.y < 0:
                bullets.remove(bullet)

        if hit:
           
            draw_restart_page()

        draw(player, elapsed_time, stars,bullets, stars2, stars3, stars4, stars5, stars6)

    pygame.quit()


    pygame.quit()

if __name__ == "__main__":
    draw_home_page()
pygame.mixer.quit()
    