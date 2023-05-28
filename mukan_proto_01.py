from collections import deque, namedtuple
from random import randint
import pyxel

Point = namedtuple("Point", ["w", "h"])  # 猫の向き

UP = Point(-16, 16)
DOWN = Point(16, 16)
RIGHT = Point(-16, 16)
LEFT = Point(16, 16)


class App:

    def __init__(self):
        pyxel.init(128,80,title= "CKSM -- CATCH THE RAINBOW !")
        pyxel.load("PYXEL_mukan.pyxres")
        
        '''
        org_colors = pyxel.colors.to_list() # 表示色リストの取得
        pyxel.colors[0]  = 0x000000
        pyxel.colors[1]  = 0x2b335f
        pyxel.colors[2]  = 0x7e2072
        pyxel.colors[3]  = 0x068500
        pyxel.colors[4]  = 0x8b4852
        pyxel.colors[5]  = 0x0000fe
        pyxel.colors[6]  = 0xa9c1ff
        pyxel.colors[7]  = 0xeeeeee
        pyxel.colors[8]  = 0xff0000
        pyxel.colors[9]  = 0xd38441
        pyxel.colors[10] = 0xe7e70a
        pyxel.colors[11] = 0x0cff00
        pyxel.colors[12] = 0x7696de
        pyxel.colors[13] = 0x9bff7c
        pyxel.colors[14] = 0xff9798
        pyxel.colors[15] = 0xedc7b0
        pyxel.colors.from_list(org_colors) # 表示色リストの代入
        '''

        self.image_origin_u=16
        self.image_origin_v=0
        
        
        self.direction = RIGHT
        # Score
        self.score = 0
        # Starting Point
        self.player_x = 20
        self.player_y = 20
        self.player_vy = 0

        self.rainbow = [(i * 60, randint(0, 104), True) for i in range(4)]
   
        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        self.update_player()

        
        for i, v in enumerate(self.rainbow):
            self.rainbow[i] = self.update_rainbow(*v)
        
    def update_player(self):
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            self.player_x = max(self.player_x - 2, 0)
            self.direction = LEFT
            self.image_origin_u = 32 
            self.image_origin_v = 16

        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            self.player_x = min(self.player_x + 2, pyxel.width - 16)
            self.direction = RIGHT
            self.image_origin_u = 16
            self.image_origin_v = 16

        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            self.player_y = max(self.player_y - 2, 0)
            self.direction = UP
            self.image_origin_u = 32
            self.image_origin_v = 0

        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            self.player_y = min(self.player_y + 2, pyxel.height - 16)
            self.direction = DOWN
            self.image_origin_u = 16
            self.image_origin_v = 0
            


    def draw(self):
        # bg color
        pyxel.cls(12)

        
        # draw rainbow
        
        for x, y, is_active in self.rainbow:
            if is_active:
                pyxel.blt(x, y, 0, 0, 72, 16, 8, 13)
        

        # draw cat
        pyxel.blt(
            self.player_x,
            self.player_y,
            0,
            self.image_origin_u,
            self.image_origin_v,
            16,
            16,
            13,
        )

        # スコアを表示
        s = "Score  {:>4}".format(self.score)
        pyxel.text(5, 4, s, 1)
        pyxel.text(4, 4, s, 7)

    def update_rainbow(self, x, y, is_active):
        if is_active and abs(x - self.player_x) < 12 and abs(y - self.player_y) < 12:
            is_active = False
            self.score += 100
            self.player_vy = min(self.player_vy, -8)
            pyxel.play(3, 4)

        x -= 1

        if x < -40:
            x = randint(40, 128)
            y = randint(0, 70)
            is_active = True

        return (x, y, is_active)

App()