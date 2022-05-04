"""Bird class file"""

# & /Imports Bird\ & #
# ------ General defs ------ #
from os import path
from numpy import arange

from arcade import Sprite, load_texture_pair
from arcade import PymunkPhysicsEngine, key
# ------ Game variables ------ #
from variáveis import B_SPRITE_TSCALING, B_JUMP_IMPULSE
from variáveis import B_SET_ANGULO, B_SPRITE_SIZE
from variáveis import B_MAXC_ROTAÇÃO, B_MAXB_ROTAÇÃO
from variáveis import B_FRICTION, B_MASSA, B_ANIMFLY_SPEED
from variáveis import B_MAXV_SPEED, B_MAXH_SPEED, TELA_CHEIA
# ------ Window modules ------ #
from módulos.Effect import dash_dust_jump
# & \Imports Bird/ & #


# General bird -- Bird __ B
class Bird(Sprite):
    """ Bird Sprite """

    @classmethod
    def load_text(cls, name: str, main_path: str, amount: int):
        return [load_texture_pair(
            f"{main_path}_{name}{texture}.png") for texture in arange(amount)]

    def __init__(self, pos: tuple[float, float],
                 diretorio: str, game_mode: str):

        """ Init Bird """
        super().__init__()

        self.x, self.y = pos
        self.center_x, self.center_y = self.set_location()

        self.game_mode: str = game_mode
        self.scale = B_SPRITE_TSCALING

        main_path_cor = 'verde', 'vermelho', 'azul'
        main_path: str = path.join(
            diretorio, f'texturas/animation_bird/{main_path_cor[0]}/Passaro_{main_path_cor[0]}')

        # Conjunto de texturas/Carregando texturas
        self.voando_texturas = self.load_text("voando", main_path, 8)
        self.parado_texturas = self.load_text("parado", main_path, 2)
        # self.ciscando_texturas = self.load_text("ciscando", main_path, 3)

        # Textura_Inicial
        self.texture = self.parado_texturas[0][0]
        self.hit_box = self.texture.hit_box_points

        # Variables to animation of move sprite
        self.index_texture = self.y_odometer = self.rotação = 0
        self.frames_texture: int = 2

        self.jump_init = 0
        self.dash_jump = dash_dust_jump((3.55, 1.2), diretorio)

    # Bird __ Settings
    def update(self):
        """ Update geral """

        if self.game_mode == 'Tela_Inicial':
            self.set_animation_sprites(
                self.frames_texture, 0.03, self.parado_texturas)
            self.dash_jump.update()
        elif self.game_mode == 'Gameplay' and self.dash_jump is not None:
            self.dash_jump.animation()
            self.dash_jump.center_x += 1.9

            if self.dash_jump.index_texture >= 3.8:
                self.dash_jump = None

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        """ Handle being moved by the pymunk engine """

        if self.game_mode == 'Gameplay':
            is_on_ground = physics_engine.is_on_ground(self)
            self.y_odometer += dy

            if self.jump_init < 1:
                impulse = (0, B_JUMP_IMPULSE)
                physics_engine.apply_impulse(self, impulse)
                self.jump_init += 1

            # Animação de voar
            if not is_on_ground and dy > 0.1 and abs(self.y_odometer) > 5:
                self.set_animation_sprites(
                    self.frames_texture, B_ANIMFLY_SPEED, self.voando_texturas)
                self.rotação -= B_SET_ANGULO
            else: self.rotação += B_SET_ANGULO-1

            self.angle = self.rotação  # Define o angulo
            # Não deixa ultrapassar do angulo máximo
            if self.angle <= B_MAXC_ROTAÇÃO: self.rotação = B_MAXC_ROTAÇÃO
            elif self.angle >= B_MAXB_ROTAÇÃO: self.rotação = B_MAXB_ROTAÇÃO

    def check_windowpos(self) -> bool:
        """ Check if the player is inside the screen """
        if self.center_y >= TELA_CHEIA[0] or self.center_y <= 0:
            return True
        elif self.center_x >= TELA_CHEIA[1] or self.center_x <= 0:
            return True
        return False

    def set_animation_sprites(self, q_sprite, speed_sprite, sprites):
        """ Make the animations """

        self.x_odometer = 0
        self.index_texture = (self.index_texture + speed_sprite) % q_sprite
        self.texture = sprites[int(self.index_texture)][0]

    def set_location(self) -> int | float:
        """ Return x and y, positions """
        return B_SPRITE_SIZE * self.x + B_SPRITE_SIZE / 2, B_SPRITE_SIZE * self.y-245 + B_SPRITE_SIZE / 2

    def pular(self, chave, física):
        """ Jump bird """

        if chave in [key.UP, key.SPACE]:
            impulse = (0, B_JUMP_IMPULSE)
            física.apply_impulse(self, impulse)

    def set_física(self, física):
        """ Add physics to the bird """
        física.add_sprite(self,
                          friction=B_FRICTION,
                          mass=B_MASSA,
                          moment=PymunkPhysicsEngine.MOMENT_INF,
                          max_vertical_velocity=B_MAXV_SPEED,
                          max_horizontal_velocity=B_MAXH_SPEED,
                          collision_type="player")
