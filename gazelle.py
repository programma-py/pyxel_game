# 220306_13_3 砂漠にガゼル
# ガゼルの滞空時間設定、音も出す
# Moverクラス作成、画像のサイズも設定、敵５０体、衝突判定
# サウンドをデータで持つ 3.25
# S キーでスタート、再スタート
# スコアを付ける
import random
import pyxel

SCREEN_WIDTH = 256
SCREEN_HEIGHT = 128
FPS = 30

ASSET_FILENAME = "gazelle.pyxres"
TRANSPARENT_COLOR = 14              # 透明色：ピンク
GROUND_Y = 116
PLAYER_X = 40
ENEMY_MAX = 50
COLLISION_DIST = 6
global game_state                   # "START", "PLAY" "CLEAR", "GAME OVER
global score

def sound_set():
    pyxel.sound(0).set("c0rrrrb0rrrr", "n", "4444422222", "n", 3)
    pyxel.sound(1).set("c3 d3", "t", "7", "n", 10)
    pyxel.sound(2).set("d-3 c3 b3 b-3 a3 a-2 g2 g2 g2", "t", "445677654", "n", 10)
    pyxel.sound(3).set("c3", "t", "2", "f", 8)
    pyxel.sound(4).set("e3r e3e3e3e3r f3e3f3 e3e3e3e3", "t", "2", "n", 20)
    pyxel.sound(5).set("g3r g3g3g3g3r a3g3a3 g3g3g3g3", "t", "2", "n", 20)
    pyxel.sound(6).set("a3 a2 c2 c2", "n", "7742", "s", 10)
    pyxel.music(0).set([4], [5], [], [])
def run_sound():
    pyxel.play(0, 0)
def jump_sound():
    pyxel.play(0, 1)
def stop_sound():
    pyxel.play(0, 2)
def wait_sound():
    pyxel.play(0, 3)
def clear_sound():
    pyxel.playm(0)

def text_draw():
    global game_state, score
    pyxel.rect(219, 9, 35, 7, 7)
    pyxel.text(220, 10, "SCORE:" + str(score), 5)
    if game_state == "START":
        pyxel.text(110, 20, "S:START", 5)
    if game_state == "GAME OVER":
        pyxel.text(110, 10, "GAME OVER", 5)
        pyxel.text(114, 20, "S:START", 5)



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
        bg1 = Mover(0, 20, self.CLOUD_IMG,    0.5, 0)
        bg2 = Mover(0, 58, self.ROCK_IMG,     1,   0)
        bg3 = Mover(0, 96, self.GROUND_IMG,   2,   0)
        self.backgrounds = [bg0, bg1, bg2, bg3]

    def update(self):
        # 背景が左に動くようにX座標を減らす
        if game_state == "START":                   # 雲だけ動かす
            bg = self.backgrounds[1]
            bg.x -= bg.vx
            if bg.x < -SCREEN_WIDTH:
                bg.x = 0
            return

        for bg in self.backgrounds:
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

    def __init__(self):
        self.jump_height = 40
        self.down_speed = 1.7
        self.state = "RUN"
        self.player = Mover(0, 0, self.RUN_IMG, self.down_speed, 0)
        self.x = PLAYER_X
        self.y = GROUND_Y - self.player.height - 1
        self.bottom = self.y + self.player.height
        self.center = self.x + self.player.width / 2

    def update(self):
        if game_state == "START" and ((pyxel.frame_count % 10) == 0):
            wait_sound()
            return

        if self.state == "RUN" and pyxel.btn(pyxel.KEY_SPACE):
            self.y -= self.jump_height
            self.state = "JUMP"
            jump_sound()
        
        if self.state == "JUMP":
            self.y += self.down_speed
            if self.y >= GROUND_Y - self.player.height - 2:
                self.y = GROUND_Y - self.player.height - 2
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

        if (pyxel.frame_count // 5 % 2) == 0 or self.state == "JUMP":
            pyxel.blt(self.x, self.y, *self.JUMP_IMG)
        else:
            pyxel.blt(self.x-1, self.y, *self.RUN_IMG)

class Enemy:
    ENEMY0_IMG = [1,  1, 29, 20, 16, TRANSPARENT_COLOR]
    ENEMY1_IMG = [1, 25, 28, 17, 17, TRANSPARENT_COLOR]
    ENEMY2_IMG = [1, 53, 30, 24, 16, TRANSPARENT_COLOR]
    ENEMY3_IMG = [1, 80, 35,  8, 11, TRANSPARENT_COLOR]
    ENEMY4_IMG = [1, 96, 39,  9,  8, TRANSPARENT_COLOR]
    ENEMY5_IMG = [1,111, 39,  9,  8, TRANSPARENT_COLOR]
    enemy_images = [ENEMY0_IMG, ENEMY1_IMG, ENEMY2_IMG, ENEMY3_IMG, ENEMY4_IMG, ENEMY5_IMG]

    def __init__(self):
        self.interval = [50, 90]
        self.speed = 2
        self.collision_dist_x = 4
        self.collision_dist_y = 4
        self.image_no_list = [0,1,2,2,3,3,4,4,5,5]

        self.enemys = [] 
        for _ in range(ENEMY_MAX):
            img_no = random.choice(self.image_no_list)
            self.enemy = Mover(0, 0, self.enemy_images[img_no], self.speed, 0)
            self.enemy.y =GROUND_Y - self.enemy.height
            self.enemys.append(self.enemy)
        self.init_x()

    def update(self, x, y):
        global game_state, score

        if game_state == "START":
            self.init_x()

        # 左に動くようにX座標を減らす
        for enemy in self.enemys:
            enemy.x -= enemy.vx
        # 衝突判定
        for enemy in self.enemys:
            if enemy.x < x + self.collision_dist_x and \
               enemy.x + enemy.width /2 > x + self.collision_dist_x and \
               y - self.collision_dist_y > enemy.y:
                stop_sound()
                game_state = "GAME OVER"
                return

        score = 0
        for enemy in self.enemys:
            if enemy.x < PLAYER_X:
                score += 1

    def draw(self):
        for enemy in self.enemys:
            pyxel.blt(enemy.x, enemy.y, *enemy.img)
    
    def init_x(self):
        x = SCREEN_WIDTH + 20
        for enemy in self.enemys:
            enemy.x = x
            x += random.randint(*self.interval)

class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, fps=FPS)
        pyxel.load(ASSET_FILENAME)
        sound_set()

        global game_state, score
        game_state = "START"
        score = 0
        self.background = Background()
        self.player = Player()
        self.enemy = Enemy()
        pyxel.run(self.update, self.draw)

    def update(self):
        global game_state

        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()
        
        if game_state == "GAME OVER" and pyxel.btn(pyxel.KEY_S):
            game_state = "START"
            self.enemy.update(0,0)
            return

        if game_state == "GAME OVER":
            return

        if game_state == "START" and pyxel.btn(pyxel.KEY_S):
            game_state = "PLAY"

        self.background.update()
        self.player.update()
        if game_state == "PLAY":
            self.enemy.update(self.player.center, self.player.bottom)

    def draw(self):
        pyxel.cls(14)
        self.background.draw()
        self.enemy.draw()
        self.player.draw()
        text_draw()

App()