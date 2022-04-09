# Gazelle running through the sabannnah
# 2022.4.3 clear screen
import random
import pyxel                        # Ver1.6.9

SCREEN_WIDTH = 256
SCREEN_HEIGHT = 128
FPS = 30

ASSET_FILENAME = "gazelle.pyxres"
TRANSPARENT_COLOR = 14              # 透明色：ピンク
GROUND_Y = 116                      # 地面のx座標
PLAYER_X = 45                       # Playerのy座標
ENEMYS_NO = 5                      # 障害物の数
global game_state                   # "START", "PLAY" "CLEAR", "GAME OVER"
global score

def sound_set():
    pyxel.sound(0).set("c0rrrrb0rrrr", "n", "4444422222", "n", 3)
    pyxel.sound(1).set("c3 d3", "t", "7", "n", 10)
    pyxel.sound(2).set("d-3 c3 b3 b-3 a3 a-2 g2 g2 g2", "t", "445677654", "n", 10)
    pyxel.sound(3).set("e3rr e3r e3r e3e3e3e3 f3f3r e3e3r f3f3r e3e3e3e3", "t", "2", "n", 12)
    pyxel.sound(4).set("g3rr g3r g3r g3g3g3g3 a3a3r g3g3r a3a3r g3g3g3g3", "t", "2", "n", 12)
    pyxel.music(0).set([3], [4], [], [])
def run_sound():
    pyxel.play(0, 0)
def jump_sound():
    pyxel.play(0, 1)
def stop_sound():
    pyxel.play(0, 2)
def clear_sound():
    pyxel.playm(0)

class Mover:
    def __init__(self, x, y, img, vx, vy):
        self.x = x
        self.y = y
        self.img = img
        self.width = img[3]
        self.height = img[4]
        self.vx = vx
        self.vy = vy

class Background:
    MOUNTAIN_IMG = [0, 0,  32, SCREEN_WIDTH,  40, TRANSPARENT_COLOR]
    CLOUD_IMG =    [0, 0,   0, SCREEN_WIDTH,  32, TRANSPARENT_COLOR]
    ROCK_IMG =     [0, 0,  72, SCREEN_WIDTH,  38, TRANSPARENT_COLOR]
    GROUND_IMG =   [0, 0, 106, SCREEN_WIDTH,  32, TRANSPARENT_COLOR]

    def __init__(self):
        bg0 = Mover(0, 40, self.MOUNTAIN_IMG, 0,   0)
        bg1 = Mover(0, 20, self.CLOUD_IMG,    0.3, 0)
        bg2 = Mover(0, 58, self.ROCK_IMG,     1,   0)
        bg3 = Mover(0, 96, self.GROUND_IMG,   2,   0)
        self.backgrounds = [bg0, bg1, bg2, bg3]

    def update(self):
        # 背景が左に動くようにX座標を減らす
        if game_state == "PLAY":
            for bg in self.backgrounds:
                bg.x -= bg.vx
                if bg.x < -SCREEN_WIDTH:
                    bg.x = 0 
        else: 
            bg = self.backgrounds[1]                # cloud
            bg.x -= bg.vx
            if bg.x < -SCREEN_WIDTH:
                bg.x = 0

    def draw(self): 
        for bg in self.backgrounds:
            pyxel.blt(bg.x, bg.y, *bg.img)
            pyxel.blt(bg.x + SCREEN_WIDTH, bg.y, *bg.img) 

