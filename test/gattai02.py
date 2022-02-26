import pygame
from pygame.locals import *
from random import randint, choice
from sys import exit

SCREEN_SIZE = Rect(0, 0, 1280, 720)
""" 画像描画の際に使う座標 """
SCREEN_CENTER = (SCREEN_SIZE[2] / 2, SCREEN_SIZE[3] / 2) # 画面中央
SCREEN_QUARTER = (SCREEN_SIZE[2] / 4, SCREEN_SIZE[3] / 4) # 画面左上
SCREEN_THREE_QUARTER_1 = (SCREEN_SIZE[2] - SCREEN_QUARTER[0], SCREEN_SIZE[3] - SCREEN_QUARTER[1] * 3) # 画面右上
SCREEN_THREE_QUARTER_2 = (SCREEN_QUARTER[0], SCREEN_SIZE[3] - SCREEN_QUARTER[1]) # 画面左下
SCREEN_THREE_QUARTER_3 = (SCREEN_THREE_QUARTER_1[0], SCREEN_THREE_QUARTER_2[1]) # 画面右下

TEXTARIA_POSITION1 = (SCREEN_CENTER[0], SCREEN_CENTER[1] - 270) # テキストエリアの位置
TEXTARIA_POSITION2 = (SCREEN_CENTER[0] - 90, SCREEN_CENTER[1]) # 回答ボタンの位置

PLAY, START, CHOICE, ROLL, ROLL_OFF, ENEMY_POP, BATTLE, ANSWER, ATTACK, GAMEOVER = ("PLAY", "START", "CHOICE", "ROLL", "ROLL_OFF", "ENEMY_POP", "BATTLE", "ANSWER", "ATTACK", "GAMEOVER")


class World():
    def __init__(self, screen, filename):
        self.screen = screen
        self.world_surface = pygame.image.load(filename).convert()
        self.world_rect = self.world_surface.get_rect()

    def draw(self):
        self.screen.blit(self.world_surface, self.world_rect)

    """def updata(self, screen, key):
        if key[K_1]:
            screen.blit(self.world_surface, self.world_rect)
        elif key[K_2]:
            screen.blit(self.world_surface, self.world_rect)"""


