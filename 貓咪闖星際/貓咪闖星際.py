# 貓咪闖星際
import pygame
import random
import os

from pygame import transform

FPS = 60

WIDTH = 500
HEIGHT = 600

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)


#遊戲初始化 and 創建視窗
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode(size=(WIDTH, HEIGHT))
pygame.display.set_caption("貓咪闖星際")
clock = pygame.time.Clock()
running = True

#載入音樂、音效
shoot_s = pygame.mixer.Sound(os.path.join("sound", "C:\py348\貓咪闖星際\sound\shoot.wav"))
die_s = pygame.mixer.Sound(os.path.join("sound", "C:\py348\貓咪闖星際\sound\death.mp3"))
gun_s = pygame.mixer.Sound(os.path.join("sound", "C:\py348\貓咪闖星際\sound\pow1.wav"))
shield_s = pygame.mixer.Sound(os.path.join("sound", "C:\py348\貓咪闖星際\sound\pow0.wav"))
expl_s = [pygame.mixer.Sound(os.path.join("sound", "C:\py348\貓咪闖星際\sound\expl0.wav")),
    pygame.mixer.Sound(os.path.join("sound", "C:\py348\貓咪闖星際\sound\expl1.wav"))
]
#pygame.mixer.Sound.set_volume(0.5)
pygame.mixer.music.load(os.path.join("sound", "C:\py348\貓咪闖星際\sound\ground.mp3"))
pygame.mixer.music.set_volume(0.5)


#別的電腦上執行路徑
#background_imag = pygame.image.load(os.path.join("img", "background.png")).convert()
#player_imag = pygame.image.load(os.path.join("img", "嘟嘟貓4.png")).convert()
#rock_imag = pygame.image.load(os.path.join("img", "rock.png")).convert()
#bullet_imag = pygame.image.load(os.path.join("img", "嘟嘟貓肉球.png")).convert()

#載入圖型
background_imag = pygame.image.load(os.path.join("img", "C://py348//貓咪闖星際//img//background.png")).convert()
player_imag = pygame.image.load(os.path.join("img", "C://py348//貓咪闖星際//img//嘟嘟貓4.png")).convert()
player_mini_imag = pygame.image.load(os.path.join("img", "C://py348//貓咪闖星際//img//嘟嘟貓mini.png")).convert()
player_mini_imag = pygame.transform.scale(player_imag, (25,25))
player_mini_imag.set_colorkey(BLACK)
bullet_imag = pygame.image.load(os.path.join("img", "C://py348//貓咪闖星際//img//嘟嘟貓肉球.png")).convert()
rock_imag = []
for i in range(7):
    rock_imag.append(pygame.image.load(os.path.join("img", f"C://py348//貓咪闖星際//img//rock{i}.png")).convert())

expl_boom = {}
expl_boom['lg'] = []
expl_boom['sm'] = []
expl_boom['player'] = []
for i in range(9):
    expl_imag = pygame.image.load(os.path.join("img", f"C://py348//貓咪闖星際//img//expl{i}.png")).convert()
    expl_imag.set_colorkey(BLACK)
    expl_boom['lg'].append(pygame.transform.scale(expl_imag,(70,70)))
    expl_boom['sm'].append(pygame.transform.scale(expl_imag,(25,25)))
    player_expl_imag = pygame.image.load(os.path.join("img", f"C://py348//貓咪闖星際//img//player_expl{i}.png")).convert()
    player_expl_imag.set_colorkey(BLACK)
    expl_boom['player'].append(pygame.transform.scale(player_expl_imag,(70,70)))

power_imgs = {}
power_imgs['shield'] = pygame.image.load(os.path.join("img", "C://py348//貓咪闖星際//img//shield.png")).convert()
power_imgs['gun'] = pygame.image.load(os.path.join("img", "C:\py348\貓咪闖星際\img\gun.png")).convert()

pygame.display.set_icon(player_mini_imag)#遊戲ICON設定
font_name = os.path.join('1.ttf')
#font_name = pygame.font.match_font("arila")


def draw_text(surf, text, size,x,y): #文字顯示
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text,True,WHITE)#True >是使文字變得更滑順
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def draw_hp(surf, hp,x,y):#HP條顯示
    if hp <0:
        hp = 0
    BRA_LENGTH = 150
    BRA_HEIGHT = 10
    fill = (hp/150)*BRA_LENGTH
    outline_rect = pygame.Rect(x,y,BRA_LENGTH,BRA_HEIGHT)
    fill_rect = pygame.Rect(x,y,fill,BRA_HEIGHT)
    pygame.draw.rect(surf,GREEN,fill_rect)
    pygame.draw.rect(surf,WHITE,outline_rect,2)

def draw_lives(surf, lives, img, x, y):#生命值顯示
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30*i
        img_rect.y = y
        surf.blit(img, img_rect)

