from pygame import *
from random import randint
font.init()
font1 = font.SysFont('Comic Sans', 28)
win_lose = font.SysFont('Comic Sans', 64)
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')
window = display.set_mode((720, 500))
display.set_caption('Overfortolantexwatch legends')
background = transform.scale(image.load('shalun_background.png'), (720, 500))

class GameSprite(sprite.Sprite):
    def __init__(self, filename, w, h, speed, x, y):
        super().__init__()
        self.image = transform.scale(
            image.load(filename),
            (w, h)
        )
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image,
                    (self.rect.x, self.rect.y)
                    )

class Player(GameSprite):
    def __init__(self, filename, w, h, speed, x, y):
        super().__init__(filename, w, h, speed, x, y)
        self.rotate_count =80
        self.rotate_active = False
        self.h, self.w = h, w
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
            if self.rotate_active:
                self.rotate_count -= 1
                if self.rotate_count % 4 == 0:
                # self.image = transform.flip(self.image, 0, 1)
                    self.image = transform.rotate(self.image, -90)
                if self.rotate_count <= 0:
                    self.rotate_active = False
        if keys_pressed[K_d] and self.rect.x < 700:
            self.rect.x += self.speed
            if self.rotate_active:
                self.rotate_count -= 1
                # self.image = transform.flip(self.image, 0, 1)
                if self.rotate_count % 4 == 0:


                    self.image = transform.rotate(self.image, 90)


                if self.rotate_count <= 0:
                    self.rotate_active = False
    
    def fire(self):
        bullet = Bullet('pirojhok.png', 15, 20, 6, self.rect.centerx, self.rect.top)
        bullets.add(bullet)
        fire.play()
    def rotanie(self):
        if self.rotate_active == False:
            self.rotate_active = True
            self.rotate_count = 80
        
            

    


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 500:
            lost += 1
            self.rect.y = 0
            self.rect.x = randint(0, 650)
            self.speed = randint(1, 3)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

bullets = sprite.Group()

spedy1 = randint(1, 3)
spedy2 = randint(1, 3)
spedy3 = randint(1, 3)
spedy4 = randint(1, 3)
spedy5 = randint(1, 3)
spedy6 = randint(1, 3)
monsters = sprite.Group()
monsters.add(Enemy('geno_zlody.png', 75, 65, spedy2, 120, 0))
monsters.add(Enemy('geno_zlody.png', 75, 65, spedy3, 240, 0))
monsters.add(Enemy('geno_zlody.png', 75, 65, spedy1, 50, 0))
monsters.add(Enemy('geno_zlody.png', 75, 65, spedy4, 360, 0))
monsters.add(Enemy('geno_zlody.png', 75, 65, spedy5, 480, 0))
monsters.add(Enemy('geno_zlody.png', 75, 65, spedy6, 600, 0))

menu_btn = GameSprite('pirojhok.png', 200, 160, 0, 300, 300)

lost = 0
score = 0

player = Player('druzhok_lazers_from_eyes.png', 75, 65, 5, 360, 420)
clock = time.Clock()
game = True
finish = True
menu = True
text_win = win_lose.render(
    'YOU WIN!', 1, (0, 255, 0)
)
text_lose = win_lose.render(
    'YOU LOSE!', 1, (255, 0, 0)
)
while game == True:
    if finish == False:
        text_missed = font1.render(
            'Missed: ' + str(lost), 1, (255, 255, 255)
        )
        text_score = font1.render(
            'Score: ' + str(score), 1, (255, 255, 255)
        )
        window.blit(background, (0, 0))
        window.blit(text_missed, (10, 30))
        window.blit(text_score, (10, 10))
        player.reset()
        bullets.update()
        bullets.draw(window)
        monsters.update()
        monsters.draw(window)
        for e in event.get():
            if e.type == QUIT:
                game = False
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    player.fire()
                if e.key == K_q:
                    player.rotanie()

    monsters_list = sprite.groupcollide(monsters, bullets, True, True)
    for monster in monsters_list:
        score += 1
        monster_ = Enemy('geno_zlody.png', 75, 65, 3, randint(0, 635), 0)
        monsters.add(monster_)
    if score >= 10:
        finish = True
        window.blit(text_win, (265, 200))
    if lost >= 3:
        finish = True
        window.blit(text_lose, (260, 200))
    if sprite.spritecollide(player, monsters, True):
        finish = True
        window.blit(text_lose, (200, 200))

    if menu == True:
        window.blit(background,(0, 0))
        menu_btn.reset()
        for e in event.get():
            if e.type == QUIT:
                game = False
           
            if e.type == MOUSEBUTTONDOWN:
                x, y = e.pos
                if menu_btn.rect.collidepoint(x, y):
                    menu = False
                    finish = False

    if finish == True and menu == False:
        for e in event.get():
            if e.type == QUIT:
                game = False
    
    if finish == True and menu == False:
        for e in event.get():
            if e.type == QUIT:
                game = False 

    clock.tick(100)
    display.update()
    player.update()