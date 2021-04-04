import pygame, random, time, math
from random import *
vec = pygame.math.Vector2
from abc import ABC, abstractmethod

pygame.init()
clock = pygame.time.Clock()
infoparam = pygame.display.Info()
p1, p2 = int(0.9 * float(infoparam.current_w)), int(0.9 * float(infoparam.current_h))
screen = pygame.display.set_mode((p1, p2))
game_size_x = 5000
game_size_y = 3000
corn = pygame.image.load("corn.png")
cloud = pygame.image.load("cloud.png")
sunrise = pygame.image.load("sunrise.png")
waterhouse1 = pygame.image.load("water_tower1.png")
waterhouse2 = pygame.image.load("water_tower2.png")
watprop = waterhouse1.get_width()
ca = corn.get_width()
icon = pygame.image.load("player1.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("A-maiz-ing fall")
game_over = False
intro = False
score = 0
intro = True

# Camera settings
class Camera:
    def __init__(self, player):
        self.player = player
        self.offset = vec(0, 0)
        self.offset_float = vec(0, 0)
        self.DISPLAY_W, self.DISPLAY_H = infoparam.current_w, infoparam.current_h
        self.CONST = vec(-self.DISPLAY_W / 2, -self.DISPLAY_H / 2)

    def setmethod(self, method):
        self.method = method

    def scroll(self):
        self.method.scroll()


class CamScroll(ABC):
    def __init__(self, camera, player):
        self.camera = camera
        self.player = player

    @abstractmethod
    def scroll(self):
        pass


class Follow(CamScroll):
    def __init__(self, camera, player):
        CamScroll.__init__(self, camera, player)

    def scroll(self):
        self.camera.offset_float.x += (
            self.player.pos_x - self.camera.offset_float.x + self.camera.CONST.x
        )
        self.camera.offset_float.y += (
            self.player.pos_y - self.camera.offset_float.y + self.camera.CONST.y
        )
        self.camera.offset.x, self.camera.offset.y = (
            int(self.camera.offset_float.x),
            int(self.camera.offset_float.y),
        )

class none(CamScroll):
    def __init__(self, camera, player):
        CamScroll.__init__(self, camera, player)

    def scroll(self):
        pass

class Border(CamScroll):
    def __init__(self, camera, player):
        CamScroll.__init__(self, camera, player)

    def scroll(self):
        self.camera.offset_float.x += (
            self.player.rect.x - self.camera.offset_float.x + self.camera.CONST.x
        )
        self.camera.offset_float.y += (
            self.player.rect.y - self.camera.offset_float.y + self.camera.CONST.y
        )
        self.camera.offset.x, self.camera.offset.y = (
            int(self.camera.offset_float.x),
            int(self.camera.offset_float.y),
        )
        self.camera.offset.x = max(0, self.camera.offset.x)
        self.camera.offset.x = min(self.camera.offset.x, 5000 - self.camera.DISPLAY_W)
        self.camera.offset.y = max(0, self.camera.offset.y)
        self.camera.offset.y = min(self.camera.offset.y, 3000 - self.camera.DISPLAY_H)



class Actor:
    def __init__(self, x, y, w, h):
        self.pos_x = x
        self.pos_y = y
        self.w = w
        self.h = h


class Player(Actor):
    def __init__(self):
        Actor.__init__(
            self,
            p1//2,
            p2//2,
            32,
            32,
        )
        self.image = pygame.image.load("pp2.png")
        self.original_image = pygame.image.load("pp1.png")
        self.rect = self.original_image.get_rect()
        self.rect.centerx = round(self.pos_x + self.w // 2)
        self.rect.centery = round(self.pos_y + self.h // 2)

        self.speed = 12
        self.mode = 1

        self.x_move = 0
        self.y_move = 0

        self.x_momentum = 0
        self.y_momentum = 0

        self.mass = 0.7

    def rotate(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.pos_x+camera.offset.x, mouse_y - self.pos_y+camera.offset.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(self.original_image, int(angle))
        self.rect = self.image.get_rect(
            center=(round(self.pos_x + self.w // 2), round(self.pos_y + self.h // 2))
        )
        # self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))

    def move(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - self.pos_x+camera.offset.x
        dy = mouse_y - self.pos_y+camera.offset.y
        angle = math.atan2(dy, dx)

        if (
            math.sqrt(((mouse_x - self.pos_x) ** 2) + ((mouse_y - self.pos_y) ** 2))
            < 100
        ):
            self.speed = 0
        else:
            self.speed = 12

        # self.x_move += self.x_momentum
        # self.y_move += self.y_momentum

        if player_move == True:
            self.x_move += self.speed * math.cos(angle)
            self.y_move += self.speed * math.sin(angle)

        self.x_momentum += self.x_move * self.mass
        self.y_momentum += self.y_move * self.mass

        if self.x_momentum > 1:
            self.x_momentum -= 1
        elif self.x_momentum < -1:
            self.x_momentum += 1
        else:
            self.x_momentum = 0

        if self.y_momentum > 1:
            self.y_momentum -= 1
        elif self.y_momentum < -1:
            self.y_momentum += 1
        else:
            self.y_momentum = 0

        player.y_momentum += 3

        if self.x_momentum > 50:
            self.x_momentum = 50

        if self.x_momentum < -50:
            self.x_momentum = -50

        if self.y_momentum > 50:
            self.y_momentum = 50

        if self.y_momentum < -50:
            self.y_momentum = -50

        self.pos_x += self.x_move + self.x_momentum
        self.pos_y += self.y_move + self.y_momentum

    def draw(self):
        screen.blit(self.image, (self.pos_x-camera.offset.x, self.pos_y-camera.offset.y))


class Projectile(Actor):
    def __init__(self):
        Actor.__init__(
            self,
            round(player.pos_x + player.w // 2),
            round(player.pos_y + player.h // 2),
            32,
            32,
        )
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - self.pos_x+camera.offset.x
        dy = mouse_y - self.pos_y+camera.offset.y
        self.angle = math.atan2(dy, dx)
        self.image = pygame.image.load("bulla.png")
        self.original_image = pygame.image.load("bulla.png")
        rel_x, rel_y = mouse_x - self.pos_x+camera.offset.x, mouse_y - self.pos_y+camera.offset.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(self.original_image, int(angle))
        self.rect = self.image.get_rect(
            center=(round(self.pos_x + self.w // 2), round(self.pos_y + self.h // 2))
        )
        self.speed = 120
    
    def rotate(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.pos_x+camera.offset.x, mouse_y - self.pos_y+camera.offset.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(self.original_image, int(angle))
        self.rect = self.image.get_rect(
            center=(round(self.pos_x + self.w // 2), round(self.pos_y + self.h // 2))
        )
        # self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))

    def draw(self):
        global e_list
        screen.blit(self.image, (self.pos_x-camera.offset.x, self.pos_y-camera.offset.y))
        for enemy in e_list:    
            if (enemy.x<=self.pos_x<=enemy.x+enemy.w or enemy.x<=self.pos_x+self.w<=enemy.x+enemy.w) and (enemy.y<=self.pos_y<=enemy.y+enemy.h or enemy.y<=self.pos_y+self.h<=enemy.y+enemy.h):
                kill_enemy(e_list.index(enemy))
    def move(self):
        self.pos_x += self.speed * math.cos(self.angle)
        self.pos_y += self.speed * math.sin(self.angle)


mouse_x, mouse_y = pygame.mouse.get_pos()
player = Player()
camera = Camera(player)
none = none(camera,player)
follow = Follow(camera, player)
border = Border(camera, player)
camera.setmethod(follow)
player_move = False

projectiles = []

def redraw():
    global e_list, game_over, projectiles, score, r_list
    player.draw()
    player.move()
    for item in e_list:
        item.draw(e_list.index(item),r_list[e_list.index(item)])

    for projectile in projectiles:
        projectile.draw()

    test_rect_1 = pygame.Rect(-2000-camera.offset.x, game_size_y - 20- camera.offset.y, game_size_x+4000, 400)
    test_rect_2 = pygame.Rect(0-camera.offset.x, 0- camera.offset.y, game_size_x, 20)
    test_rect_3 = pygame.Rect(0-camera.offset.x, 0- camera.offset.y, 20, game_size_y)
    test_rect_4 = pygame.Rect(game_size_x - 20-camera.offset.x, 0- camera.offset.y, 20, game_size_y)
    
    if player.pos_y+player.h>=game_size_y-20:
        game_over = True
    else:
        pygame.draw.rect(screen, (203,145,84), test_rect_1)

    if player.pos_y+player.h<=0:
        game_over = True
    else:
        pygame.draw.rect(screen, (110,182,255), test_rect_2)

    if player.pos_x+player.w>=game_size_x:
        game_over = True
    else:
        pygame.draw.rect(screen, (110,182,255), test_rect_3)

    if player.pos_x+player.w<=0:
        game_over = True
    else:
        pygame.draw.rect(screen, (110,182,255), test_rect_4)
    
    screen.blit(waterhouse1, (1100-watprop-camera.offset.x,0-camera.offset.y))
    screen.blit(waterhouse2, (-1050+game_size_x-camera.offset.x,0-camera.offset.y))
    cloud_par = cloud.get_width()
    cloudh = cloud.get_height()
    for number in range(math.ceil(game_size_x/cloud_par)*-2,math.ceil(game_size_x/cloud_par)*2):
            screen.blit(cloud, (0+(number*cloud_par)-camera.offset.x,0-40-camera.offset.y))
            screen.blit(cloud, (0+(number/1.5*cloud_par)-camera.offset.x,0-40-camera.offset.y))
            screen.blit(cloud, (0+(number/1.2*cloud_par)-camera.offset.x,0-40-camera.offset.y))
    camera.scroll()
    font = pygame.font.SysFont('Arial',50)
    scoretext = font.render('Score: '+str(score), True, (255,100,100))    
    screen.blit(scoretext,(p1-200,0+p2/10))
    pygame.display.flip()

# Enemy Creation
class Enemy:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.escape_x = round(uniform(1.25,1.75),2)
        if (100*self.escape_x) % 2 ==0:
            self.escape_x = -self.escape_x
        self.escape_y = round(uniform(1.25,1.75),2)
        if (100*self.escape_y) % 2 ==0:
            self.escape_y = -self.escape_y
        self.timer = 0
        self.hor1 = False
        self.hor2 = False
        self.ver1 = False
        self.ver2 = False
        self.timer = 0
        self.condition = False
    
    def rotate(self):
        rel_x, rel_y = player.pos_x - self.x, player.pos_y - self.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(self.original_image, int(angle))
        self.rect = self.image.get_rect(
            center=(round(self.x + self.w // 2), round(self.y + self.h // 2))
        )
        # self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))

    def draw(self, e_i, randum):
        global game_over, e_list
        if 1<=randum<=2:
            self.image1 = pygame.image.load("enemy1.png")
            self.original_image = pygame.image.load("enemy1.png")
        if 2<randum<=3:
            self.image1 = pygame.image.load("enemy2.png")
            self.original_image = pygame.image.load("enemy2.png")
        if 3<randum<=4:
            self.image1 = pygame.image.load("enemy3.png")
            self.original_image = pygame.image.load("enemy3.png")

        self.rotate()
        switch = False
        screen.blit(self.image, (self.x-camera.offset.x, self.y-camera.offset.y,self.w,self.h))
        speed_x, speed_y = 0,0
        # Collisions at edges
        if self.x<=0:
            self.hor1 = True
            speed_x=0
        if self.x + self.w>= game_size_x:
            self.hor2 = True
            speed_x=0
        if self.y<=0:
            self.ver1 = True
            speed_y=0
        if self.y + self.h>= game_size_y:
            self.ver2=True
            speed_y=0

        if (self.x<=player.pos_x<=self.x+self.w or self.x<=player.pos_x+player.w<=self.x+self.w) and (self.y<=player.pos_y<=self.y+self.h or self.y<=player.pos_y+player.h<=self.y+self.h):
            game_over = True
            
        # Prevent enemies from colliding with each other
        else:
            for element in e_list:
                if e_list.index(element)!=e_i and ((element.x<self.x<element.x+element.w) or (element.x<self.x+self.w<element.x+element.w)) and ((element.y<self.y<element.y+element.h) or (element.y<self.y+self.h<element.y+element.h)):
                    if not self.condition:
                        self.timer = 2
                    switch = True
                    self.condition = True
                    if (-element.escape_x<0 and not self.hor1) or (-element.escape_x>0 and not self.hor2):
                        self.x=randint(20,int(0.7*game_size_x))
                    
                    if (-element.escape_y<0 and not self.ver1) or (-element.escape_y>0 and not self.ver2):
                        self.y=randint(0,int(0.7*game_size_y))

            if not switch:
                if self.condition:
                    self.timer-=1
                if self.timer <=0:
                    self.condition = False
                    d1 = player.pos_x - self.x
                    d2 = player.pos_y - self.y
                    speed_x=uniform(2.7,3.6)
                    if abs(d1) >0:
                        speed_y=(speed_x*abs(d2)/abs(d1))
                        if speed_y>3.5:
                            speed_y = 3.5
                    else:
                        speed_y = 3.5
                    if d1>2:
                        if not self.hor2:
                            self.x+=speed_x
                    elif d1<-2:
                        if not self.hor1:
                            self.x-=speed_x
                    if d2>2:
                        if not self.ver2:
                            self.y+=speed_y
                    elif d2<-2:
                        if not self.ver1:
                            self.y-=speed_y
rd_list = [[],[]]
r_list = list()
entry1 = randint(0,p1)
entry2 = randint(0,p2)
def randomize():
    global rd_list,entry1, entry2
    entry1 = randint(0,game_size_x)
    entry2 = randint(0,game_size_y)
    def check():
        global entry1, entry2
        clear = True
        for item1 in rd_list[0]:
            for item2 in rd_list[1]:
                while (item1-(p1/14)<=entry1<=item1+(p1/14) and item2-(p1/14)<=entry1<=item2+(p1/14)) or (player.pos_x-150<entry1<player.pos_x+player.w+150 and player.pos_y-150<entry2<player.pos_y+player.h+150):
                    entry1 = randint(0,game_size_x)
                    entry2 = randint(0,game_size_y)
                    clear=False
        return clear

    if len(rd_list[0])==0:
        rd_list[0].append(entry1)
        rd_list[1].append(entry2)
    else:
        while check()==False:
            check()

        rd_list[0].append(entry1)
        rd_list[1].append(entry2)


e_list = list()
def spawn_enemy():
    global e_list, r_list
    randomize()
    e_list.append(Enemy(rd_list[0][-1],rd_list[1][-1],(game_size_x/35),(game_size_y/35)))
    r_list.append(randint(1,4))


for f in range(1,5):
    spawn_enemy()

# Function receives index of killed enemy in e_list and kills it
def kill_enemy(dead_indx):
    global rd_list, score
    score+=1
    e_list.pop(dead_indx)
    for sub_list in rd_list:
        sub_list.pop(dead_indx)
    spawn_enemy()
    spawn_enemy()


clouds_list = [[],[]]
for item in range(1,20):
    clouds_list[0].append(randint(100,4700))
    clouds_list[1].append(randint(100,2700))

# Running the game
game_escape = False
while game_escape == False:
    # Running the game
    while not game_over:
        if intro:
            screen.fill((0, 0, 0))
            bkga = pygame.image.load("Intro.png")
            screen.blit(bkga, (160, 40))
            for event in pygame.event.get():
                # Getting the mouse coordinates
                mouse = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    intro = False
            pygame.display.update()
        else:

            screen.fill((110,182,255))
            for item in clouds_list[0]:
                screen.blit(
                    cloud,
                    (
                        item - camera.offset.x,
                        (clouds_list[1][clouds_list[0].index(item)] - camera.offset.y),
                    ),
                )

            
            screen.blit(sunrise, (p1/1.2-camera.offset.x,-1000-camera.offset.y))
            
            for number in range(math.ceil(game_size_x / ca) * -2, math.ceil(game_size_x / ca) * 2):
                screen.blit(
                    corn,
                    (
                        0 + (number * ca) - camera.offset.x,
                        game_size_y - ca - camera.offset.y,
                    ),
                )
            player.x_move = 0
            player.y_move = 0

            for event in pygame.event.get():
                # Getting the mouse coordinates
                mouse = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.MOUSEMOTION:
                    player.rotate()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if player.mode == 1:
                            player_move = True
                        if player.mode == 2:
                            projectiles.append(Projectile())

                    if event.key == pygame.K_1:
                        camera.setmethod(follow)

                    elif event.key == pygame.K_2:
                        camera.setmethod(none)

                    if event.key == pygame.K_TAB:
                        if player.mode == 1:
                            player.mode = 2
                            player_move = False
                            player.original_image = pygame.image.load("pp2.png")
                        elif player.mode == 2:
                            player.mode = 1
                            player.original_image = pygame.image.load("pp1.png")

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        player_move = False

            for projectile in projectiles:
                if projectile.pos_x < game_size_x and projectile.pos_x > 0:
                    projectile.move()

                else:
                    projectiles.pop(projectiles.index(projectile))

            redraw()

            # Draw the game
            pygame.display.update()
            # Frames per second
            clock.tick(30)

    while game_over:
        screen.fill((0,0,0))
        bomb = pygame.image.load("game_over.png")
        font = pygame.font.SysFont('Arial',50)
        scoretext = font.render('Score: '+str(score), True, (255,100,100))    
        screen.blit(scoretext,(p1-400,0+p2/10))
        mtext = font.render('Play Again?', True, (255,100,100))    
        mtext1 = font.render('Press Enter', True, (255,100,100)) 
        screen.blit(mtext,(p1-400,0+p2/1.5))
        screen.blit(mtext1,(p1-400,0+p2/1.3))
        screen.blit(bomb,((p1/2)-bomb.get_width()/2,(p2/2)-bomb.get_height()/2))
        pygame.display.update()
        token = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_escape = True
                    token = 1
                elif event.key == pygame.K_RETURN:
                    score = 0
                    token = 1
                    game_over = False
                    player = Player()
                    camera = Camera(player)
                    # none = none(camera, player)
                    follow = Follow(camera, player)
                    border = Border(camera, player)
                    camera.setmethod(follow)
                    player_move = False
                    projectiles = []

        if token == 0:
            pygame.display.update()
        else:
            break

pygame.quit()
    