class Player:
    JUMP_IMG = [1, 25, 1, 20, 20, TRANSPARENT_COLOR]
    RUN_IMG =  [1, 50, 2, 19, 19, TRANSPARENT_COLOR]
    STOP_IMG = [1, 99, 0, 19, 24, TRANSPARENT_COLOR]
    POPPERS_IMG0 = [1, 0, 0,  24, 24, TRANSPARENT_COLOR]
    POPPERS_IMG1 = [1, 0, 0, -24, 24, TRANSPARENT_COLOR]

    def __init__(self):
        self.jump_height = 40
        self.down_speed = 1.5
        self.state = "RUN"                              # "RUN", "JUMP", "STOP"
        self.player = Mover(0, 0, self.RUN_IMG, self.down_speed, 0)
        self.x = PLAYER_X
        self.init_y = GROUND_Y - self.player.height - 2
        self.max_y  = self.init_y - self.jump_height
        self.y = self.init_y
        self.bottom = self.y + self.player.height
        self.center = self.x + self.player.width / 2

    def update(self):
        if self.state == "RUN" and pyxel.btn(pyxel.KEY_SPACE):
            self.y = self.max_y
            self.state = "JUMP"
            jump_sound()
        
        if self.state == "JUMP":
            self.y += self.down_speed
            if self.y >= self.init_y:
                self.y = self.init_y
                self.state = "RUN"
            
        if self.state == "RUN" and ((pyxel.frame_count % 10) == 0):
            run_sound()
        
        self.bottom = self.y + self.player.height

    def draw(self):
        if game_state == "GAME OVER":
            pyxel.blt(self.x, self.y, *self.STOP_IMG) 
            return

        if game_state == "START":
            if (pyxel.frame_count // 5 % 2) == 0:
                pyxel.blt(self.x, self.y, *self.JUMP_IMG)
            else:
                pyxel.blt(self.x, self.y-1, *self.JUMP_IMG)
            return

        if game_state == "CLEAR":
            if (pyxel.frame_count // 5 % 2) == 0:
                pyxel.blt(self.x, self.y, *self.JUMP_IMG)
                pyxel.blt(self.x+19, self.y-16, *self.POPPERS_IMG0)
                pyxel.blt(self.x-15, self.y-16, *self.POPPERS_IMG1)
            else:
                pyxel.blt(self.x, self.y-1, *self.JUMP_IMG)
                pyxel.blt(self.x+18, self.y-16, *self.POPPERS_IMG0)
                pyxel.blt(self.x-14, self.y-16, *self.POPPERS_IMG1)
            return

        if (pyxel.frame_count // 5 % 2) == 0 or self.state == "JUMP":
            pyxel.blt(self.x, self.y, *self.JUMP_IMG)
        else:
            pyxel.blt(self.x-1, self.y, *self.RUN_IMG)

class Enemy:
    ENEMY0_IMG = [1,  1, 29, 20, 16, TRANSPARENT_COLOR]     # camel
    ENEMY1_IMG = [1, 26, 28, 16, 17, TRANSPARENT_COLOR]     # leafy tree
    ENEMY2_IMG = [1, 53, 30, 13, 17, TRANSPARENT_COLOR]     # dead tree
    ENEMY3_IMG = [1, 80, 35,  8, 11, TRANSPARENT_COLOR]     # small dead tree
    ENEMY4_IMG = [1, 96, 39,  9,  8, TRANSPARENT_COLOR]     # grass
    ENEMY5_IMG = [1,111, 39,  9,  8, TRANSPARENT_COLOR]     # mushuroom
    enemy_images = [ENEMY0_IMG, ENEMY1_IMG, ENEMY2_IMG, ENEMY3_IMG, ENEMY4_IMG, ENEMY5_IMG]

    def __init__(self):
        self.interval = [50, 90]
        self.speed = 2
        self.width = 20
        self.start_x = SCREEN_WIDTH + self.width
        self.collision_dist_x = 2                           # 衝突判定の距離:大きい程厳しい
        self.collision_dist_y = 2                           # 衝突判定の距離:小さい程厳しい
        self.image_no_list = [0,1,2,2,3,3,4,4,5,5]
        self.initialize()

    def initialize(self):
        self.enemys = []
        x = self.start_x
        for _ in range(ENEMYS_NO):
            img_no = random.choice(self.image_no_list)
            self.enemy = Mover(0, 0, self.enemy_images[img_no], self.speed, 0)
            self.enemy.x = x
            x += random.randint(*self.interval)
            self.enemy.y =GROUND_Y - self.enemy.height
            self.enemys.append(self.enemy)

    def update(self, x, y):                 # x:Playerのcenterのx座標,　y:Playerのbottomのy座標
        global game_state, score

        # 左に動くようにX座標を減らす
        for enemy in self.enemys:
            enemy.x -= enemy.vx
        # 衝突判定
        for enemy in self.enemys:
            if ( x + self.collision_dist_x > enemy.x and \
                 x - self.collision_dist_x < enemy.x + enemy.width) and \
                 y > enemy.y + self.collision_dist_y:
                stop_sound()
                game_state = "GAME OVER"
                return

        score = 0
        for enemy in self.enemys:
            if enemy.x  < PLAYER_X - self.width:
                score += 1
        if score == ENEMYS_NO and self.enemys[ENEMYS_NO-1].x < -self.width:
            clear_sound()
            game_state = "CLEAR"

    def draw(self):
        for enemy in self.enemys:
            pyxel.blt(enemy.x, enemy.y, *enemy.img)
    
    def init_x(self):
        x = self.start_x
        for enemy in self.enemys:
            enemy.x = x
            x += random.randint(*self.interval)

class Text:
    def __init__(self):
        pass
    def update(self):
        pass
    def draw(self):
        global game_state, score
        pyxel.rect(219, 9, 35, 7, 7)
        pyxel.text(220, 10, "SCORE:" + str(score), 5)
        pyxel.text(2, 2, "Pyxel 1.6.9", 5)
        if game_state == "START":
            pyxel.text(110, 20, "S:START", 5)
        if game_state == "PLAY" and score == 0:
            pyxel.text(110, 20, "SPACE:JUMP", 5)    
        if game_state == "CLEAR":
            pyxel.text(110, 10, "GAME CLEAR", 5)
            pyxel.text(114, 20, "S:START", 5)
        if game_state == "GAME OVER":
            pyxel.text(110, 10, "GAME OVER", 5)
            pyxel.text(114, 20, "S:START", 5)

class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, fps=FPS)
        pyxel.load(ASSET_FILENAME)
        sound_set()

        global game_state, score
        game_state = "START"
        score = 0
        self.text = Text()
        self.background = Background()
        self.player = Player()
        self.enemy = Enemy()
        pyxel.run(self.update, self.draw)

    def update(self):
        global game_state

        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()

        if game_state == "START" and pyxel.btn(pyxel.KEY_S):
            game_state = "PLAY"

        if game_state == "GAME OVER" and pyxel.btn(pyxel.KEY_S):
            self.enemy.initialize()
            game_state = "PLAY"
 
        if game_state == "CLEAR" and pyxel.btn(pyxel.KEY_S):
            self.enemy.initialize()
            game_state ="PLAY"

        self.background.update()
        if game_state == "PLAY":
            self.player.update()
            self.enemy.update(self.player.center, self.player.bottom)

    def draw(self):
        pyxel.cls(14)
        self.background.draw()
        self.enemy.draw()
        self.player.draw()
        self.text.draw()

App()