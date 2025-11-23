import pygame
import sys
import math
import random
pygame.init()


SIZE = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
screen.fill((0, 0, 0))
LEFT = RIGHT = DOWN = UP = CTRL = False
K_LEFT, K_RIGHT, K_DOWN, K_UP = False, False, False, False
zs = []
bs = []
IMAGES = {
    "01": "pygam/sprites/PNG/Tiles/tile_01.png",
    "02": "pygam/sprites/PNG/Tiles/tile_02.png",
    "03": "pygam/sprites/PNG/Tiles/tile_03.png",
    "17": "pygam/sprites/PNG/Tiles/tile_17.png",
    "42": "pygam/sprites/PNG/Tiles/tile_42.png",
    "116": "pygam/sprites/PNG/Tiles/tile_116.png",
    "117": "pygam/sprites/PNG/Tiles/tile_117.png",
    "143": "pygam/sprites/PNG/Tiles/tile_143.png",
    "144": "pygam/sprites/PNG/Tiles/tile_144.png",
    "163": "pygam/sprites/PNG/Tiles/tile_163.png",
    "164": "pygam/sprites/PNG/Tiles/tile_164.png",
    "167": "pygam/sprites/PNG/Tiles/tile_167.png",
    "168": "pygam/sprites/PNG/Tiles/tile_168.png",
    "190": "pygam/sprites/PNG/Tiles/tile_190.png",
    "191": "pygam/sprites/PNG/Tiles/tile_191.png",
    "194": "pygam/sprites/PNG/Tiles/tile_194.png",
    "195": "pygam/sprites/PNG/Tiles/tile_195.png",
}
MAP = []
floar = ["17", "42"]
walls = []
ts1 = []
ts2 = []
ts3 = []
boss_spawn = True
boss_hp = 21
its = []
use_baf_in_first_room = False
new_baf_in_bafroom = True
new_baf_with_zomb = True
baf_in_3_room = False
rooms = [1, 3, 4]
random.shuffle(rooms)
boss_room = rooms[0]
zomb_room = rooms[1]
spawn_room = 2
baf_room = rooms[2]
num_room = spawn_room
choice = ["spectral", "diog_shot", "speed_shot"]

def create_map(a, b, c, d, floar_ind):
    for i in range(19):
        for j in range(25):
            if j == 0:
                MAP.append([])
            if i == 0:
                if c:
                    if j == 11 or j == 12 or j == 13:
                        MAP[i].append("03")
                    elif j == 0:
                        MAP[i].append("163")
                    elif j == 24:
                        MAP[i].append("164")
                    else:
                        MAP[i].append("195")
                else:
                    if j == 0:
                        MAP[i].append("163")
                    elif j == 24:
                        MAP[i].append("164")
                    else:
                        MAP[i].append("195")
            elif i == 18:
                if d:
                    if j == 11 or j == 12 or j == 13:
                        MAP[i].append("03")
                    elif j == 0:
                        MAP[i].append("163")
                    elif j == 24:
                        MAP[i].append("164")
                    else:
                        MAP[i].append("194")
                else:
                    if j == 0:
                        MAP[i].append("190")
                    elif j == 24:
                        MAP[i].append("191")
                    else:
                        MAP[i].append("194")
            else:
                if j == 0:
                    if a:
                        if i == 8:
                            MAP[i].append("01")
                        elif i == 9:
                            MAP[i].append("01")
                        elif i == 10:
                            MAP[i].append("01")
                        else:
                            MAP[i].append("168")
                    else:
                        MAP[i].append("168")
                elif j == 24:
                    if b:
                        if i == 8:
                            MAP[i].append("02")
                        elif i == 9:
                            MAP[i].append("02")
                        elif i == 10:
                            MAP[i].append("02")
                        else:
                            MAP[i].append("167")
                    else:
                        MAP[i].append("167")   
                else:
                    MAP[i].append(f"{floar[floar_ind]}")
# a - left, b - right, c - top, d - bot

if spawn_room == 2:
    create_map(True, True, False, True, 1)
elif spawn_room == 3:
    create_map(False, True, False, False, 0)
