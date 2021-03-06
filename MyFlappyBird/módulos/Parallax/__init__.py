"""Class Parallax for game."""

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
    """Parallax | Create class file."""

    __slots__ = 'MAX_X', 'PONTO_X', 'layer'

    def __init__(self, x, y,
                 diretorio: str,
                 index, image,
                 max_x, ponto_max,
                 flipp=False):
        """Create Parallax and variables."""
        self.MAX_X = max_x
        self.PONTO_X = ponto_max

        self.layer = Background((x, x-24.61), y,
                                diretorio, index,
                                image, flipp)

        self.set_psize(self.layer, 2)

    def set_psize(self, layer, value):
        """Set size in layers to Parallax."""
        nuns = Iterator(value)
        for index in nuns:
            layer.set_size(self.layer.return_sprite(index), index)

    def _return(self, index, background: Object) -> Sprite:
        return background.return_sprite(index)

    def update(self, background, vel):
        """Update moves."""
        self.movimento(background, vel)

        self.loop_movimento(background, 0)
        self.loop_movimento(background, 1)

    def movimento(self, background, vel):
        """Set move to all layers."""
        nuns = Iterator(2)
        for index in nuns:
            background.movement_aside(background.return_sprite(index), vel)

    def loop_movimento(self, background, index):
        """Do the loop move after x position."""
        if background.return_sprite(index).center_x >= self.MAX_X:
            background.return_sprite(index).center_x = self.PONTO_X


class Background(Object):
    """Parallax | Background Florest."""

    __slots__ = 'background_texturas'

    def __init__(self, x, y,
                 diretorio, index,
                 image, flip_vertical=False):
        """Background florest variables."""
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
        """Set size/pos florest."""
        self.set_location(background, F_SPRITE_SIZE,
                          (self.x[valor], self.y))
        self.set_scaling(background, F_SPRITE_TSCALING)

    def return_sprite(self, index) -> Sprite:
        """Return background sprite."""
        return self.background_texturas[index]

    def movement_aside(self, background, vel):
        """Move aside."""
        background.center_x += vel


class Water:
    """Parallax | Water."""

    def __init__(self, x, y, altura, largura, DIRETORIO):
        """Water variables."""
        self.x, self.y = x, y
        self.altura, self.largura = altura, largura

    def draw(self):
        """Draw Water."""
        draw_rectangle_filled(self.x, self.y,
                              self.largura, self.altura,
                              csscolor.AQUA)
        draw_rectangle_filled(self.x, self.y+30,
                              self.largura, 5,
                              csscolor.LIGHT_CYAN)


class Spawn_leaves:
    """Leaf spwan constant."""

    def __init__(self, pos, diretorio, física) -> None:
        """Variables to loop spwan."""
        self.x, self.y = pos

        self.diretorio = diretorio
        self.física = física

    def leave(self, pos) -> Leave_particle:
        """Return leaves."""
        return Leave_particle(pos, self.diretorio, self.física)

    def generate(self) -> list:
        """Leaf generator."""
        poss = Iterator(EL_LEAVES_POS, op=1)
        return [self.leave((self.x + pos[0], self.y + pos[1])) for pos in poss]
