"""Parallax program file"""

# & /Imports Parallax\ & #
# ------ General defs ------ #
from arcade import Sprite
from arcade import draw_rectangle_filled, csscolor
# ------ Game variables ------ #
from variáveis import F_SPRITE_SIZE, F_SPRITE_TSCALING
from variáveis import ARQUIVO_BACKGROUND, EL_LEAVES_POS
# ------ Window modules ------ #
from módulos.Objeto import Object, Iterator
from módulos.Effect import Leave_particle
# & \Imports Parallax/ & #


# Itens parallax -- Parallax __ PLL, BG, W, SL
class Parallax:
    """ Parallax class file """

    def __init__(self, x, y,
                 diretorio: str,
                 index, image,
                 max_x, ponto_max,
                 flipp=False):
        """ Init Parallax """

        self.MAX_X = max_x
        self.PONTO_X = ponto_max

        self.layer = Background((x, x-24.61), y,
                                diretorio, index,
                                image, flipp)

        self.set_psize(self.layer, 2)

    def set_psize(self, layer, value):

        nuns = Iterator(value)
        for index in nuns:
            layer.set_size(self.layer.return_sprite(index), index)

    def _return(self, index, background: Object) -> Sprite:
        return background.return_sprite(index)

    def update(s_up, background, vel):
        s_up.movimento(background, vel)

        s_up.loop_movimento(background, 0)
        s_up.loop_movimento(background, 1)

    def movimento(self, background, vel):

        nuns = Iterator(2)
        for index in nuns:
            background.movement_aside(background.return_sprite(index), vel)

    def loop_movimento(self, background, index):
        if background.return_sprite(index).center_x >= self.MAX_X:
            background.return_sprite(index).center_x = self.PONTO_X


class Background(Object):
    """ Background Sprites """

    def __init__(self, x, y,
                 diretorio, index,
                 image, flip_vertical=False):
        """ Init Background """
        from numpy import arange
        super().__init__(diretorio, ARQUIVO_BACKGROUND)

        self.x, self.y = x, y
        self.image, self.index = image, index

        # Conjunto de texturas/Carregando texturas
        self.background_texturas = [Sprite(
            f"{self.main_path}_{self.image}{self.index}.png",
            hit_box_algorithm='None',
            flipped_vertically=flip_vertical
            ) for _ in arange(2)]

    def set_size(self, background, valor):
        self.set_location(background, F_SPRITE_SIZE,
                          (self.x[valor], self.y))
        self.set_scaling(background, F_SPRITE_TSCALING)

    def return_sprite(self, index) -> Sprite:
        """ return background sprite """
        return self.background_texturas[index]

    def movement_aside(self, background, vel):
        background.center_x += vel


class Water:
    """ Water init """

    def __init__(self, x, y, altura, largura, DIRETORIO):
        """ Water variables """

        self.x, self.y = x, y
        self.altura, self.largura = altura, largura

    def draw(self):
        """ Draw Water """
        draw_rectangle_filled(self.x, self.y,
                              self.largura, self.altura,
                              csscolor.AQUA)
        draw_rectangle_filled(self.x, self.y+30,
                              self.largura, 5,
                              csscolor.LIGHT_CYAN)


class Spawn_leaves:
    def __init__(self, pos, diretorio, física) -> None:

        self.x, self.y = pos

        self.diretorio = diretorio
        self.física = física

    def leave(self, pos) -> Leave_particle:
        return Leave_particle(pos, self.diretorio, self.física)

    def generate(self) -> list:
        poss = Iterator(EL_LEAVES_POS, op=1)
        leaves = [self.leave((self.x + pos[0], self.y + pos[1]))
                  for pos in poss]

        return leaves
