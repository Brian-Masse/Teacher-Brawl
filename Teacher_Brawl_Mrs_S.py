import pygame
import pygame
import math
import os

Directory = "/Users/brianmasse/Developer/Python/Teacher-Brawl"


class Mrs_S(pygame.sprite.Sprite):
    def __init__(self, game, controlled):
        self.game = game
        self.groups = game.sprite_group, game.scaled
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.folder = Directory + "/Game images/Mrs S"
        self.image = pygame.image.load(os.path.join(
            self.folder, "b.png")).convert_alpha()
        self.rect = self.image.get_rect()

        self.mirror = controlled
        self.controlled = controlled.controlled

        self.base_hit_count = 0
        self.walk_cycle = 0
        self.walk_cycle_change = 1
        self.center = 0

        self.roll_cycle = 0
        self.jump_cycle = 0
        self.spin_cycle = 0
        self.knockback_cycle = 0
        self.attack_cycle = 0

        self.health = 500
        self.stamina = 200
        self.walk_speed = 13
        self.slide_distance = 33
        self.base_hit_damage = 15
        self.slam_damage = 2
        self.spin_damage = 2
        self.strike_damage = 15
        self.stamina_recharge = .8

    def check_image(self):
        if abs(self.controlled.j_triggers[-6]) == 1 or self.controlled.boolians[8] or self.controlled.boolians[5] > 0 or self.controlled.boolians[6] or self.controlled.boolians[7] or self.controlled.boolians[9] or self.controlled.boolians[15] or self.controlled.boolians[13] or self.controlled.ydir != 0 or self.controlled.velocity > 10 or self.controlled.boolians[4] or self.controlled.boolians[3] or self.controlled.boolians[14] == True or self.controlled.boolians[11] or self.controlled.boolians[16] or self.controlled.boolians[17] or self.controlled.counts[13] >= 101:
            if self.controlled.ydir == 180:
                self.img = "lu.png"
                self.center = 7

            if self.controlled.velocity > 10:
                self.img = "j2.png"
                self.center = 16

            if self.controlled.boolians[3]:
                self.img = "bl.png"
                self.center = 14

            if abs(self.controlled.j_triggers[-6]) == 1 and not self.controlled.boolians[4]:
                self.walk_cycle += self.walk_cycle_change

                if self.walk_cycle <= 10:
                    self.img = "w1.png"
                    self.center = 11
                    if self.controlled.boolians[3]:
                        self.img = "bl1.png"
                        self.center = 16
                    if self.controlled.target.boolians[18]:
                        self.img = "gw1.png"
                        self.center = 21
                        if self.controlled.counts[13] > 0 and self.controlled.counts[13] < 10:
                            self.img = "gwa1.png"
                            self.center = 22
                if self.walk_cycle > 10 and self.walk_cycle <= 20:
                    self.img = 'w2.png'
                    self.center = 10
                    if self.controlled.boolians[3]:
                        self.img = "bl2.png"
                        self.center = 15
                    if self.controlled.target.boolians[18]:
                        self.img = "gw2.png"
                        self.center = 21
                        if self.controlled.counts[13] > 0 and self.controlled.counts[13] < 10:
                            self.img = "gwa2.png"
                            self.center = 22
                if self.walk_cycle > 20 and self.walk_cycle <= 30:
                    self.img = 'w3.png'
                    self.center = 19
                    if self.controlled.boolians[3]:
                        self.img = "bl3.png"
                        self.center = 19
                    if self.controlled.target.boolians[18]:
                        self.img = "gw3.png"
                        self.center = 21
                        if self.controlled.counts[13] > 0 and self.controlled.counts[13] < 10:
                            self.img = "gwa3.png"
                            self.center = 22
                    if self.walk_cycle == 30:
                        self.walk_cycle_change = -1

                if self.walk_cycle == 0:
                    self.walk_cycle_change = 1

            if self.controlled.boolians[17]:
                if self.controlled.boolians[17] and not self.controlled.target.boolians[18] or self.controlled.boolians[17] == -10 and not self.controlled.target.boolians[18]:
                    self.img = "g2.png"
                    self.center = 20
                if self.controlled.boolians[17] == -5:
                    self.img = "g1.png"
                    self.center = 15
                if self.controlled.target.boolians[18] and not abs(self.controlled.j_triggers[-6]) == 1 and not self.controlled.boolians[4]:
                    self.img = 'gs.png'
                    self.center = 21
                if self.controlled.counts[13] > 0 and self.controlled.counts[13] < 10 and not abs(self.controlled.j_triggers[-6]) == 1:
                    self.img = "ga.png"
                    self.center = 22

            if self.controlled.boolians[8]:
                self.img = 'sl.png'
                self.center = 39

            if self.controlled.boolians[6]:
                self.img = 'c.png'
                self.center = 10

            if self.controlled.boolians[7]:
                self.img = 'r.png'
                self.center = 17

            if self.controlled.boolians[15]:
                self.img = 'j1.png'
                self.center = 11
                self.jump_cycle += 1
                if self.jump_cycle > 9:
                    self.img = 'j2.png'
                    self.center = 12

            if self.controlled.boolians[5] > 0 and not self.controlled.boolians[4]:
                self.img = "a2.png"
                self.center = 18

            if self.controlled.boolians[13]:
                if self.spin_cycle < 8:
                    self.img = "u1.png"
                    self.center = 16
                if self.spin_cycle >= 8 and self.spin_cycle < 16:
                    self.img = "u2.png"
                    self.center = 4
                if self.spin_cycle >= 16 and self.spin_cycle < 24:
                    self.img = "u3.png"
                    self.center = 18
                if self.spin_cycle >= 24 and self.spin_cycle < 32:
                    self.img = "u4.png"
                    self.center = 15
                    if self.spin_cycle > 31:
                        self.spin_cycle = 0

                self.spin_cycle += 1

            if self.controlled.boolians[9]:
                self.img = 's.png'
                self.center = 30

            if self.controlled.boolians[4] and not self.controlled.boolians[17]:
                self.img = 'st.png'
                self.center = 4

            if self.controlled.counts[10] >= 15:
                self.img = 'cu.png'
                self.center = 29

            if self.controlled.boolians[14] == True:
                self.img = "cua.png"
                self.center = 19

            if self.controlled.boolians[11] and self.controlled.temp_amount > 40:
                self.img = 'k.png'
                self.center = 34

            if self.controlled.boolians[16]:
                if self.controlled.boolians[16] == -5:
                    self.img = 'bbs1.png'
                    self.center = 6
                else:
                    self.img = 'bbs2.png'
                    self.center = 15

        else:
            self.img = "b.png"
            self.center = 7
            self.jump_cycle = 0
            self.spin_cycle = 0
            self.knockback_cycle = 0
            self.attack_cycle = 0

    def update_image(self):

        self.image = pygame.image.load(os.path.join(
            self.folder, self.img)).convert_alpha()
        self.image = pygame.transform.flip(self.image, int(
            max(0, self.controlled.dir_his[-1] / 90)), 0)
        if self.img == 'r.png':
            self.roll_cycle += 15
            self.image = pygame.transform.rotate(
                self.image, self.roll_cycle * self.controlled.dir_his[-1] / 90)
        if self.img == 'k.png':
            self.knockback_cycle += .2
            self.image = pygame.transform.rotate(
                self.image, self.knockback_cycle * self.controlled.dir_his[-1] / 90)
        else:
            self.rol_cycle = 0
        self.rect = self.image.get_rect()

    def update(self):
        self.check_image()
        self.update_image()

        self.mirror.get_size(self.rect.width * 3,
                             self.rect.height * 3, self.center, 3)