elif spawn_room == 1:
    create_map(True, False, False, False, 0)
elif spawn_room == 4:
    create_map(False, False, True, False, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, hp):
        pygame.sprite.Sprite.__init__(self)
        self.x = x        
        self.y = y       
        self.x_speed = 0  
        self.y_speed = 0 
        self.image = pygame.image.load("pygam/sprites/PNG/Hitman 1/hitman1_stand.png")
        self.image = pygame.transform.rotate(self.image, 270)
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y
        self.a = 90 
        self.r = 0
        self.speed_shot = 80
        self.time_shied = 0
        self.spectral_shot = False
        self.diog_shot = False
        self.hp = hp
        self.full_hp = hp
        self.dead = False
    

    def reset(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, left, right, down, up, CTRL, K_LEFT, K_RIGHT, K_DOWN, K_UP, bs, zs, walls, ts1, ts2, ts3):
        global num_room, use_baf_in_first_room

        self.r += 1
        if left:
            self.x_speed = -3
            if self.r > 20:
                self.image = pygame.image.load("pygam/sprites/PNG/Hitman 1/hitman1_hold.png")
                self.image = pygame.transform.rotate(self.image, 180)
                self.a = 180

        elif right:
            self.x_speed = 3
            if self.r > 20:
                self.image = pygame.image.load("pygam/sprites/PNG/Hitman 1/hitman1_hold.png")
                self.image = pygame.transform.rotate(self.image, 0)
                self.a = 0

        if not (left or right):
            self.x_speed = 0 
        if CTRL:
            self.x_speed *= 1.5
        self.rect.x += self.x_speed

        if down:
            self.y_speed = 3
            if self.r > 20:
                self.image = pygame.image.load("pygam/sprites/PNG/Hitman 1/hitman1_hold.png")
                self.image = pygame.transform.rotate(self.image, 270)
                self.a = 270

        elif up:
            self.y_speed = -3
            if self.r > 20:
                self.image = pygame.image.load("pygam/sprites/PNG/Hitman 1/hitman1_hold.png")
                self.image = pygame.transform.rotate(self.image, 90)
                self.a = 90

        if not (down or up):
            self.y_speed = 0 
        if CTRL:
            self.y_speed *= 1.5
        self.rect.y += self.y_speed

        if not self.diog_shot:
            if K_LEFT and self.r >= self.speed_shot:
                self.image = pygame.image.load("pygam/sprites/PNG/Hitman 1/hitman1_gun.png")
                self.image = pygame.transform.rotate(self.image, 180)
                bs.append(Bullet(self.rect.x, self.rect.y, 2, 10))
                self.r = 0

            elif K_RIGHT and self.r >= self.speed_shot:
                self.image = pygame.image.load("pygam/sprites/PNG/Hitman 1/hitman1_gun.png")
                self.image = pygame.transform.rotate(self.image, 0)
                bs.append(Bullet(self.rect.x, self.rect.y, 1, 10))
                self.r = 0

            elif K_DOWN and self.r >= self.speed_shot:
                self.image = pygame.image.load("pygam/sprites/PNG/Hitman 1/hitman1_gun.png")
                self.image = pygame.transform.rotate(self.image, 270)
                bs.append(Bullet(self.rect.x, self.rect.y, 3, 10))
                self.r = 0

            elif K_UP and self.r >= self.speed_shot:
                self.image = pygame.image.load("pygam/sprites/PNG/Hitman 1/hitman1_gun.png")
                self.image = pygame.transform.rotate(self.image, 90)
                bs.append(Bullet(self.rect.x, self.rect.y, 4, 10))
                self.r = 0
        else:
            if K_LEFT and self.r >= self.speed_shot:
                self.image = pygame.image.load("pygam/sprites/PNG/Hitman 1/hitman1_gun.png")
                self.image = pygame.transform.rotate(self.image, 180)
                bs.append(Bullet(self.rect.x, self.rect.y, 2, 10))
                bs.append(Bullet(self.rect.x, self.rect.y, 5, 10))
                bs.append(Bullet(self.rect.x, self.rect.y, 6, 10))
                self.r = 0

            elif K_RIGHT and self.r >= self.speed_shot:
                self.image = pygame.image.load("pygam/sprites/PNG/Hitman 1/hitman1_gun.png")
                self.image = pygame.transform.rotate(self.image, 0)
                bs.append(Bullet(self.rect.x, self.rect.y, 1, 10))
                bs.append(Bullet(self.rect.x, self.rect.y, 7, 10))
                bs.append(Bullet(self.rect.x, self.rect.y, 8, 10))
                self.r = 0

            elif K_DOWN and self.r >= self.speed_shot:
                self.image = pygame.image.load("pygam/sprites/PNG/Hitman 1/hitman1_gun.png")
                self.image = pygame.transform.rotate(self.image, 270)
                bs.append(Bullet(self.rect.x, self.rect.y, 6, 10))
                bs.append(Bullet(self.rect.x, self.rect.y, 3, 10))
                bs.append(Bullet(self.rect.x, self.rect.y, 7, 10))
                self.r = 0

            elif K_UP and self.r >= self.speed_shot:
                self.image = pygame.image.load("pygam/sprites/PNG/Hitman 1/hitman1_gun.png")
                self.image = pygame.transform.rotate(self.image, 90)
                bs.append(Bullet(self.rect.x, self.rect.y, 5, 10))
                bs.append(Bullet(self.rect.x, self.rect.y, 8, 10))
                bs.append(Bullet(self.rect.x, self.rect.y, 4, 10))
                self.r = 0

        for b in bs:
            if b.name == "zombie" and pygame.sprite.collide_rect(self, b) and self.time_shied >= 15:
                self.time_shied = 0
                if num_room == spawn_room:
                    self.rect.x, self.rect.y = 70, 70
                elif num_room == zomb_room:
                    self.rect.x, self.rect.y = 700, 300
                else:
                    boss.hp = boss.full_hp
                    self.rect.x, self.rect.y = WIDTH / 2, HEIGHT / 2 + 100
                print("ранен")
                self.hp -= 1
        
        for zom in zs:
            if pygame.sprite.collide_rect(self, zom) and self.time_shied >= 15:
                self.time_shied = 0
                if num_room == spawn_room:
                    self.rect.x, self.rect.y = 70, 70
                elif num_room == zomb_room:
                    self.rect.x, self.rect.y = 700, 300
                else:
                    self.rect.x, self.rect.y = WIDTH / 2, HEIGHT / 2 + 100
                print("ранен")
                self.hp -= 1
        if num_room == boss_room:
            if pygame.sprite.collide_rect(self, boss) and boss.hp != 0:
                self.hp -= 1
                print("ранен")
                self.rect.x, self.rect.y = WIDTH / 2, HEIGHT / 2 + 100
                boss.hp = boss.full_hp   
        for wall in walls:
            if pygame.sprite.collide_rect(self, wall):
                if self.x_speed < 0:
                    self.rect.left = wall.rect.right
                elif self.x_speed > 0:
                    self.rect.right = wall.rect.left
                if self.y_speed > 0:
                    self.rect.bottom = wall.rect.top
                elif self.y_speed < 0:
                    self.rect.top = wall.rect.bottom

        for t in ts1:
            if pygame.sprite.collide_rect(self, t):
                if num_room == boss_room:
                    if boss.hp <= 0 or boss.lock == False:
                        if num_room == 2:
                            return 1
                        else:
                            return 2
                    elif boss.lock:
                        print("не уходи далеко")
                elif len(zs) == 0:
                    if num_room == 2:
                        return 1
                    else:
                        return 2
                else:
                    print("не уходи далеко")

        for t in ts2:
            if pygame.sprite.collide_rect(self, t):
                if num_room == boss_room:
                    if boss.hp <= 0 or boss.lock == False:
                        if num_room == 2:
                            return 3
                        else:
                            return 2
                    elif boss.lock:
                        print("не уходи далеко")
                elif len(zs) == 0:
                    if num_room == 2:
                        return 3
                    else:
                        return 2
                else:
                    print("не уходи далеко")

        for t in ts3:
            if pygame.sprite.collide_rect(self, t):
                if num_room == boss_room:
                    if boss.hp <= 0 or boss.lock == False:
                        if num_room == 2:
                            return 4
                        else:
                            return 2
                    elif boss.lock:
                        print("не уходи далеко")
                elif len(zs) == 0:
                    if num_room == 2:
                        return 4
                    else:
                        return 2
                else:
                    print("не уходи далеко")
        if self.hp == 0:
            print("dead")
            self.dead = True
            self.hp = self.full_hp
            self.speed_shot = 80
            self.spectral_shot = False
            self.diog_shot = False
            use_baf_in_first_room = False
            return spawn_room
        self.time_shied += 1


    def __repr__(self):
        return f"{self.x}, {self.y}"


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, n, speed, name="hitman"):
        pygame.sprite.Sprite.__init__(self)
        self.x = x        
        self.y = y       
        self.x_speed = 0  
        self.y_speed = 0 
        self.image = pygame.surface.Surface((10, 10))
        if name == "hitman":
            self.image.fill((200, 200, 200))
        else:
            self.image.fill((200, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y
        self.n = n
        self.speed = speed
        self.name = name

    def reset(self, screen):
        screen.blit(self.image, self.rect)
    
    def update(self):
        if self.n == 1:
            self.rect.x += self.speed
        elif self.n == 2:
            self.rect.x -= self.speed
        elif self.n == 3:
            self.rect.y += self.speed
        elif self.n == 4:
            self.rect.y -= self.speed
        elif self.n == 5:
            self.rect.x -= self.speed
            self.rect.y -= self.speed
        elif self.n == 6:
            self.rect.x -= self.speed
            self.rect.y += self.speed
        elif self.n == 7:
            self.rect.x += self.speed
            self.rect.y += self.speed
        elif self.n == 8:
            self.rect.x += self.speed
            self.rect.y -= self.speed
    
    def __del__(self):
        del self


class Zombie(pygame.sprite.Sprite):
    def __init__(self, path, x, y, hp):
        pygame.sprite.Sprite.__init__(self)
        self.path = path
        self.x = x        
        self.y = y       
        self.x_speed = 0  
        self.y_speed = 0 
        self.image = pygame.image.load(f"{self.path[0]}")
        self.image = pygame.transform.rotate(self.image, 90)
        self.image = pygame.transform.scale(self.image, (20, 32))
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y
        self.a = 90
        self.way = (x, y)
        self.speed = 1.5
        self.time = 0
        self.time_shied = 0
        self.hp = hp
        self.full_hp = hp
    

    def reset(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, bs):
        self.time += 1
        if self.rect.x > self.way[0]:
            self.rect.x -= self.speed
        if self.rect.x < self.way[0]:
            self.rect.x += self.speed
        if self.rect.y > self.way[1]:
            self.rect.y -= self.speed
        if self.rect.y < self.way[1]:
            self.rect.y += self.speed
        if self.rect.x == self.way[0] and self.rect.y == self.way[1]:
            a = random.randint(1, 2)
            if a == 1:
                self.way = (random.randint(50, 750), self.rect.y)
            else:
                self.way = (self.rect.x, random.randint(75, 525))
            if a == 1:
                if self.way[0] > self.rect.x:
                    self.image = pygame.image.load(f"{self.path[1]}")
                    self.image = pygame.transform.rotate(self.image, 0)
                else:
                    self.image = pygame.image.load(f"{self.path[2]}")
                    self.image = pygame.transform.rotate(self.image, 0)     
            if a == 2:
                if self.way[1] > self.rect.y:
                    self.image = pygame.image.load(f"{self.path[3]}")
                    self.image = pygame.transform.rotate(self.image, 0)
                else:
                    self.image = pygame.image.load(f"{self.path[4]}")
                    self.image = pygame.transform.rotate(self.image, 0)
            if "zombie" in self.path[0]:
                self.image = pygame.transform.scale(self.image, (30, 44))
            if "skeleton" in self.path[0] and not "skeleton_runner" in self.path[0]:
                if not (self.way[1] > self.rect.y):
                    self.image = pygame.transform.scale(self.image, (30, 44))
                else:
                    self.image = pygame.transform.scale(self.image, (44, 44))
            if "skeleton_runner" in self.path[0]:
                if self.way[1] != self.rect.y:
                    self.image = pygame.transform.scale(self.image, (44, 44))
                else:
                    self.image = pygame.transform.scale(self.image, (30, 44))


        if self.time % 180 == 0 and "zombie" in self.path[0]:
            for i in range(1, 5):
                bs.append(Bullet(self.rect.x, self.rect.y, i, 5, "zombie"))
        if self.time % 180 == 0 and "skeleton" in self.path[0] and not ("skeleton_runner" in self.path[0]):
            for i in range(1, 9):
                bs.append(Bullet(self.rect.x, self.rect.y, i, 5, "zombie"))
        if "skeleton_runner" in self.path[0] and self.time % 180 == 0:
            speed = 5
            if self.way[0] > self.rect.x:
                bs.append(Bullet(self.rect.x, self.rect.y, 1, speed, "zombie"))
                bs.append(Bullet(self.rect.x, self.rect.y, 7, speed, "zombie"))
                bs.append(Bullet(self.rect.x, self.rect.y, 8, speed, "zombie"))
            elif self.way[0] < self.rect.x:
                bs.append(Bullet(self.rect.x, self.rect.y, 2, speed, "zombie"))
                bs.append(Bullet(self.rect.x, self.rect.y, 5, speed, "zombie"))
                bs.append(Bullet(self.rect.x, self.rect.y, 6, speed, "zombie"))
            elif self.way[1] > self.rect.y:
                bs.append(Bullet(self.rect.x, self.rect.y, 7, speed, "zombie"))
                bs.append(Bullet(self.rect.x, self.rect.y, 6, speed, "zombie"))
                bs.append(Bullet(self.rect.x, self.rect.y, 3, speed, "zombie"))
            else:
                bs.append(Bullet(self.rect.x, self.rect.y, 8, speed, "zombie"))
                bs.append(Bullet(self.rect.x, self.rect.y, 5, speed, "zombie"))
                bs.append(Bullet(self.rect.x, self.rect.y, 4, speed, "zombie"))
        for b in bs:
            if pygame.sprite.collide_rect(self, b) and b.name == "hitman" and self.time_shied >= 15:
                self.time_shied = 0
                self.hp -= 1
                if not p.spectral_shot:
                    bs.remove(b)
                print("сущность ранена")
        self.time_shied += 1

    def __del__(self):
        del self

    def __str__(self):
        return f"({self.x}, {self.y}, {self.path[0]})"
    
    def __repr__(self):
        return f"{self.x}, {self.y}"


class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, hp):
        pygame.sprite.Sprite.__init__(self)
        self.x = x        
        self.y = y       
        self.x_speed = 0  
        self.y_speed = 0 
        self.image = pygame.image.load("pygam/sprites/PNG/Zombie 1/zoimbie1_stand.png")
        self.image = pygame.transform.rotate(self.image, 270)
        self.image = pygame.transform.scale(self.image, (self.image.get_size()[0], self.image.get_size()[1]))
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y
        self.hp = hp
        self.time_shied = 0
        self.time = 0
        self.way = [(self.rect.x - 200, self.rect.y), (self.rect.x + 200, self.rect.y)]
        self.num_way = 0
        self.speed = 1
        self.full_hp = hp
        self.lock = False
        if self.hp % 3 != 0:
            print("""
            000000000000000000000000000000000000000000000000000000000000000000000
            число жизней босса строго должно нацело делиться на три, измените код!
            000000000000000000000000000000000000000000000000000000000000000000000
            """)
            pygame.quit()
            sys.exit()
    
    def reset(self, screen):
        screen.blit(self.image, self.rect)
    
    def update(self, bs):
        self.time_shied += 1
        for b in bs:
            if pygame.sprite.collide_rect(self, b):
                self.lock = True
                if b.name == "hitman" and self.time_shied >= 15:
                    if not p.spectral_shot:
                        bs.remove(b)
                    self.time_shied = 0
                    self.hp -= 1
                    print("босс ранен")
                    if self.hp == 0:
                        for i in range(1, 9):
                            bs.append(Bullet(self.rect.x, self.rect.y, i, 10, "zombie"))
                    if self.hp == self.full_hp / 3 * 2:
                        self.time = 0
                        print("босс злится")
                    if self.hp == self.full_hp / 3:
                        self.time = 0
                        print("босс злится")

        if self.hp < self.full_hp:
            self.image = pygame.image.load("pygam/sprites/PNG/Zombie 1/zoimbie1_gun.png")
            self.image = pygame.transform.rotate(self.image, 270)
            if self.way[self.num_way % 2] == (self.rect.x, self.rect.y):
                self.num_way += 1
            if self.num_way % 2 == 0:
                self.rect.x -= self.speed
            else:
                self.rect.x += self.speed
            if self.hp <= self.full_hp / 3:
                if self.time % 80 == 0:
                    bs.append(Bullet(self.rect.x, self.rect.y, 3, 3, "zombie"))
                    bs.append(Bullet(self.rect.x, self.rect.y, 6, 3, "zombie"))
                    bs.append(Bullet(self.rect.x, self.rect.y, 7, 3, "zombie"))
            else:
                if self.time % 90 == 0:
                    bs.append(Bullet(self.rect.x, self.rect.y, 3, 3, "zombie"))
                    bs.append(Bullet(self.rect.x, self.rect.y, 6, 3, "zombie"))
                    bs.append(Bullet(self.rect.x, self.rect.y, 7, 3, "zombie"))
            if self.time % 180 == 1 and self.hp <= 20:
                self.temp = (self.rect.x, self.rect.y + 200)
            if self.hp <= self.full_hp / 3 * 2 and self.time >= 1:
                pygame.draw.rect(screen, (20, 20, 20), (self.temp[0] - 5, self.temp[1] - 5, 10, 10))
            if self.time % 150 == 0:
                bs.append(Bullet(WIDTH / 2 - 300, self.rect.y, 1, 5, "zombie"))
                bs.append(Bullet(WIDTH / 2 + 300, self.rect.y, 2, 5, "zombie"))
                bs.append(Bullet(self.rect.x, self.rect.y, 4, 5, "zombie"))
            self.time += 1
            if self.hp <= self.full_hp / 3 * 2:
                if self.time % 180 == 0 and self.time != 0:
                    for i in range(1, 9):
                        bs.append(Bullet(self.temp[0], self.temp[1], i, 2, "zombie"))
            if self.hp <= self.full_hp / 3:
                if self.time % 70 == 0:
                    bs.append(Bullet(p.rect.x, 0, 3, 5, "zombie"))
        else:
            self.image = pygame.image.load("pygam/sprites/PNG/Zombie 1/zoimbie1_stand.png")
            self.image = pygame.transform.rotate(self.image, 270)


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, path):
        self.path = path
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect(center=(x, y))


