from stats import*
from Teacher_Brawl_Mr_A import*
from Teacher_Brawl_Mrs_S import*
import math
import random

pygame.init()

screen_width = 1440
screen_height = 860
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

running = True
CENTER_x = screen_width / 2
CENTER_y = screen_height

clock = pygame.time.Clock()

Directory = "/Users/brianmasse/Desktop/python/Games/Teacher Brawl - the game"

class Camera:
    def __init__(self, game):
        self.camera = pygame.Rect(0, 0, 1440, 860)
        self.total_scale = 1
        self.x = 0
        self.y = 0
        self.shake_ = 0

    def apply(self, entity):
        if not entity == A.B:
            return entity.rect.move(self.camera.topleft)
        elif entity == A.B:
            return entity.rect.move(round(self.camera.x * .1), round(self.camera.y * .1))


    def scale(self, entity, target):

        if not abs(A.HB1.rect.x - A.HB2.rect.x) == 0:
            #self.total_scale = (1000 / abs(A.HB1.rect.x - A.HB2.rect.x))
            self.total_scale = round((700 / math.sqrt((A.HB1.rect.right - A.HB2.rect.right)**2 + (A.HB1.rect.y - A.HB2.rect.y)**2)), 5)

        self.total_scale = max(0.66, self.total_scale)
        self.total_scale = min(1.6, self.total_scale)

        if self.total_scale >= 2:
            self.total_scale = 2

        CENTER_x = 500 + screen_width
        CENTER_y = 800

        self.keys = pygame.key.get_pressed()

        scaled_x = round(target.rect.width * self.total_scale)
        scaled_y = round(target.rect.height * self.total_scale)
        entity.image = pygame.transform.scale(entity.image, (scaled_x, scaled_y))
        entity.rect = entity.image.get_rect()

        change_x = self.total_scale * ((target.rect.x + target.rect.width / 2) - CENTER_x)
        change_y = self.total_scale * ((target.rect.y + target.rect.height / 2) - CENTER_y)

        entity.rect.center = (round(CENTER_x + change_x), round(CENTER_y + change_y))

    def get_coords(self):
        self.x = -(((A.P.rect.x + A.P.rect.width / 2) + (A.P2.rect.x + A.P2.rect.width / 2)) / 2) + screen_width / 2
        y = abs((A.P.rect.y - A.P2.rect.y )) / 2
        y = min(300, y)
        y = max(A.P.rect.y - y, A.P2.rect.y - y)

        self.y = -y + screen_height / 2
        self.y = max(0, self.y)




    def update(self, target):

        if self.shake_ == 0:
            self.get_coords()
            self.first = 0
            self.second = 0


        if self.shake_ < self.second and self.shake_ >= self.first:
            self.x += 5
            self.y -= 5
            self.shake_ += 1

        if self.shake_ > 0 and self.shake_ < self.first:
            self.x -= 5
            self.y += 5
            self.shake_ += 1

        if self.shake_ >= self.second:
            self.shake_ = 0

        self.camera = pygame.Rect(round(self.x), round(self.y), 1440 , 860)

    def shake(self, first, second):
        self.first = first
        self.second = second
        self.get_coords()
        self.shake_ = True

class player1(pygame.sprite.Sprite):
    def __init__(self, game, mirror, color):
        self.game = game
        self.groups = game.sprite_group, game.scaled
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image = pygame.Surface((100, 50))
        self.image.set_alpha(0)
        #self.image.fill(color)

        self.mirror = mirror
        self.rect = self.image.get_rect()

        self.rect.x = (self.mirror.rect.x)
        self.rect.y = (self.mirror.rect.y)

#================================================================================================================================================================================================