class Chara():
    def __init__(self, screen, chara_img, name, life, level, exp, gold, pos):
        self.screen = screen
        self.chara_surface = pygame.image.load(chara_img).convert_alpha()
        self.life_surface = pygame.image.load("test\data\sticon3b-3.png").convert_alpha()
        self.shadowlife_surface = pygame.image.load("test\data\sticon3j-3.png").convert_alpha()
        self.life_surface = pygame.transform.rotozoom(self.life_surface, 0, 1.8)
        self.shadowlife_surface = pygame.transform.rotozoom(self.shadowlife_surface, 0, 1.8)

        self.name = name
        self.maxlife = life
        self.life = life
        self.level = level
        self.exp = exp
        self.gold = gold
        self.pos = pos

        """" rect属性を加え、キャラクター画像の描画開始ポジションをセンタリング """
        self.chara_rect = self.chara_surface.get_rect(center=(self.pos[0], self.pos[1])) # get_rect(center=(位置x,位置y))で画像の中央に描画位置を持ってきてくれるよ
        self.shadowlife_rect = self.shadowlife_surface.get_rect(center=(self.pos[0], self.pos[1]))
        self.life_rect = self.life_surface.get_rect(center=(self.pos[0], self.pos[1]))

        self.textaria = TextAria(self.screen, self.name, self.pos, self.chara_rect) 

    # """" キャラクターを描画 """
    def draw(self):
        if SCREEN_SIZE.contains(self.chara_rect): # pygame.Rect.contain()で、(指定のRect_a).contains(指定のRect_b)を比較し、Rect_aの中にRect_bが入っていればTrueを返す。
            self.screen.blit(self.chara_surface, self.chara_rect)
        else: # もしモンスターの画像がスクリーンからはみ出た場合の処理
            self.chara_rect.center = (self.pos[0], self.pos[1] - 80)
            self.screen.blit(self.chara_surface, self.chara_rect)

        # """ ライフを描画 """
        self.shadowlifes_rectlist = []
        self.lifes_rectlist = []
        self.shadowlife_rect.bottom = self.chara_rect.top
        self.life_rect.bottom = self.chara_rect.top
        # """ 対象の名前の場合、ライフ描画を調整する """
        if self.name == "オーク":
            self.shadowlife_rect.bottom = self.chara_rect.top + 60
            self.life_rect.bottom = self.chara_rect.top + 60
        # """ ライフが1の時の描画 """
        if self.maxlife == 1:
            self.shadowlifes_rectlist.append(self.shadowlife_rect)
            self.lifes_rectlist.append(self.life_rect)
            self.screen.blit(self.shadowlife_surface, self.shadowlife_rect)
            self.screen.blit(self.life_surface, self.life_rect)
        # """ ライフが偶数の時の描画 """
        elif self.maxlife % 2 == 0:
            list_center = int(self.maxlife // 2)
            for i in range(self.maxlife):
                self.shadowlifes_rectlist.append(self.shadowlife_rect.move(-50 * list_center, 0))
                self.screen.blit(self.shadowlife_surface, self.shadowlifes_rectlist[i].move(50 * i + 25, 0))
            for i in range(self.life):
                self.lifes_rectlist.append(self.life_rect.move(-50 * list_center, 0))
                self.screen.blit(self.life_surface, self.lifes_rectlist[i].move(50 * i + 25, 0))            
        # """ ライフが奇数の時の描画 """
        elif self.maxlife % 2 != 0:
            list_center = int(self.maxlife // 2)
            for i in range(self.maxlife):
                self.shadowlifes_rectlist.append(self.shadowlife_rect.move(-50 * list_center, 0))
                self.screen.blit(self.shadowlife_surface, self.shadowlifes_rectlist[i].move(50 * i, 0))            
            for i in range(self.life):
                self.lifes_rectlist.append(self.life_rect.move(-50 * list_center, 0))
                self.screen.blit(self.life_surface, self.lifes_rectlist[i].move(50 * i, 0))
             
    def attack(self, world_surface, hostile_surface, hostile_pos, chara_name):
        dir = 1 # プレイヤー
        if SCREEN_SIZE[2] / 2 <= self.pos[0]:
            dir = -1 # エネミー
        self.textaria.attack_textaria_draw(chara_name, dir, world_surface, self.chara_surface, self.chara_rect, hostile_surface, hostile_pos)
        for i in range(20):
            self.screen.blit(world_surface, [0, 0])
            self.screen.blit(hostile_surface, hostile_pos)
            self.screen.blit(self.chara_surface, [self.chara_rect[0] + i * 15 * dir, self.chara_rect[1]])
            pygame.display.update()
        pygame.time.delay(1000)


class Player(Chara):
    def __init__(self, screen, filename, name, life, level, exp, gold, pos):
        Chara.__init__(self, screen, filename, name, life, level, exp, gold, pos)
        self.chara_surface = pygame.transform.flip(self.chara_surface, True, False) # 画像を反転させてるよ、キャラを左向きから右向きにしてるよ


class Enemy(Chara):
    def __init__(self, screen, filename, name, life, level, exp, gold, pos):
        Chara.__init__(self, screen, filename, name, life, level, exp, gold, pos)
        if self.name == "オーク":
            self.chara_surface = pygame.transform.flip(self.chara_surface, True, False)


class TextAria():
    def __init__(self, screen, chara_name, chara_pos, chara_rect):
        self.screen = screen
        self.chara_name = chara_name
        self.chara_pos = chara_pos
        self.chara_rect = chara_rect
        self.questionaria_surface = pygame.image.load("test\data\woodframe01_blue.png").convert_alpha()
        self.answeraria_surface = pygame.image.load("test\data\pipo-WindowBaseSet2a_09.png").convert_alpha()
        self.player_attacktextaria_surface = pygame.image.load("test\data\s_005_click.png").convert_alpha()
        self.enemy_attacktextaria_surface = pygame.image.load("test\data\s_001_click.png").convert_alpha()

        """ answeraria_surfaceを0.75倍に縮小する """
        self.answeraria_surface = pygame.transform.rotozoom(self.answeraria_surface, 0, 0.75) # 元の画像は120*120なので90*90になる
        self.player_attacktextaria_surface = pygame.transform.rotozoom(self.player_attacktextaria_surface, 0, 0.5)
        self.enemy_attacktextaria_surface = pygame.transform.rotozoom(self.enemy_attacktextaria_surface, 0, 0.5)

        self.questionaria_rect = self.questionaria_surface.get_rect(center=(TEXTARIA_POSITION1))
        self.answeraria_rect = self.answeraria_surface.get_rect(center=(TEXTARIA_POSITION2))
        self.player_attacktextaria_rect = self.player_attacktextaria_surface.get_rect(center=(self.chara_pos[0], self.chara_pos[1]))
        self.player_attacktextaria_rect.bottom = self.chara_rect.top
        self.enemy_attacktextaria_rect = self.enemy_attacktextaria_surface.get_rect(center=(self.chara_pos[0], self.chara_pos[1]))
        self.enemy_attacktextaria_rect.bottom = self.chara_rect.top
        if self.chara_name == "さんぞく":
            self.enemy_attacktextaria_rect.bottom = self.chara_rect.top - 80

        self.text = Text(self.screen, self.chara_name, self.chara_pos, self.chara_rect)

    def draw(self):
        """ 問題を表示する欄を描画 """
        self.screen.blit(self.questionaria_surface, self.questionaria_rect)
        """ 回答ボタンの位置を指定 """
        self.answer_rect = []
        for y in range(4):
            for x in range(3):
                self.answer_rect.append(self.answeraria_rect.move(90 * x, 90 * y))
        """ 回答ボタンを描画 """
        for i in range(len(self.answer_rect)):            
            self.screen.blit(self.answeraria_surface, self.answer_rect[i])
    
    def attack_textaria_draw(self, chara_name, dir, world_surface, chara_surface, chara_rect, hostile_surface, hostile_pos):
        if dir == 1: # プレイヤー
            self.screen.blit(world_surface, [0, 0])
            self.screen.blit(chara_surface, chara_rect)
            self.screen.blit(hostile_surface, hostile_pos)
            self.screen.blit(self.player_attacktextaria_surface, self.player_attacktextaria_rect)
            self.text.attack_text_draw(chara_name)
        if dir == -1: # エネミー
            self.screen.blit(world_surface, [0, 0])
            self.screen.blit(chara_surface, chara_rect)
            self.screen.blit(hostile_surface, hostile_pos)
            self.screen.blit(self.enemy_attacktextaria_surface, self.enemy_attacktextaria_rect)
            self.text.attack_text_draw(chara_name)
        pygame.display.update()
        pygame.time.delay(1000)
            
       
class Text():
    def __init__(self, screen, chara_name, chara_pos, chara_rect):
        self.screen = screen
        self.chara_name = chara_name
        self.chara_pos = chara_pos
        self.chara_rect = chara_rect
        self.WHITE = (255, 255, 255)
        self.filename = "test\data\GN-Koharuiro_Sunray.ttf"
        self.font_16 = pygame.font.Font(self.filename, 16)
        self.font_32 = pygame.font.Font(self.filename, 32)
        self.font_64 = pygame.font.Font(self.filename, 64)
        self.font_120 = pygame.font.Font(self.filename, 110)

    def questiontext_draw(self, num1, num2):
        """ 問題のsurface作成及び、rectの付与 """
        self.question = self.font_32.render("たしざんにこたえよう！", True, self.WHITE)
        self.question_rect = self.question.get_rect(center=(TEXTARIA_POSITION1[0], TEXTARIA_POSITION1[1] - 50))
        """ 描画 """
        self.screen.blit(self.question, self.question_rect)

        """ 足し算のsurface作成及び、rectの付与 """
        self.addition = self.font_120.render("{} + {} = ".format(num1, num2), True, self.WHITE)
        self.addition_rect = self.addition.get_rect(center=(TEXTARIA_POSITION1[0], TEXTARIA_POSITION1[1] + 20))
        """ 描画 """
        self.screen.blit(self.addition, self.addition_rect)

    def answerbotton_draw(self):
        """ 回答ボタンの文字のsurface作成及び、rectの付与 """
        self.answerbotton_str = "1 2 3 4 5 6 7 8 9 BS 0 OK".split() # pygame.font.renderに使用したい文字列のリスト
        """ [1,2,3,4,5,6,7,8,9,BS,0,OK] """
        self.answerbotton_surface_list = [] # renderした時の格納先 return surface
        self.answerbotton_rect_list = [] # get_rectした時の格納先 return rect
        for i in range(len(self.answerbotton_str)):
            self.answerbotton_surface_list.append(self.font_64.render("%s" % self.answerbotton_str[i], True, self.WHITE))
        for i in range(len(self.answerbotton_str)):
            self.answerbotton_rect_list.append(self.answerbotton_surface_list[i].get_rect(center=(TEXTARIA_POSITION2[0] - 3, TEXTARIA_POSITION2[1] + 5)))
        """ 作成したリストを2次元配列に変えるため、n分割する """
        n = 3
        self.answerbotton_surface_chunk = [self.answerbotton_surface_list[i:i + n] for i in range(0, len(self.answerbotton_surface_list), n)]
        """ [[Surface, Surface, Surface], [Surface, Surface, Surface], [Surface, Surface, Surface], [Surface, Surface, Surface]] """
        self.answerbotton_rect_chunk = [self.answerbotton_rect_list[i:i + n] for i in range(0, len(self.answerbotton_rect_list), n)]
        """ [[Rect, Rect, Rect],[Rect, Rect, Rect],[Rect, Rect, Rect],[Rect, Rect, Rect]] """
        """ 描画 """
        for y in range(4):
            for x in range(3):
                self.screen.blit(self.answerbotton_surface_chunk[y][x], (self.answerbotton_rect_chunk[y][x][0] + 93 * x, self.answerbotton_rect_chunk[y][x][1] + 90 * y))
    
    def attack_text_draw(self, chara_name):
        if chara_name == "ヒーロー":
            self.attacktext = self.font_32.render("たたかう", True, self.WHITE)
            self.attacktext_rect = self.attacktext.get_rect(center=(self.chara_pos[0], self.chara_pos[1]))
            self.attacktext_rect.bottom = self.chara_rect.top - 3
        if chara_name == "スライム":
            self.attacktext = self.font_32.render("とびつく", True, self.WHITE)
            self.attacktext_rect = self.attacktext.get_rect(center=(self.chara_pos[0], self.chara_pos[1]))
            self.attacktext_rect.bottom = self.chara_rect.top - 3
        if chara_name == "さんぞく":
            self.attacktext = self.font_32.render("きりかかる", True, self.WHITE)
            self.attacktext_rect = self.attacktext.get_rect(center=(self.chara_pos[0], self.chara_pos[1]))
            self.attacktext_rect.bottom = self.chara_rect.top - 3
        if chara_name == "オーク":
            self.attacktext = self.font_32.render("ぶんまわす", True, self.WHITE)
            self.attacktext_rect = self.attacktext.get_rect(center=(self.chara_pos[0], self.chara_pos[1]))
            self.attacktext_rect.bottom = self.chara_rect.top + 75

        self.screen.blit(self.attacktext, self.attacktext_rect)


class Main():
    def __init__(self):
        
        self.set_object()

        while True:        
            self.clock.tick(60)           
            self.key_handler()

            if self.game_state == None:
                self.game_state = CHOICE

            if self.game_state == CHOICE:
                self.enemy = [ Enemy(self.screen, "test\data\slime_144_120.png", "スライム", 1, 1, 10, 10, SCREEN_THREE_QUARTER_3),
                               Enemy(self.screen, "test\data\sanzoku_a.png", "さんぞく", 4, 3, 3, None, SCREEN_THREE_QUARTER_3),
                               Enemy(self.screen, "test\data\ouck_a.png", "オーク", 7, 10, None, None, SCREEN_THREE_QUARTER_3) ]
                self.choice_enemy = choice(self.enemy)
                self.game_state = START

            if self.game_state == START:
                self.world.draw()
                self.player.draw()
                self.choice_enemy.draw()
                self.player.textaria.draw()
                self.player.textaria.text.answerbotton_draw()
                
                if self.game_phase == None:
                    self.game_phase = ROLL
                if self.game_phase == ROLL_OFF:
                    pass

                if self.game_phase == ROLL:
                    self.rand_num = randint(0, 10), randint(1, 10)
                    self.game_phase = ROLL_OFF

                self.player.textaria.text.questiontext_draw(self.rand_num[0], self.rand_num[1])
                self.Trueans = self.rand_num[0] + self.rand_num[1]
                
                self.Answer = self.answer()
                if self.Answer != None:
                    self.game_phase = ATTACK
            
                if self.game_phase == ATTACK:
                    if self.Trueans == self.Answer:
                        self.player.attack(self.world.world_surface, self.choice_enemy.chara_surface, self.choice_enemy.chara_rect, self.player.name)
                        self.choice_enemy.life -= 1
                        if self.choice_enemy.life > 0:
                            self.game_state = START
                            self.game_phase = None
                        elif self.choice_enemy.life <= 0:
                            self.game_state = CHOICE
                            self.game_phase = None
                    elif self.Trueans != self.Answer:
                        self.choice_enemy.attack(self.world.world_surface, self.player.chara_surface, self.player.chara_rect, self.choice_enemy.name)
                        self.player.life -= 1
                        if self.player.life > 0:
                            self.game_state = START
                            self.game_phase = None
                        if self.player.life <= 0:
                            pass
                
            pygame.display.update()
            
    
    def set_object(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE.size, 0, 32)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("勇者カロとヘルの娘")

        self.answer_list = []
        self.game_state = None
        self.game_phase = None
        self.Trueans = None
        self.Answer = None
        self.rand_num = None
        self.event_pos_x, self.event_pos_y = 0, 0

        self.world = World(self.screen, r"test\data\bg_road00_day_1280_720.jpg") 
        self.player = Player(self.screen, "test\data\hero_185_250.png", "ヒーロー", 3, 1, None, None, SCREEN_THREE_QUARTER_2)

    
    def key_handler(self):
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                self.event_pos_x, self.event_pos_y = event.pos
            if event.type == QUIT:
                pygame.quit()
                exit()
        

    def answer(self):
        if self.player.textaria.answer_rect[0].collidepoint(self.event_pos_x, self.event_pos_y):
            self.answer_list.append(1)
        if self.player.textaria.answer_rect[1].collidepoint(self.event_pos_x, self.event_pos_y):
            self.answer_list.append(2)
        if self.player.textaria.answer_rect[2].collidepoint(self.event_pos_x, self.event_pos_y):
            self.answer_list.append(3)
        if self.player.textaria.answer_rect[3].collidepoint(self.event_pos_x, self.event_pos_y):
            self.answer_list.append(4)
        if self.player.textaria.answer_rect[4].collidepoint(self.event_pos_x, self.event_pos_y):
            self.answer_list.append(5)
        if self.player.textaria.answer_rect[5].collidepoint(self.event_pos_x, self.event_pos_y):
            self.answer_list.append(6)
        if self.player.textaria.answer_rect[6].collidepoint(self.event_pos_x, self.event_pos_y):
            self.answer_list.append(7)
        if self.player.textaria.answer_rect[7].collidepoint(self.event_pos_x, self.event_pos_y):
            self.answer_list.append(8)
        if self.player.textaria.answer_rect[8].collidepoint(self.event_pos_x, self.event_pos_y):
            self.answer_list.append(9)
        if self.player.textaria.answer_rect[9].collidepoint(self.event_pos_x, self.event_pos_y):
            del self.answer_list[-1]
        if self.player.textaria.answer_rect[10].collidepoint(self.event_pos_x, self.event_pos_y):
            self.answer_list.append(0)
       
        if not self.answer_list:
            question = self.player.textaria.text.font_120.render("?", True, self.player.textaria.text.WHITE)
            self.screen.blit(question, (self.player.textaria.text.addition_rect[2] + 500, self.player.textaria.text.addition_rect[3] - 63))
        elif self.answer_list:
            answer_surface = self.player.textaria.text.font_120.render("".join(map(str, self.answer_list)), True, self.player.textaria.text.WHITE)
            self.screen.blit(answer_surface, (self.player.textaria.text.addition_rect[2] + 450, self.player.textaria.text.addition_rect[3] - 63))
            if self.player.textaria.answer_rect[11].collidepoint(self.event_pos_x, self.event_pos_y):
                self.Answer = int("".join(map(str, self.answer_list)))
                self.answer_list.clear()
                return self.Answer
        
        self.event_pos_x, self.event_pos_y = 0, 0 # MOUSEBUTTONイベントから受け取った座標を初期化


if __name__ == "__main__":
    Main()