class Items(pygame.sprite.Sprite):
    def __init__(self, x, y, ybaf=""):
        global choice
        pygame.sprite.Sprite.__init__(self)
        self.x = x        
        self.y = y
        if ybaf == "":
            self.baf = random.choice(choice)
            choice.remove(self.baf)
        else:
            self.baf = ybaf
        if self.baf == "spectral":
            self.image = pygame.image.load("pygam/sprites/PNG/Slab/runeGrey_slab_001.png")
        elif self.baf == "diog_shot":
            self.image = pygame.image.load("pygam/sprites/PNG/Slab/runeGrey_slab_002.png")
        elif self.baf == "speed_shot":
            self.image = pygame.image.load("pygam/sprites/PNG/Slab/runeGrey_slab_003.png")
        elif self.baf == "heal":
            self.image = pygame.image.load("pygam/sprites/PNG/Slab/runeGrey_slab_004.png")
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y
        print(self.baf)
    
    def reset(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, p):
        global use_baf_in_first_room, baf_in_3_room
        if pygame.sprite.collide_rect(self, p):
            if num_room == baf_room:
                use_baf_in_first_room = True
            elif num_room == zomb_room:
                baf_in_3_room = False
            its.remove(self)
            if self.baf == "spectral":
                p.spectral_shot = True
            elif self.baf == "diog_shot":
                p.diog_shot = True
            elif self.baf == "speed_shot":
                p.speed_shot = 40
            elif self.baf == "heal":
                p.hp = p.full_hp
    
    def __del__(self):
        del self