class hit_box1(pygame.sprite.Sprite):
    def __init__(self, game, x, y, left, right, jump, attack, block, start_dir, ID):
        self.game = game
        self.groups = game.sprite_group, game.sprite_players
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image = pygame.Surface((80, 140))
        self.image.set_alpha(0)
        self.rect = self.image.get_rect()
        self.image.fill((227, 51, 51))

        self.counts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        #[self.time(jump(0)), self.zero(stun(1)), self.block_count(parry(2)), self.base_hit_check(hit(3)), self.first_frame_check_hit(4), roll_double_tap(5), crouch_hold(6), slam-count(7), base_hit_count(8), base_hit_count_check(9), charge_up(10), strike_count(11), grab_count(12), grab_hit_count(13), heart_his(14)]
        self.stats = [500, 100]
        #[self.health(0), self.stamina(1)]
        self.controlls = [left, right, jump, attack, block]
        self.boolians = [False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        #[on_ground?(0), air_jump?(1), base_hit?(2), block?(3), stun?(4), hit?(5), crouch?(6), roll?(7), slide(8)?, slam(9)?, base_hit?(10), knockback?(11), touching_ground(12), upwards_spin(13), charge_up(14), jump?(15), strike(16)?, grab(17), grabbed(18), perried?(19)]

        self.j_triggers = []
        self.button = ['m']
        self.joystick = pygame.joystick.Joystick(ID) 
        self.joystick.init()

        self.velocity = 0
        self.force = 0
        self.init_force = 0
        self.x_velocity = 0

        self.rect.x = x
        self.rect.y = y

        self.dir = start_dir
        self.ydir = 0
        self.dir_his = [90]
        self.mod = 1

        self.temp_check3 = False
        self.temp_check4 = False

        self.damage_reduc = 1

        self.life = 3

    def setup(self):
        if A.x == 1:
            self.sprite_player = pygame.sprite.Group()
            self.sprite_player.add(self)
            for i in A.sprite_players:
                if not self == i:
                    self.target = i

            for i in A.sprite_group:
                if i == A.A1 or i == A.A2:
                    if i.target == self.target:
                        self.target_arm = i
                    if i.target == self:
                        self.arm = i

                if i == A.MRA or i == A.MRSS:
                    if i.controlled == self:
                        self.player = i

                    if i.controlled == self:
                        self.player = i

                if self == A.HB1:
                    self.mirrorer = A.P
                if self == A.HB2:
                    self.mirrorer = A.P2

            self.stats[0] = self.player.health
            self.stats[1] = self.player.stamina

    def get_triggers(self):
        self.button = ['m']
        for i in range(6):
            axis = self.joystick.get_axis(i)
            axis = round(axis)
            self.j_triggers.append(axis)

        for i in range(0, 15):
            button = self.joystick.get_button(i)
            if button == 1:
                self.button.append(i)

    def check_dir(self):
        if not self.boolians[5] > 0 and not self.boolians[4]:
            if self.dir != 0:
                self.dir_his = []
                self.dir_his.append(self.dir)

            if self.j_triggers[-3]:
                self.ydir = -self.j_triggers[-3] * 180
                self.dir = 0
            else:
                self.ydir = 0

    def Gravity(self):
        self.counts[0] += 1

        if self.force > 0:
            self.force = self.init_force - (9.8 * self.counts[0])
            if self.force < 0:
                self.force = 0
                self.init_force= 0
                self.counts[0] = 0

    def jump(self):
        self.keys = pygame.key.get_pressed()

        for i in self.button:
            if not self.boolians[4]:
                if self.keys[self.controlls[2]] or i == 0 :

                    if self.boolians[0]:
                        if not self.boolians[15]:
                            self.player.img = "j1.png"
                        self.boolians[15] = True

                        if self.player.img == "j2.png":
                            self.force = 200
                            self.init_force = 200
                            self.boolians[0] = 0
                            self.boolians[12] = False


                    if not self.boolians[0] and self.force == 0 and self.boolians[1]:
                        self.boolians[15] = True
                        self.player.jump_cycle = 0
                        self.force = 200
                        self.init_force = 200
                        self.boolians[1] = False
                        self.counts[0] = 0

                    if self.counts[0] < 10 and self.counts[0] > 4:
                        if self.force < 220 and self.force > 0:
                            self.force += 10
                            self.init_force += 10

    def move(self):
        if not self.boolians[2] and not self.boolians[4] and self.boolians[5] <= 0:
            if self.keys[self.controlls[0]] or self.j_triggers[-6] == -1:
                self.x_velocity = - self.player.walk_speed * self.mod
                self.dir = -90
            elif self.keys[self.controlls[1]] or self.j_triggers[-6] == 1:
                self.x_velocity =  self.player.walk_speed * self.mod
                self.dir = 90

            else:
                self.x_velocity = 0

            if self.counts[3] > 0 and self.ydir != 0:
                self.dir = 0

    def change_size(self, width, height,):
        og_x, og_y = self.rect.x, self.rect.bottom
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.bottom = og_x , og_y

    def check_crouch(self):
        self.temp_check2 = False
        for i in self.button:
            if i == 13 and not self.boolians[8] and not self.boolians[4] and not self.counts[3] > 0 and not self.target.boolians[18]:
                self.temp_check2 = True

        if self.temp_check2:
            if not self.boolians[6]:
                self.change_size(self.rect.width, 100)
                self.boolians[6] = True
                self.mod = .5
                self.damage_reduc = .1
        else:
            if self.boolians[6]:
                self.change_size(self.rect.width, 140,)
                self.boolians[6] = False
                self.mod = 1
                self.damage_reduc = 1

    def check_roll(self):
        if self.temp_check3 == 2 and self.button.count(1) == 0 and self.boolians[0] and not self.stats[1] < 25 and not self.counts[3] > 0 and not self.boolians[4] and not self.target.boolians[18]:
            self.temp_check3 = 3
            self.boolians[0] = False
        elif not self.temp_check3 >= 3:
            self.temp_check3 = False

        for i in self.button:
            if i == 1:
                self.temp_check3 = 2

        if self.temp_check3 >= 3:
            if not self.boolians[7]:
                self.temp_dir = self.dir_his[-1]
                self.change_size(self.rect.width, self.rect.width,)
                self.boolians[7] = True
                self.stats[1] -= 25

            self.x_velocity = 25 * self.temp_dir / -90
            self.temp_check3 += 1
            if self.temp_check3 >= 20:
                self.temp_check3 = False

        else:
            if self.boolians[7]:
                self.change_size(self.rect.width, 140,)
                self.boolians[7] = False

    def check_slide(self):
        hits = pygame.sprite.spritecollide(self, self.target.sprite_player, False)
        if self.button.count(14) >= 1 and abs(self.j_triggers[-6]) == 1 and self.j_triggers[-3] == 1:
            if not self.temp_check4 > 2 and self.boolians[12] and not self.stats[1] < 25 and self.temp_check == False and not self.boolians[4] and not self.target.boolians[18]:
                self.temp_check4 = 2
                self.boolians[0] = False

            elif not self.temp_check4 >= 2:
                self.temp_check4 = False

        if self.button.count(14) == 0 and self.temp_check4 == 100:
            self.temp_check4 = False

        if self.temp_check4 >= 2 and self.temp_check4 < 100:
            if not self.boolians[8]:
                self.change_size(140, 50,)
                self.boolians[8] = True
                self.stats[1] -= 25

            self.x_velocity = 20 * self.dir_his[-1] / 90
            self.temp_check4 += 1
            if self.temp_check4 >= self.player.slide_distance:
                self.temp_check4 = 100

        else:
            if self.boolians[8] or self.boolians[13]:
                self.change_size(80, 140,)
                self.boolians[8] = False

    def check_collide(self, dir):
        for i in range(2):
            if i == 0:
                hits = pygame.sprite.spritecollide(self, self.game.sprite_ground, False)

            if i == 1 and not self.boolians[8]:
                hits = pygame.sprite.spritecollide(self, self.target.sprite_player, False)
            else:
                i = 3

            if dir == 'x':
                if hits:
                    if i == 1 and not self.target.boolians[18]:
                        self.target.rect.x += round(self.x_velocity)
                        self.mod = .2
                    if i == 1 and self.target.boolians[18]:
                        self.target.rect.x += round(self.x_velocity)
                        self.mod = 1

                    elif not self.target.boolians[18]:
                        if self.x_velocity < 0:
                            self.rect.x = hits[0].rect.right
                        if self.x_velocity > 0:
                            self.rect.x = hits[0].rect.left - self.rect.width
                elif not self.mod == 1:
                    self.mod = 1

            if dir == 'y':
                if hits:
                    if self.target.temp_check4 == 100 and i == 1:
                        self.target.temp_check4 = 15

                    if self.force > 0 and not i == 1:

                        self.force = 0
                        self.init_force = 0
                        self.counts[0] = 0
                        self.rect.y = hits[0].rect.bottom

                    if self.velocity > 0:
                        if i == 1 and self.boolians[13] or i == 1 and self.boolians[9]:
                            pass
                        else:
                            self.force = 0
                            self.init_force = 0
                            self.counts[0] = 0
                            self.rect.bottom = hits[0].rect.top
                            self.boolians[0] = True
                            self.boolians[1] = True
                            self.boolians[12] = True
                            if not self.player.img == "j1.png":
                                self.boolians[15] = False

                if not hits and i == 0:
                    self.boolians[12] = False

                    if self.velocity > 0 and i == 1 and not self.boolians[9]:
                        if self.rect.y < self.target.rect.y:
                            self.force = 100
                            self.init_force = 100

    def check_knockbacks(self):
        if self.boolians[11]:
            self.knockback(0, 1, 3)

    def knockback(self, dir, amount, amount2):
        if not self.boolians[11]:
            self.temp_dir = dir
            self.boolians[11] = True
            self.boolians[12] = False
            self.force = amount
            self.init_force = amount
            self.temp_amount = amount
            self.temp_amount2 = amount2

        else:
            if self.boolians[12] and self.counts[0] > 0:
                self.boolians[11] = False
                self.boolians[19] = False
                self.x_velocity = 0

            else:
                self.x_velocity = self.temp_amount2 * self.temp_dir

        if self.temp_amount > 40:
            self.dir = (self.x_velocity / max(1, abs(self.x_velocity))) * -90

    def block(self, damage, perry, knockback):
        if self.target.boolians[3]:
            if self.target.counts[2] <= 5 and perry and not self.target.stats[1] <= 0:
                self.perry(damage, True)
                for i in range(len(self.boolians)):
                    if i == 19 or i == 11:
                        pass
                    else:
                        self.boolians[i] = False

            elif self.target.stats[1] - damage <= 0 and not self.boolians[19]:
                self.target.stun(100)
                self.target.stats[1] -= damage
            elif not self.boolians[19]:
                self.target.stats[1] -= damage

    def charge_up(self):
        hits = pygame.sprite.spritecollide(self.target, self.arm.sprite_arm, False,)
        if self.j_triggers[-2] == 1 and not self.boolians[14] and self.boolians[12] and not self.boolians[14] == -10 and not self.boolians[15] and not self.target.boolians[18]:
            self.counts[10] += 1
            if self.counts[10] >= 15:
                self.stats[1] -= 1
                self.boolians[5] = False
                self.counts[1] = 0
                self.stun(10)

        if not self.j_triggers[-2] == 1 and self.counts[10] >= 15 or self.counts[10] >= 140 or self.boolians[14] == True or self.stats[1] < 0 and self.counts[10] >= 15:
            self.boolians[14] = True
            og_x = round((self.rect.x + (self.rect.width / 2)) + (self.rect.width / 3) * (self.dir / 90))
            og_y = round(self.rect.y + (self.rect.height / 3)) + (self.rect.height / 2) * self.ydir / -180
            self.arm.rect.center = (round(og_x + 50 * self.dir / 90), round(og_y))
            self.counts[10] -= 1
            self.counts[1] = 0
            self.stun(1)

        if self.counts[10] <= 0 or self.boolians[14] and hits and self.target.boolians[5]:
            self.counts[10] = 0
            self.boolians[14] = -10

        if self.boolians[14] == -10 and not self.j_triggers[-2] == 1:
            self.boolians[14] = False

    def slam(self):
        if self.j_triggers[-3] == 1 and self.j_triggers[-5] == 1:
            if not self.boolians[0] and not self.boolians[4] and not self.counts[3] > 0 and not self.target.boolians[18]:
                self.boolians[9] = True
                self.counts[0] = 40
                self.counts[7] = 85
                self.arm.image = pygame.Surface((100, 35))
                og_x = round((self.rect.x + (self.rect.width / 2)) + (self.rect.width / 3) * (self.dir / 90))
                og_y = round(self.rect.y + (self.rect.height / 3)) + (self.rect.height / 2) * self.ydir / -180
                self.arm.rect.center = (og_x, round(og_y + 50 * A.C.total_scale))
        else:
            self.boolians[9] = False
            self.counts[7] = 0

        if self.boolians[0]:
            self.counts[7] = 0
            self.boolians[9] = False

    def upwards_spin(self):
        if self.j_triggers[-2] == 1 and self.ydir == 180 or self.boolians[13]:
            if not self.boolians[6] and not self.boolians[7] and not self.boolians[3] and not self.boolians[4] and not self.target.boolians[18] and self.stats[1] > 25:
                if self.boolians[12] or not self.boolians[1] and self.boolians[15]:
                    if not self.boolians[13]:
                        self.player.spin_cycle = 0
                        self.counts[0] = 0
                        self.boolians[0]= False
                        self.init_force = 400
                        self.force = 400
                        self.boolians[13] = True
                        self.boolians[8] = False
                        self.boolians[12] = False
                        self.boolians[15] = False

        if self.boolians[13]:
            self.arm.image = pygame.Surface((100, 100))
            self.arm.rect = self.arm.image.get_rect()
            og_x = round((self.rect.x + (self.rect.width / 2)))
            og_y = round(self.rect.y - (self.arm.rect.height / 3))
            self.arm.rect.center = (round(og_x), round(og_y))
            self.stats[1] -= 2


        if self.force <= 0 or self.stats[1] < 0:

            self.boolians[13] = False

    def big_boy_strike(self):

        if self.button.count(3) == 1:
            if not self.boolians[3] and not self.boolians[4] and not self.boolians[6] and not self.boolians[7] and not self.boolians[8] and not self.boolians[16] == -5 and not self.target.boolians[18] and self.stats[1] > 30:
                if not self.boolians[16]:
                    self.stats[1] -= 30
                self.boolians[16] = -5

        if self.boolians[16]:
            self.counts[11] += 1
            self.counts[1] = 0
            self.stun(1)
            og_x = round((self.rect.x + (self.rect.width / 2)) + (self.rect.width / 3) * (self.dir_his[-1] / 90))
            og_y = round(self.rect.y + (self.rect.height / 3))
            self.arm.rect.center = (round(og_x), round(og_y))

        if self.boolians[16] == False:
            self.counts[11] = 0

        if self.counts[11] >= 24:
            self.boolians[16] = True
            self.arm.image = pygame.Surface((100, 35))
            self.arm.rect = self.arm.image.get_rect()
            og_x = round((self.rect.x + (self.rect.width / 2)) + (self.rect.width / 3) * (self.dir_his[-1] / 90))
            og_y = round(self.rect.y + (self.rect.height / 3))
            self.arm.rect.center = (round(og_x + 50 * self.dir / 90), round(og_y))

        if self.counts[11] >= 30:
            self.counts[11] = 0
            self.boolians[16] = False

    def base_hit(self):
        self.counts[9] += 1
        if self.counts[9] >= 30:
            self.boolians[5] = 0
            self.counts[9] = 0
            self.counts[3] = 0

        if self.j_triggers[-2] == 1 and not self.boolians[5] == 1 and not self.boolians[5] == -4 and self.ydir == 0 and self.boolians[14] == False and not self.target.boolians[18]:
            self.boolians[5] = 1
        if not self.j_triggers[-2] == 1 and self.boolians[5] == -1:
            self.counts[3] = 1
            self.counts[10] = 0
        if self.j_triggers[-2] == 1 and self.counts[3] == 1:
            self.counts[10] = 0
            self.boolians[5] = 2
        if not self.j_triggers[-2] == 1 and self.boolians[5] == -2:
            self.counts[3] = 2
        if self.j_triggers[-2] == 1 and self.counts[3] == 2:
            self.boolians[5] = 3
            self.counts[10] = 0
        if self.boolians[5] == -4 and not self.j_triggers[-2] == 1:
            self.boolians[5] = 0

        if self.boolians[5] > 0:
            self.counts[8] += 1
            og_x = round((self.rect.x + (self.rect.width / 2)) + (self.rect.width / 3) * (self.dir / 90))
            og_y = round(self.rect.y + (self.rect.height / 3)) + (self.rect.height / 2) * self.ydir / -180
            self.arm.rect.center = (round(og_x + 50 * self.dir / 90), round(og_y))
            if self.counts[8] >= 10:
                self.boolians[5] = -self.boolians[5]
                self.counts[8] = 0
                self.counts[9] = 0
                if self.boolians[5] == -3:
                    self.counts[3] = 0
                    self.boolians[5] = -4

    def base_hit_check(self, check, damage, knockback, knockback2, dir):
        hits = pygame.sprite.spritecollide(self, self.target_arm.sprite_arm, False,)
        if hits and check > 0 or check > 0 and self.boolians[10]:
            if check < 3:
                if not self.boolians[10]:
                    self.target.block(damage / 2 , True, True)
                    if not self.boolians[3]:
                        self.stats[0] -= damage * self.damage_reduc
                        self.leters = letters(A, (240, 62, 62), self.mirrorer, len(A.letters), "-" + str(damage))
                        self.knockback(dir, knockback * 15, knockback)
                    A.C.shake(1, 2)
                    self.boolians[10] = True


            if check == 3:
                if not self.boolians[10]:
                    self.target.block(damage * 2 , True, True)
                    if not self.boolians[3]:
                        self.boolians[11] = False
                        self.leters = letters(A, (240, 62, 62), self.mirrorer, len(A.letters), "-" + str(damage))
                        self.knockback(dir, knockback2 * 15, knockback2)
                        self.stats[0] -= damage * self.damage_reduc
                    A.C.shake(6, 12)
                    self.boolians[10] = True

        else:
            self.boolians[10] = False

    def check_hits(self):
        self.check_hit(self.target_arm.sprite_arm, self.target.boolians[9], self.target.player.slam_damage, self.target.dir_his[-1] / 90, 10, 10, 2)
        self.check_hit(self.target_arm.sprite_arm, self.target.boolians[13], self.target.player.spin_damage, 0 , 10, 40, .1)
        self.check_hit(self.target_arm.sprite_arm, self.target.boolians[14], self.target.counts[10] / 3, self.target.dir_his[-1] / 90 , self.target.counts[10], 1.7, .2)
        self.check_hit(self.target_arm.sprite_arm, self.target.boolians[16], self.target.player.strike_damage, self.target.dir_his[-1] / 90 , 10, 9, 2)
        self.base_hit_check(self.target.boolians[5], self.target.player.base_hit_damage, 1, 15, self.target.dir_his[-1] / 90)

    def check_hit(self, entity, check, damage, dir, knockback, knockback_y, knockback_x):
        hits = pygame.sprite.spritecollide(self, entity, False,)
        if hits and check == True:
            if not self.boolians[5]:
                self.target.block(damage, True, True)
                if self.boolians[3] and self.stats[1] > 0:
                    pass
                else:
                    self.stats[0] -= damage * self.damage_reduc
                    self.leters = letters(A, (240, 62, 62), self.mirrorer, len(A.letters), "-" + str(round(damage, 1)))
                    self.boolians[11] = False
                    self.knockback(dir, knockback * knockback_y, knockback * knockback_x)

    def check_stamina(self,):
        if not self.stats[1] >= self.player.stamina:
            self.stats[1] += self.player.stamina_recharge

    def check_block(self):
        self.temp_check = False
        for i in self.button:
            if self.keys[self.controlls[4]] or i == 6:
                self.temp_check = True

        if self.temp_check:
            self.boolians[3] = True
            self.counts[2] += 1
            self.mod = .5
        else:
            if self.boolians[3]:
                self.mod = 1
            self.counts[2] = 0
            self.boolians[3] = False

    def grab(self):
        if self.button.count(4) == 1:
            if self.boolians[12] and not self.boolians[6] and not self.boolians[7] and not self.boolians[8] and not self.boolians[3] and not self.boolians[4] and not self.boolians[17]:
                self.boolians[17] = -5

        if self.boolians[17] and not self.target.boolians[18]:
            self.counts[12] += 1

        if self.counts[12] >= 15 and not self.target.boolians[18]:
            self.boolians[17] = True
            og_x = round((self.rect.x + (self.rect.width / 2)) + (self.rect.width / 3) * (self.dir / 90))
            og_y = round(self.rect.y + (self.rect.height / 3))
            self.arm.rect.center = (round(og_x + 50 * self.dir / 90), round(og_y))
            self.counts[1] = 0
            self.stun(1)

        if self.counts[12] > 20 and not self.target.boolians[18]:
            self.boolians[17] = -10

        if self.counts[12] > 50 and not self.target.boolians[18] and self.boolians[17] == -10:
            self.boolians[17] = False
            self.counts[12] = 0

        if self.target.boolians[18]:
            self.counts[12] += 1
            self.arm.image = pygame.Surface((150, 35))
            self.arm.rect = self.arm.image.get_rect()
            og_x = round((self.rect.x + (self.rect.width / 2)))
            og_y = round(self.rect.y + (self.rect.height / 3))
            self.arm.rect.center = (round(og_x), round(og_y))

        if self.counts[12] >= 200:
            self.target.boolians[18] = False
            self.counts[12] = 0
            self.boolians[17] = False

    def check_grab(self):
        hits = pygame.sprite.spritecollide(self, self.target_arm.sprite_arm, False,)
        if self.target.boolians[17]     == True and hits and not self.boolians[18]:
            self.target.block(25, True, True)
            if not self.target.boolians[19]:
                self.boolians[18] = True
        if self.boolians[18] and hits:
            self.counts[1] = 0
            self.stun(1)
            self.rect.x = (self.target.rect.x + (self.target.rect.width * round(max(self.target.dir_his[-1] / 90, 0)))) +  round((self.rect.width * min(0, self.target.dir_his[-1] / 90)))
            self.dir = ((self.target.rect.x - self.rect.x) / abs(self.target.rect.x - self.rect.x)) * 90
            self.dir_his.append(((self.target.rect.x - self.rect.x) / abs(self.target.rect.x - self.rect.x)) * 90)

    def check_grab_hit(self):
        if self.target.boolians[18]:
            if self.j_triggers[-2] == 1 and self.counts[13] < 100 or self.counts[13] > 0:
                self.counts[13] += 1
                self.target.check_grab_hit_(0)
            if self.j_triggers[-1] == 1:
                self.counts[13] = 101
                self.target.check_grab_hit_(self.dir_his[-1])

        if self.counts[13] > 10 and not self.j_triggers[-2] == 1 and not self.counts[13] >= 101:
            self.counts[13] = 0
        if self.counts[13] >= 101:
            self.counts[13] += 1
        if self.counts[13] >= 120:
            self.counts[13] = 0

    def check_grab_hit_(self, orginal_dir):
        if self.target.counts[13] < 10 and self.target.counts[13] != 0:
            self.stats[0] -= .5
            self.leters = letters(A, (240, 62, 62), self.mirrorer, len(A.letters), "-" + str(1))
        if self.target.counts[13] == 101:
            if self.boolians[18]:
                self.og_dir = orginal_dir
                self.boolians[18] = False
                self.target.boolians[17] = False

            if self.target.ydir == 0:
                self.knockback(self.og_dir / 90, 200, 25)
            else:
                self.knockback(0, 400, 0)


    def perry(self, power, knockback):
        self.boolians[19] = True
        if knockback:
            self.knockback(self.dir / -90, power * 1.5, power / 2 )
        if self.stats[1] <= 0:
            self.stun(100)
        else:
            self.stun(50)

    def check_stun(self):
        if self.boolians[4] or self.boolians[19]:
            self.stun(self.stun_length)

    def stun(self, stun_length):
        if not self.boolians[11]:
            self.x_velocity = 0
        self.boolians[4] = True
        self.stun_length = stun_length
        self.counts[1] += 1

        if self.boolians[19]:
            for i in range(len(self.boolians)):
                if i == 19 or i == 11 or i == 12 or i == 4:
                    pass
                else:
                    self.boolians[i] = False
                    self.target.boolians[18] = False

        if self.counts[1] > stun_length + 1:
            self.boolians[4] = False
            self.counts[1] = 0

    def draw_hearts(self):
        if self.counts[14] > self.stats[0]:
            if not len(A.particles) >= 10:
                for i in range(random.randrange(1, max(15, min(20, 5 * round((self.counts[14] - self.stats[0]) / 4))))):
                    temp = str(random.randrange(1, 4))
                    file = 'HP' + temp + '.png'
                    A.hearts = particles(A, self.player, 10, 10, file, 35, True)

        self.counts[14] = self.stats[0]

    def check_fall(self):
        if self.rect.y >= 2000:
            self.stats[0] -= 50
            self.rect.y = 660
            self.rect.x = 1500
            self.x_velocity = 0
            self.target.boolians[17] = False
            self.boolians[18] = False
            self.target.counts[12] = 0

    def update(self):
        self.setup()
        self.get_triggers()
        if A.x == 2:

            self.check_stamina()
            self.Gravity()
            self.jump()
            self.move()
            self.check_dir()
            self.check_roll()
            self.check_slide()
            self.check_crouch()
            self.check_block()
            self.grab()
            self.check_grab()
            self.check_grab_hit()
            self.base_hit()
            self.charge_up()
            self.check_hits()
            self.check_knockbacks()
            self.slam()
            self.upwards_spin()
            self.big_boy_strike()
            self.check_stun()
            self.draw_hearts()
            self.check_fall()


            self.velocity = - self.init_force + (9.8 * self.counts[0])
            self.rect.x += round(self.x_velocity)
            self.check_collide('x')
            self.rect.y += round((self.velocity / 15))
            self.check_collide('y',)
            self.image.set_alpha(0)

#================================================================================================================================================================================================


class arm(pygame.sprite.Sprite):
    def __init__(self, game, target):
        count = 0
        self.game = game
        self.sprite_arm = pygame.sprite.Group()
        self.groups = game.sprite_group, self.sprite_arm
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.target = target

        self.image = pygame.Surface((100, 35))

        self.rect = self.image.get_rect()
        self.rect.x = int(50)
        self.rect.y = int(50)

    def update(self):
        if self.target.boolians[5] <= 0 and not self.target.boolians[9] and not self.target.boolians[13] and not self.target.boolians[14] and not self.target.boolians[16] and not self.target.boolians[17] == True and not self.target.target.boolians[18]:
            if self.target.ydir != 0:
                self.image = pygame.Surface((35, 100))
            else:
                self.image = pygame.Surface((100, 35))

            self.rect = self.image.get_rect()

            if self.target.ydir != 0:
                x = round((self.target.rect.x + (self.target.rect.width / 2)) + (self.target.rect.width / 3) * (self.target.dir / 90))
            else:
                x = round((self.target.rect.x + (self.target.rect.width / 2)) + (self.target.rect.width / 3) * (self.target.dir_his[-1] / 90))
            y = round(self.target.rect.y + (self.target.rect.height / 3)) + (self.rect.height / 2) * self.target.ydir / -180

            self.rect.center = (round(x), round(y))
        self.image.set_alpha(0)

class ground_skin(pygame.sprite.Sprite):
    def __init__(self, game, mirror):
        self.game = game
        self.groups = game.sprite_group, game.scaled
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image = pygame.Surface((50, 50))
        self.image.fill((0,0, 0))

        self.mirror = mirror

        self.rect = self.image.get_rect()
        self.rect.x = int(50)
        self.rect.y = int(50)

class ground_hitboxes(pygame.sprite.Sprite):
    def __init__(self, game, width, height, x, y, color):
        self.x = x
        self.y = y
        self.arm = 0

        self.game = game
        self.groups = game.sprite_group, game.sprite_ground
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image = pygame.Surface((width, height))
        self.image.set_alpha(0)
        #self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

class extras_skins(pygame.sprite.Sprite):
    def __init__(self, game, follow, stat):
        self.game = game
        self.groups = game.sprite_group
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.folder = Directory + "/Games/Teacher Brawl - the game/Game images/extra"
        self.image = pygame.image.load(os.path.join(self.folder, "ns.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.img = "ns.png"

        self.stat = stat
        self.follow = follow

    def update(self):
        if self.stat == 3:
            if not self.follow.controlled.boolians[self.stat]:
                self.img = "ns.png"
            if self.follow.controlled.boolians[self.stat]:
                self.img = "s.png"

class embers(pygame.sprite.Sprite):
    def __init__(self, game, ):
        self.game = game
        self.groups = game.sprite_embers
        pygame.sprite.Sprite.__init__(self, self.groups)

        x = random.randrange(4, 8)
        self.image = pygame.Surface((x, x))
        self.image.fill((212, random.randrange(50, 149),83))
        self.rect = self.image.get_rect()
        self.count = 0

    def update(self):
        if self.count == 0:
            self.rect.x = random.randrange(screen_width , screen_width * 3)
            self.rect.y = random.randrange(50, screen_height + 100)
            self.image.set_alpha(random.randrange(155, 255))
            self.count += 1
        else:
            self.count += 1
            if self.count == 2 and self.count < 75:
                self.x = (random.randrange(0, 6))
                self.y = (random.randrange(-1, 2))

            if self.count >= 100:
                self.count = 1

            self.rect.x -= self.x
            self.rect.y += self.y
            if self.rect.x < 0:
                self.count = 0

class background(pygame.sprite.Sprite):
    def __init__(self, game, image, y_change):
        self.game = game
        self.groups = game.backgrounds,
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.img = image
        self.image = pygame.image.load(os.path.join(Directory + "/Game images/background", image)).convert_alpha()
        self.rect = self.image.get_rect()

        self.image = pygame.transform.scale(self.image, (round(self.rect.width * 9), round(self.rect.height * 9)))

        self.rect = self.image.get_rect()
        self.change_y = y_change

    def update(self):
        if A.start_screen:
            self.image = pygame.transform.scale(self.image, (screen_width, screen_height))
            self.rect.x = 0
            self.rect.y = 0
        else:
            self.image = pygame.image.load(os.path.join(Directory + "/Game images/background", self.img)).convert_alpha()
            self.rect = self.image.get_rect()
            self.image = pygame.transform.scale(self.image, (round(self.rect.width * 9), round(self.rect.height * 9)))
            self.rect = self.image.get_rect()

            self.rect.x = -250
            self.rect.bottom = self.change_y

class tiles(pygame.sprite.Sprite):
    def __init__(self, game, folder, image, select, chosen, x, y, move, name, y_change, icon, win):
        self.game = game
        self.groups = game.tiles
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image = pygame.image.load(os.path.join(folder, image)).convert_alpha()
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (self.rect.width * 10, self.rect.height * 10))

        self.rect = self.image.get_rect()

        self.x = x
        self.y = y
        self.img = image
        self.select = select
        self.base = image
        self.folder = folder
        self.movement = move
        self.name = name
        self.y_change = y_change
        self.icon = icon
        self.win = win

        self.chosen = chosen
        self.choose = False
        self.selected = False
        self.move = True

        self.select_region_x = 20
        self.select_region_y = 20

        self.range = []
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

    def get_buttons(self):
        self.button = ['m']
        self.hat = ['m']
        for i in range(0, 15):
            button = self.joystick.get_button(i)
            if button == 1:
                self.button.append(i)
        hat = self.joystick.get_hat(0)
        if abs(hat[0]) == 1:
            self.hat.append(hat[0])

    def change_select(self):
        if self.hat.count(-1) == 0 and self.hat.count(1) == 0:
            self.move = True
        for i in self.hat:
            if self.move:
                if i == -1:
                    self.select_region_x -= self.movement
                    self.move = False
                if i == 1:
                    self.select_region_x += self.movement
                    self.move = False

        if self.select_region_x <= 0:
            self.select_region_x = 20

    def update_image(self):
        self.image = pygame.image.load(os.path.join(self.folder, self.img)).convert_alpha()
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (self.rect.width * 10, self.rect.height * 10))
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

    def check_map(self):
        self.range = []
        for i in range(self.rect.x, self.rect.right):
            self.range.append(i)
        for i in self.range:
            if self.range.count(self.select_region_x) == 0:
                self.img = self.base
                self.selected = False
            else:
                self.img = self.select
                self.selected = True

        if self.selected:
            if self.button.count(0) == 1:
                A.map_screen = 100
            if A.map_screen == 100 and self.button.count(0) == 0 and not A.map_screen == False:
                A.map_screen = False
                for i in A.tiles:
                    A.tiles.remove(i)
                A.MRAT = tiles(A, Directory + "/Game images/tiles", "MRA.png", "MRAS.png", "MRAC.png", 10, 10, 380, 0, 0, "MRAI.png", "MRAW.png")
                A.MRSST = tiles(A, Directory + "/Game images/tiles", "MRSS.png", "MRSSS.png", "MRSSC.png", 400, 10, 380, 0, 0, "MRSSI.png", "MRSSW.png")
                A.name = self.name
                A.y_change = self.y_change

    def check_select(self):
        self.range = []
        for i in range(self.rect.x, self.rect.right):
            self.range.append(i)

        if not self.choose:
            for i in self.range:
                if self.range.count(self.select_region_x) == 0:
                    self.img = self.base
                    self.selected = False
                else:
                    self.img = self.select
                    self.selected = True

            if self.selected and self.button.count(0) == 1:
                self.img = self.chosen
                if not A.player_1_selected:
                    A.I1 = icons(A, Directory + "/Game images/tiles", self.icon, 10, 10)
                    A.player_1_selected = True
                    self.choose = True
                    A.L1 = numbers(A, A.HB1, 120, 10, self.win)
                    if self == A.MRAT:
                        A.MRAB = skin_base(A, A.HB1, 0)
                        A.MRA = Mr_A(A, A.MRAB)
                    if self == A.MRSST:
                        A.MRSSB = skin_base(A, A.HB1, 0)
                        A.MRSS = Mrs_S(A, A.MRSSB)

                elif not self.choose:
                    A.player_2_selected = -100

            if A.player_2_selected == -100 and self.button.count(0) == 0:
                A.I2 = icons(A, Directory + "/Game images/tiles", self.icon, screen_width - 110, 10)
                A.player_2_selected = True
                A.L2 = numbers(A, A.HB2, round(screen_width - 120 - 11 * (100 / 13)), 10, self.win)
                if self == A.MRAT:
                    A.MRAB = skin_base(A, A.HB2, 0)
                    A.MRA = Mr_A(A, A.MRAB)
                if self == A.MRSST:
                    A.MRSSB = skin_base(A, A.HB2, 0)
                    A.MRSS = Mrs_S(A, A.MRSSB)




    def update(self):
        self.get_buttons()
        self.change_select()
        self.update_image()

        if A.map_screen:
            self.check_map()

        else:
            self.check_select()

class icons(pygame.sprite.Sprite):
    def __init__(self, game, folder, image, x, y):
        self.groups = game.sprite_embers
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image = pygame.image.load(os.path.join(folder, image)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

class numbers(pygame.sprite.Sprite):
    def __init__(self, game, target, x, y, win):
        self.groups = game.sprite_embers
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image = pygame.image.load(os.path.join(Directory + "/Game images/numbers", "3.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (round(11 * (100 / 13)), 100))
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y
        self.win = win

        self.count = 0
        self.change_x = []
        self.change_y = []

        self.rect.x = x
        self.rect.y = y
        self.target = target

        self.move_ = False

    def update_image(self):
        self.image = pygame.image.load(os.path.join(Directory + "/Game images/numbers", self.img)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (round(11 * (100 / 13)), 100))
        self.rect = self.image.get_rect()

    def move(self):
        self.move_ = True
        self.rect.x = round(screen_width / 2 - self.rect.width / 2)
        self.rect.y = round(screen_height / 2)

        self.count += 1
        for i in range(min(self.x, self.rect.x), max(self.x, self.rect.x), 8):
            self.change_x.append(i)
        for i in range(self.y, round(screen_height / 2), 6):
            self.change_y.append(i)

        self.rect.x = self.change_x[round(self.count * ((self.x - screen_width / 2) / (abs(self.x - screen_width / 2))))]
        self.rect.y = self.change_y[ - self.count]

        if self.change_x[self.count] == self.change_x[-1]:
            self.move_ = False

    def update(self):
        self.img = str(self.target.life) + '.png'
        if self.move_:
            self.move()
        else:
            self.count = 0
            self.update_image()
            self.rect.x = self.x
            self.rect.y = self.y

        if self.target.stats[0] <= 0:
            self.target.life -= 1
            self.target.stats[0] = self.target.player.health
            if self.target.life < 0:
                A.end_game = True
                self.target.life = 0
                if self == A.L1:
                    self.image = pygame.image.load(os.path.join(Directory + "/Game images/tiles", A.L2.win)).convert_alpha()
                else:
                    self.image = pygame.image.load(os.path.join(Directory + "/Game images/tiles", A.L1.win)).convert_alpha()

                self.rect = self.image.get_rect()
                self.image = pygame.transform.scale(self.image, (self.rect.width * 15, self.rect.height * 15))
                self.rect = self.image.get_rect()

                self.rect.x = round(screen_width / 2- self.rect.width / 2)
                self.rect.y = round(screen_height / 2 - 100)

            else:
                self.img = str(self.target.life) + '.png'
                self.update_image()
                self.move()

class letters(pygame.sprite.Sprite):
    def __init__(self, game, color, target, ID, msg):
        self.groups = game.letters, game.sprite_embers
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image = pygame.Surface((20,20))
        self.rect = self.image.get_rect()
        self.change = [0]
        self.count = -600

        self.ID = ID
        self.color = color
        self.target = target

        self.group_list = []
        self.msg = msg

    def update(self):
        self.group_list = []
        self.font = pygame.font.Font(Directory + "/Fonts/PixelEmulator-xq08.ttf", round(15 * A.C.total_scale))
        self.image = self.font.render(self.msg, False, self.color,).convert()
        self.rect = self.image.get_rect()

        for i in A.letters:
            self.group_list.append(i)
        for i in range(255):
            self.change.append(i)

        if len(self.group_list) > 4:
            if self.group_list.index(self) == 0:
                A.sprite_embers.remove(self)
                A.letters.remove(self)

        if not self.count >= 245:
            self.count += 10
        else:
            A.sprite_embers.remove(self)
            A.letters.remove(self)
        if self.count > 0:
            self.image.set_alpha(self.change[ - self.count])

        self.rect.x = round(self.target.rect.x + A.C.camera.x - self.rect.width)
        self.rect.y = round(self.target.rect.y + A.C.camera.y + (12 * A.C.total_scale   * self.group_list.index(self)))

class particles(pygame.sprite.Sprite):
    def __init__(self, game, location, speed, slope, image, fade, rot = False):
        self.groups = game.sprite_embers, game.particles
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image = pygame.image.load(os.path.join(Directory + "/Game images/extra", "DA.png")).convert_alpha()

        self.rect = self.image.get_rect()
        self.location = location

        self.x =  random.randrange(0, self.location.rect.width)
        self.y =   random.randrange(0, 50)

        self.slope = random.randrange(-slope, slope)
        self.speed = random.randrange(-speed, speed)

        self.change = []
        for i in range(0, 255, fade):
            self.change.append(i)

        self.img = image

        self.count = 260
        self.count2 = 0

        self.rot = rot

    def update(self):
        self.count2 += 1
        self.image = pygame.image.load(os.path.join(Directory + "/Game images/extra", self.img)).convert_alpha()
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (round(self.rect.width * A.C.total_scale * 1.4), round(self.rect.height* A.C.total_scale * 1.4)))
        self.rect = self.image.get_rect()

        if self.rot:
            self.image = pygame.transform.rotate(self.image, 50)

        self.rect.x = self.location.rect.x + A.C.camera.x + self.x + (self.count2 * self.speed)
        self.rect.y =self.location.rect.y + A.C.camera.y +  self.y + (self.slope * self.count2)

        if self.count > 250:
            self.count -= 1
        elif self.count == 250:
            self.count = 0
        if self.count < 250:
            self.count += 1

            if self.count >= len(self.change):
                A.sprite_embers.remove(self)
                A.particles.remove(self)
            else:
                self.image.set_alpha(self.change[- self.count])


class sys():
    def __init__(self):
        self.name = 0
        self.x = 0
        self.start_screen = True
        self.map_screen = True
        self.y_change = 0
        self.end_game = False

        self.player_1_selected = False
        self.player_2_selected = False

        self.sprite_group = pygame.sprite.Group()
        self.sprite_ground = pygame.sprite.Group()
        self.sprite_players = pygame.sprite.Group()
        self.sprite_embers = pygame.sprite.Group()
        self.scaled = pygame.sprite.Group()
        self.tiles = pygame.sprite.Group()
        self.backgrounds = pygame.sprite.Group()
        self.letters = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()

        self.C = Camera(self)

        self.G = ground_hitboxes(self, screen_width * 2, 500, -120, 800, (0,0,0))
        self.G2 = ground_hitboxes(self, 200, 10, 1350, 300, (0, 0 ,0))
        self.G3 = ground_hitboxes(self, 100, 10, 1300, 550, (0, 0 ,0))

        self.HB1 = hit_box1(self, 400, 660, MrA_stats[2], MrA_stats[3], MrA_stats[4], MrA_stats[5], MrA_stats[6], 90, 0)
        self.HB2 = hit_box1(self, 1500, 660, MrsS_stats[2], MrsS_stats[3], MrsS_stats[4], MrsS_stats[5], MrsS_stats[6], -90, 1)
        self.A1 = arm(self, self.HB1)
        self.A2 = arm(self, self.HB2)

        self.GS = ground_skin(self, self.G)
        self.GS2 = ground_skin(self, self.G2)
        self.GS3 = ground_skin(self, self.G3)
        self.P = player1(self, self.HB1, (227, 51, 51))
        self.AS1 = player1(self, self.A1, (207, 12, 12))
        self.P2 = player1(self, self.HB2, (52, 180, 235))
        self.AS2 = player1(self, self.A2, (0, 136, 227))

        #self.MRAB = skin_base(self, self.HB1, 0)
        #self.MRA = Mr_A(self, self.MRAB)
        #self.MRSSB = skin_base(self, self.HB2, 0)
        #self.MRSS = Mrs_S(self, self.MRSSB)
        #self.name = 'aud1.png'
        #self.map_screen = False
        #self.start_screen = False

        self.AUD = tiles(self, Directory + "/Game images/background", "aud_win.png", "aud_win2.png", "aud_win2.png", 10, 5, 310, "aud1.png", 1100, 0, 0)
        self.SOC = tiles(self, Directory + "/Game images/background", "soc_win.png", "soc_win2.png", "soc_win2.png", 320, 5, 310, "soc1.png", 1000, 0, 0)
        self.SOC = tiles(self, Directory + "/Game images/background", "cor_win.png", "cor_win2.png", "cor_win2.png", 640, 5, 310, "cor1.png", 950, 0, 0)
        self.SOC = tiles(self, Directory + "/Game images/background", "fron_win.png", "fron_win2.png", "fron_win2.png", 950, 5, 310, "fron1.png", 1000, 0, 0)

        for i in range(500):
            self.i = embers(self)

        self.x += 1

    def draw_stamina_bars(self, target):
        center = (min(0, (- target.rect.width) * target.controlled.dir_his[-1] / 90 ))
        start_x = round(target.rect.x + abs((target.center * 3 * A.C.total_scale) + center) - ((80 * A.C.total_scale) / 2) + A.C.camera.x)

        pygame.draw.rect(screen, (197, 218, 250), ((start_x, round(target.rect.y - (25 * A.C.total_scale) + A.C.y)), (round(80 * A.C.total_scale), round(14 * A.C.total_scale))))
        pygame.draw.rect(screen, (79, 182, 255), ((start_x, round(target.rect.y - (25 * A.C.total_scale) + A.C.y)), ((round((80 * A.C.total_scale) * max(0, (target.controlled.stats[1] / target.stamina)))), round(14 * A.C.total_scale))))
        pygame.draw.rect(screen, (0, 0, 0), ((start_x, round(target.rect.y - (25 * A.C.total_scale) + A.C.y)), (round(80 * A.C.total_scale), round(14 * A.C.total_scale))), round(3 * A.C.total_scale))

    def draw_health_bars(self, target, screen_div, total, start_x):
        pygame.draw.rect(screen, (197, 218, 250), ((start_x, 12), (490, 35)),)
        pygame.draw.rect(screen, (244, 66, 66), ((start_x, 12), ((round(490 * (target.mirror.stats[0] / target.mirror.player.health)), 35))))
        pygame.draw.rect(screen, (0, 0, 0), ((start_x, 12 ), (490, 35)), 5)

    def update_shield(self, target):
        self.ESA.image = pygame.image.load(os.path.join(self.ESA.folder, self.ESA.img)).convert_alpha()
        self.ESA.rect = self.ESA.image.get_rect()
        self.ESA.image = pygame.transform.scale(self.ESA.image, (round((self.ESA.rect.width * 2) * self.C.total_scale ), round((self.ESA.rect.height * 2) * self.C.total_scale)))
        self.ESA.rect = self.ESA.image.get_rect()
        self.ESA.rect.x = target.rect.x
        self.ESA.rect.y = target.rect.y

    def draw(self):
        for i in A.scaled:
            A.C.scale(i, i.mirror)
        if A.x == 1:
            A.x = 2
        for i in A.sprite_group:
            screen.blit(i.image, A.C.apply(i))
        A.sprite_embers.draw(screen)

        self.draw_stamina_bars(A.MRA)
        self.draw_health_bars(A.P, 1, 2, round(130 + 11 * (100 / 13)))
        self.draw_stamina_bars(A.MRSS)
        self.draw_health_bars(A.P2, 2, 2, 735)
        #self.update_shield(A.MRA)

    def update(self):
        if not self.map_screen:
            if len(self.backgrounds) == 0:
                self.B = background(self, self.name, self.y_change)
            if not self.end_game:
                A.B.update()
            screen.blit(self.B.image, A.C.apply(A.B))

        if not self.start_screen:
            if not self.end_game:
                A.sprite_embers.update()
                A.sprite_group.update()
                A.C.update(A.HB1)
            self.draw()

        else:
            self.tiles.update()
            self.tiles.draw(screen)
            if self.player_1_selected and self.player_2_selected == True:
                self.start_screen = False

        clock.tick(60)

A = sys()

while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    A.update()
    pygame.display.flip()

pygame.quit()