def draw_init():#初始畫面顯示
    screen.blit(background_imag, (0,0))
    draw_text(screen, "貓咪闖星際", 65, WIDTH/2 ,HEIGHT/4)
    draw_text(screen, "←  →移動貓貓，空白鍵射出肉球", 20, WIDTH/2 ,HEIGHT/2)
    draw_text(screen, "按任意鍵開始遊戲!", 18, WIDTH/2 ,HEIGHT* 3/4)
    pygame.display.update()
    waiting = True
    while(waiting):
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                waiting = False
                return False

class Player(pygame.sprite.Sprite):#玩家設定
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image =pygame.transform.scale(player_imag, (50,50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        #pygame.draw.circle(self.image, RED,self.rect.center,self.radius)
        self.rect.centerx = (WIDTH/2)
        self.rect.bottom = (HEIGHT - 10)
        self.speedx = 8
        #self.speedy = 8
        self.lives = 3
        self.hp = 150
        self.hidden = False
        self.hide_time = 0
        self.gun = 1
        self.gun_time = 0

    def update(self):
        now = pygame.time.get_ticks()
        if (self.gun >1 and now - self.gun_time > 5000):
            self.gun -= 1
            self.gun_time = now

        if (self.hidden and now - self.hide_time > 2000):
            self.hidden = False
            self.rect.centerx = (WIDTH/2)
            self.rect.bottom = (HEIGHT - 10)

        key_presse = pygame.key.get_pressed()
        if key_presse[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        
        if key_presse[pygame.K_LEFT]:
            self.rect.x -= self.speedx

        if key_presse[pygame.K_UP]:
            self.rect.y -= self.speedy

        if key_presse[pygame.K_DOWN]:
            self.rect.y -= self.speedy

        if self.rect.left > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    
    def shoot(self):
        if (not(self.hidden)):
            if (self.gun == 1):
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullet.add(bullets)
                shoot_s.play()
            elif (self.gun >= 2):
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_s.play()


    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2 , HEIGHT+500)
    
    def gunup(self):
        self.gun += 1
        self.gun_time = pygame.time.get_ticks()


class ROCK(pygame.sprite.Sprite):#m隕石設定
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(rock_imag)
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.radius = self.rect.width *0.80 / 2
        #pygame.draw.circle(self.image, RED,self.rect.center,self.radius)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-200, -100)
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(2, 10)
        self.total_degree = 0
        self.rot_degree = random.randrange(-3, 3)
        
    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedx = random.randrange(-3, 3)
            self.speedy = random.randrange(2, 10)

class Bullet(pygame.sprite.Sprite):#子彈設定
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_imag, (30,25))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10
        

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):#隕石碰撞設定
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_boom[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 40
        

    def update(self):
        now = pygame.time.get_ticks()
        if (now - self.last_update > self.frame_rate):
            self.last_update = now
            self.frame += 1 
            if (self.frame == len(expl_boom[self.size])):
                self.kill()
            else:
                self.image = expl_boom[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

class Power(pygame.sprite.Sprite):#寶物設定
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = power_imgs[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3
        

    def update(self):
        self.rect.y += self.speedy
        if (self.rect.top > HEIGHT):
            self.kill()

#遊戲設定群組化
all_sprites = pygame.sprite.Group()
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powers = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    r = ROCK()
    all_sprites.add(r)
    rocks.add(r)

score = 0
pygame.mixer.music.play(-1)
#遊戲迴圈
show_init = True
while running:
    if (show_init):
        close = draw_init()
        if (close):
            break
        show_init = False
        all_sprites = pygame.sprite.Group()
        rocks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powers = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            r = ROCK()
            all_sprites.add(r)
            rocks.add(r)
            
        score = 0

    clock.tick(FPS)
    #取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()


    #石頭被射中判斷
    all_sprites.update()
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
    for hit in hits:
        random.choice(expl_s).play()
        score += int(hit.radius)
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        #掉寶率 
        if (random.random() > 0.9):
            pow = Power(hit.rect.center)
            all_sprites.add(pow)
            powers.add(pow)
        r = ROCK()
        all_sprites.add(r)
        rocks.add(r)


    #貓貓遭石頭擊中判斷
    hits2 = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)
    for hit in hits2:
        r = ROCK()
        all_sprites.add(r)
        rocks.add(r)
        player.hp -= hit.radius
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl) 
        if player.hp <= 0:
            die = Explosion(player.rect.center, 'player')
            die_s.play()
            player.lives -= 1
            player.hp = 150
            player.hide()
            

    #吃寶物判定
    hits2 = pygame.sprite.spritecollide(player, powers, True)
    for hit in hits2:
        if (hit.type == 'shield'):
            player.hp += 20
            shield_s.play()
            if (player.hp > 150):
                player.hp = 150
        elif (hit.type == 'gun'):
            player.gunup()
            gun_s.play()



    #遊戲結束設定
    if (player.lives == 0 and  not die.alive()):
        show_init = True

    #畫面顯示
    screen.fill(BLACK)
    screen.blit(background_imag, (0,0))
    all_sprites.draw(screen)
    draw_text(screen, str(score),28,WIDTH/2,10)
    draw_hp(screen,player.hp,6,15)
    draw_lives(screen,player.lives,player_mini_imag,WIDTH - 100, 15)
    pygame.display.update()



pygame.quit()
