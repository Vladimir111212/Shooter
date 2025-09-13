from pygame import *
from random import randint
import time as tm
init()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, height, weight):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (height, weight))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x       
        self.rect.y = player_y
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        if keys_press[K_a] and self.rect.x > -5:
            self.rect.x -= self.speed
        if keys_press[K_d] and self.rect.x < 650:
            self.rect.x += self.speed
    def fire(self):
        global bullets
        bullet = Bullet('bullet.png', self.rect.centerx - 6, 610, 10, 15, 8)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost_enemy
        if self.rect.y >= 700:
            lost_enemy += 1
            self.rect.x = randint(0, 650)
            self.rect.y = 0

            
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()           
            


class Asteroids(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 700:
            self.rect.x = randint(0, 650)
            self.rect.y = 0





health = 3
finish = False
win = display.set_mode((700, 700))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (700, 700))
music = mixer.music.load('space.ogg')
font1 = font.Font(None, 80)
window1 = font1.render('YOU WIN!', True, (255, 220, 6))
font2 = font.Font(None, 80)
window2 = font2.render('YOU LOSE!', True, (255, 220, 6))
font3 = font.Font(None, 80)
window3 = font3.render(str(health), True, (255, 0, 0))
font4 = font.Font(None, 30)
window4 = font4.render('Wait, reload:', True, (255, 0, 0))
mixer.music.play()
fire = mixer.Sound('fire.ogg')
sprite1 = Player('rocket.png', 0, 620, 6, 50, 50)
sprite2 = Enemy('ufo.png', randint(0, 650), 0, randint(1, 2), 50, 50)
sprite3 = Enemy('ufo.png', randint(0, 650), 0, randint(1, 2), 50, 50)
sprite4 = Enemy('ufo.png', randint(0, 650), 0, randint(1, 2), 50, 50)
sprite5 = Enemy('ufo.png', randint(0, 650), 0, randint(1, 2), 50, 50)
sprite6 = Enemy('ufo.png', randint(0, 650), 0, randint(1, 2), 50, 50)
asteroid1 = Asteroids('asteroid.png', randint(0, 650), 0, randint(1, 2), 50, 50)
asteroid2 = Asteroids('asteroid.png', randint(0, 650), 0, randint(1, 2), 50, 50)
asteroid3 = Asteroids('asteroid.png', randint(0, 650), 0, randint(1, 2), 50, 50)            
asteroid4 = Asteroids('asteroid.png', randint(0, 650), 0, randint(1, 2), 50, 50)


font1 = font.Font(None, 36)






num_fire = 0
reload_time = False
lost_enemy = 0
killed_enemy = 0
bullets = sprite.Group()
monsters = sprite.Group()
asteroids = sprite.Group()
monsters.add(sprite2)
monsters.add(sprite3)
monsters.add(sprite4)
monsters.add(sprite5)
monsters.add(sprite6)
asteroids.add(asteroid1)
asteroids.add(asteroid2)
asteroids.add(asteroid3)
asteroids.add(asteroid4)
clock = time.Clock()
FPS = 60


game = True
while game:
    keys_press = key.get_pressed()
    if finish != True:
        text_lose = font1.render('Пропущено врагов:' + str(lost_enemy), 1, (200, 255, 240))
        text_win = font1.render('убито врагов:' + str(killed_enemy), 1, (200, 255, 240))

        if keys_press[K_SPACE]:
            if num_fire < 5 and reload_time == False:
                sprite1.fire()
                fire.play()
                num_fire += 1
            if num_fire >= 5 and reload_time == False:
                reload_time = True
                sec = tm.time()
            

        win.blit(background, (0, 0))
        win.blit(text_lose, (0, 0))
        win.blit(text_win, (0, 30))
        sprite1.reset()
        sprite1.update()
        monsters.draw(win)
        monsters.update()
        asteroids.draw(win)
        asteroids.update()
        bullets.draw(win)
        bullets.update()
        win.blit(window3, (650, 20))
        collides = sprite.groupcollide(monsters, bullets, True, True)
        collide_monster = sprite.spritecollide(sprite1, monsters, True)
        collide_asteroid = sprite.spritecollide(sprite1, asteroids, True)



        for y in collides:
            killed_enemy += 1
            sprite8 = Enemy('ufo.png', randint(0, 650), 0, randint(1, 2), 50, 50)
            monsters.add(sprite8)
        if killed_enemy >= 10:
            win.blit(window1, (200, 200))
            finish = True
            mixer.music.stop()
        if lost_enemy >= 3:
            win.blit(window2, (200, 200))
            finish = True
            mixer.music.stop()
        
        if health <= 0:
            win.blit(window2, (200, 200))
            finish = True
            mixer.music.stop()

        for clash in collide_monster:
            sprite8 = Enemy('ufo.png', randint(0, 650), 0, randint(1, 2), 50, 50)
            health -= 1
            window3 = font3.render(str(health), True, (255, 0, 0))
            monsters.add(sprite8)
            

        for bump in collide_asteroid:
            asteroid4 = Asteroids('asteroid.png', randint(0, 650), 0, randint(1, 2), 50, 50)
            health -= 1
            window3 = font3.render(str(health), True, (255, 0, 0))
            asteroids.add(asteroid4) 

        if reload_time == True:
            if tm.time() - sec < 2:
                win.blit(window4, (500, 650))
            else:
                num_fire = 0
                reload_time = False
            
                    
    if finish == True:
        if keys_press[K_r]:
            finish = False
            mixer.music.play()
            lost_enemy = 0
            health = 3
            window3 = font3.render(str(health), True, (255, 0, 0))
            sprite1.rect.x = 350
            sprite1.rect.y = 620
            for monster in monsters:
                monster.kill()
            for collet in bullets:
                collet.kill()
            for meteor in asteroids:
                meteor.kill()
            sprite8 = Enemy('ufo.png', randint(0, 650), 0, randint(1, 2), 50, 50)
            sprite9 = Enemy('ufo.png', randint(0, 650), 0, randint(1, 2), 50, 50)
            sprite10 = Enemy('ufo.png', randint(0, 650), 0, randint(1, 2), 50, 50)
            sprite11 = Enemy('ufo.png', randint(0, 650), 0, randint(1, 2), 50, 50)
            sprite12 = Enemy('ufo.png', randint(0, 650), 0, randint(1, 2), 50, 50)
            monsters.add(sprite8)
            monsters.add(sprite9)
            monsters.add(sprite10)
            monsters.add(sprite11)
            monsters.add(sprite12)

            asteroid5 = Asteroids('asteroid.png', randint(0, 650), 0, randint(1, 2), 50, 50)
            asteroid6 = Asteroids('asteroid.png', randint(0, 650), 0, randint(1, 2), 50, 50)
            asteroid7 = Asteroids('asteroid.png', randint(0, 650), 0, randint(1, 2), 50, 50)                       
            asteroid8 = Asteroids('asteroid.png', randint(0, 650), 0, randint(1, 2), 50, 50)
            
            asteroids.add(asteroid5)
            asteroids.add(asteroid6)
            asteroids.add(asteroid7)
            asteroids.add(asteroid8)
            print('нажата кнопка')
        



    for i in event.get():
        if i.type == QUIT:
            game = False
    clock.tick(FPS)
    display.update()
        







