X_START = 16
Y_START = 16
TILES = pygame.sprite.Group()

for i in MAP:
    for j in i:
        tile = Tile(X_START, Y_START, IMAGES[j])
        TILES.add(tile)
        X_START += 32
    X_START = 16
    Y_START += 32

for i in TILES:
    if "17" in i.path or "42" in i.path :
        continue
    elif "03" in i.path:
        ts3.append(i)
    elif "02" in i.path:
        ts1.append(i)
    elif "01" in i.path:
        ts2.append(i)
    else:
        walls.append(i)


p = Player(WIDTH / 2, 70, 2)
z = Zombie(["pygam/sprites/PNG/Zombie 1/zombie.png", "pygam/sprites/PNG/Zombie 1/zombie_right.png", "pygam/sprites/PNG/Zombie 1/zombie_left.png",
"pygam/sprites/PNG/Zombie 1/zombie.png", "pygam/sprites/PNG/Zombie 1/zombie_up.png"], WIDTH / 2,  HEIGHT / 2, 2)
s = Zombie(["pygam/sprites/PNG/Zombie 1/skeleton.png", "pygam/sprites/PNG/Zombie 1/skeleton_right.png", "pygam/sprites/PNG/Zombie 1/skeleton_left.png",
"pygam/sprites/PNG/Zombie 1/skeleton.png", "pygam/sprites/PNG/Zombie 1/skeleton_up.png"], (WIDTH / 4) * 3,  (HEIGHT / 4) * 3, 2)
s1 = Zombie(["pygam/sprites/PNG/Zombie 1/skeleton_runner.png", "pygam/sprites/PNG/Zombie 1/skeleton_runner_right.png", "pygam/sprites/PNG/Zombie 1/skeleton_runner_left.png",
"pygam/sprites/PNG/Zombie 1/skeleton_runner.png", "pygam/sprites/PNG/Zombie 1/skeleton_runner_up.png"], (WIDTH / 4) * 3,  (HEIGHT / 4), 2)

