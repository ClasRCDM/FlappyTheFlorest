"""Class to effects"""

# & /Imports effects\ & #
# ------ General defs ------ #
from os import path
from random import randint, uniform
# ------ Game variables ------ #
from variáveis import B_SPRITE_TSCALING, B_SPRITE_SIZE
from variáveis import EL_SPRITE_LEAVES, EDJ_SPRITE
# ------ Window modules ------ #
from módulos.Objeto import Object_sprite
# & \Imports effects/ & #


# Particles Sprites -- Effect __ LP, DDJ
class Leave_particle(Object_sprite):
    """ Leaves """

    def __init__(self, pos, diretorio, física):
        """ Starting sheets """
        super().__init__(pos[0], pos[1])

        self.scale: float = B_SPRITE_TSCALING + 1
        self.result_angle = 0

        self.side = randint(0, 1)

        self.speed_x = self.speed_y = randint(0, 2)
        self.play_speed = 0

        # Add texture
        self.set_sprite(self.sprite_loc(
            diretorio, EL_SPRITE_LEAVES[randint(0, 4)]))

        self.set_pos(B_SPRITE_SIZE)
        self.set_física(física)

    def random_pos(self):
        self.speed_x = self.speed_y = randint(0, 2)
        self.set_pos(B_SPRITE_SIZE)

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        """ Handle being moved by the pymunk engine """

        # Leaf fall movement
        self.effects(physics_engine, d_angle)

        if self.center_x >= 400 or self.center_y <= 0:
            self.kill()

    def set_física(self, física):
        física.add_sprite(self,
                          mass=2,
                          max_vertical_velocity=450,
                          max_horizontal_velocity=450,
                          collision_type='item')

    def effects(self, phy, angle):
        """ Leaf fall movements """
        from operator import add, sub

        moddif = None
        if self.side == 0: moddif = add
        elif self.side == 1: moddif = sub

        moddif(round(uniform(0.5, 2.5), 2), self.result_angle)

        self.angle = self.result_angle

        phy.apply_impulse(self, (self.speed_x + self.play_speed,
                                 self.speed_y))


class dash_dust_jump(Object_sprite):
    def __init__(self, pos, diretorio):
        """ init dash animation """
        super().__init__(pos[0], pos[1])

        self.scale: float = B_SPRITE_TSCALING-2.1

        # Add texture
        self.set_sprite(self.sprite_loc(diretorio, EDJ_SPRITE[0]))

        self.set_pos(B_SPRITE_SIZE)

        main_path: str = path.join(
            diretorio, 'texturas/effects/dustjump/FX052')

        # load sprite anim
        self.anim = self.load_texts(main_path, 4)

        # Variables to animation of move sprite
        self.index_texture: int = 0
        self.frames_texture: int = 4

    def animation(self):
        self.set_animation_sprites(
            self.frames_texture, 0.16, self.anim)

        if self.index_texture >= 3.8:
            self.kill()

    def set_animation_sprites(self, q_sprite, speed_sprite, sprites):
        self.index_texture = (self.index_texture + speed_sprite) % q_sprite
        self.texture = sprites[int(self.index_texture)]