def del_zs_and_bs():
    t = 0
    for zom in zs:
        if zom.hp == 0:
            zs.pop(t)
        t += 1

    t = 0
    for bul in bs:
        if abs(bul.rect.x) > 1000 or abs(bul.rect.y) > 1000:
            bs.pop(t)
        t += 1

def heal_mobs():
    z.hp = z.full_hp
    s.hp = s.full_hp
    s1.hp = s1.full_hp
    if num_room == boss_room:
        boss.rect.x, boss.rect.y = WIDTH / 2, HEIGHT / 2 - 150
        boss.lock = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            LEFT = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            RIGHT = True

        elif event.type == pygame.KEYUP and event.key == pygame.K_a:
            LEFT = False
        elif event.type == pygame.KEYUP and event.key == pygame.K_d:
            RIGHT = False

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            DOWN = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            UP = True

        elif event.type == pygame.KEYUP and event.key == pygame.K_s:
            DOWN = False
        elif event.type == pygame.KEYUP and event.key == pygame.K_w:
            UP = False

        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            K_LEFT = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            K_RIGHT = True

        elif event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
            K_LEFT = False
        elif event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
            K_RIGHT = False

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            K_DOWN = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            K_UP = True

        elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
            K_DOWN = False
        elif event.type == pygame.KEYUP and event.key == pygame.K_UP:
            K_UP = False


        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LCTRL:
            CTRL = True
        elif event.type == pygame.KEYUP and event.key == pygame.K_LCTRL:
            CTRL = False


        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    del_zs_and_bs()
    screen.fill((0, 0, 0))
    TILES.draw(screen)
    for zom in zs:
        zom.update(bs)
        zom.reset(screen)
    for b in bs:
        b.update()
        b.reset(screen)
    for it in its:
        it.reset(screen)
        it.update(p)
    p.reset(screen)
    temp = p.update(LEFT, RIGHT, DOWN, UP, CTRL, K_LEFT, K_RIGHT, K_DOWN, K_UP, bs, zs, walls, ts1, ts2, ts3)
    if len(zs) == 0 and new_baf_with_zomb and num_room == zomb_room:
        new_baf_with_zomb = False
        baf_in_3_room = True
        ran = random.randint(1, 5)
        if ran == 1:
            item2 = Items(WIDTH / 2, HEIGHT / 2)
        else:
            item2 = Items(WIDTH / 2, HEIGHT / 2, "heal")
        its.append(item2)
    if temp:
        its.clear()
        zs.clear()
        bs.clear()
        TILES = pygame.sprite.Group()
        MAP = []
        walls = []
        ts1 = []

        if p.dead:
            heal_mobs()

        if temp == 4:
            p.rect.y = 33
        elif num_room == 4:
            p.rect.y = 500
        else:
            if temp > num_room:
                p.rect.x = 710
            else:
                p.rect.x = 33

        if temp == boss_room:
            if boss_spawn:
                boss_spawn = False
                boss = Boss(WIDTH / 2, HEIGHT / 2 - 75, boss_hp)
            if temp == 2:
                create_map(True, True, False, True, 1)
            elif temp == 3:
                create_map(False, True, False, False, 0)
            elif temp == 1:
                create_map(True, False, False, False, 0)
            elif temp == 4:
                create_map(False, False, True, False, 0)

        elif temp == spawn_room:
            if temp == 2:
                create_map(True, True, False, True, 1)
            elif temp == 3:
                create_map(False, True, False, False, 0)
            elif temp == 1:
                create_map(True, False, False, False, 0)
            elif temp == 4:
                create_map(False, False, True, False, 0)

        elif temp == zomb_room:
            if temp == 2:
                create_map(True, True, False, True, 1)
            elif temp == 3:
                create_map(False, True, False, False, 0)
            elif temp == 1:
                create_map(True, False, False, False, 0)
            elif temp == 4:
                create_map(False, False, True, False, 0)
            if baf_in_3_room:
                its.append(item2)
            else:
                zs.append(z)
                zs.append(s)
                zs.append(s1)

        elif temp == baf_room:
            if new_baf_in_bafroom:
                new_baf_in_bafroom = False
                item = Items(WIDTH / 2, HEIGHT / 2)
            if temp == 2:
                create_map(True, True, False, True, 1)
            elif temp == 3:
                create_map(False, True, False, False, 0)
            elif temp == 1:
                create_map(True, False, False, False, 0)
            elif temp == 4:
                create_map(False, False, True, False, 0)
            if not use_baf_in_first_room:
                its.append(item)

        num_room = temp
        X_START = 16
        Y_START = 16
        for i in MAP:
            for j in i:
                tile = Tile(X_START, Y_START, IMAGES[j])
                TILES.add(tile)
                X_START += 32
            X_START = 16
            Y_START += 32
        for i in TILES:
            if "17" in i.path or "42" in i.path:
                continue
            elif "03" in i.path:
                ts3.append(i)
            elif "02" in i.path:
                ts1.append(i)
            elif "01" in i.path:
                ts2.append(i)
            else:
                walls.append(i)
        if p.dead:
            p.rect.x, p.rect.y = WIDTH / 2, 70
            p.dead = False
    if num_room == boss_room and boss.hp > 0:
        boss.reset(screen)
        boss.update(bs)
        if boss.lock and boss.hp != boss.full_hp:
            pygame.draw.rect(screen, (20, 20, 20), (WIDTH / 2 - 100, 2, 208, 42))
            pygame.draw.rect(screen, (150, 0, 0), (WIDTH / 2 - 96, 6, boss.hp * (200 / boss.full_hp), 34))
    pygame.display.update()
    clock.tick(60)
