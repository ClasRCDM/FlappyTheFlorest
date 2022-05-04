"""Objects class file"""

# & /Imports Objects\ & #
# ------ General defs ------ #
from os import path
from typing import Union

from arcade import Sprite, load_texture
# & \Imports Objects/ & #


def Iterator(val, op=0) -> int:
    from numpy import arange

    match op:
        case 1: return (index for index in val)
        case 2: return (index for index in enumerate(val))
        case _: return (index for index in arange(val))


# General Objects -- Object __ OB, OB_SP
class Object:
    """ Object """

    def __init__(self,
                 diretorio, arquivo,
                 x: Union[int, float] = None,
                 y: Union[int, float] = None,
                 index: int = None,
                 image: str = None):
        """ Object Setting

        Args:
            x (Union[int, float], optional): x argument position. Defaults to None.
            y (Union[int, float], optional): y argument position. Defaults to None.
            index (int, optional): sprite index. Defaults to None.
            image (str, optional): sprite name. Defaults to None.
        """

        self.DIRETORIO = diretorio
        self.ARQUIVO = arquivo

        self.x: int | float = x if x is not None else 0
        self.y: int | float = y if y is not None else 0

        self.x_y = self.x, self.y

        self.index = index if index is not None else 0
        self.image = image if image is not None else 'image'

        self.main_path: str = path.join(self.DIRETORIO, self.ARQUIVO)

    def set_location(self,
                     background: Sprite, sprite_size: int,
                     pos: tuple[int, int] = (0, 0),
                     v_pro: bool = False):
        """ Adding positions

        Args:
            background (Sprite): forest background
            sprite_size (int): background scale, size
            pos (tuple[int, int], optional): sprite position on screen. Defaults to (0, 0).
            v_pro (bool, optional): corrects position for reflection. Defaults to False.
        """

        if not v_pro:
            background.set_position(sprite_size * pos[0] + sprite_size / 2,
                                    sprite_size * pos[1] + sprite_size / 2)
        else:
            background.set_position(pos[0], pos[1])

    def set_scaling(self, background: Sprite, sprite_scaling: float):
        """ Adding scales

        Args:
            background (Sprite): forest background
            sprite_scaling (float): background scale
        """

        background.scale = sprite_scaling


class Object_sprite(Sprite):
    """ Object sprite """

    @classmethod
    def load_texts(cls, main_path: str, amount: int):
        return [load_texture(
            f"{main_path}_{texture}.png") for texture in range(amount)]

    def __init__(self,
                 x: Union[int, float] = None,
                 y: Union[int, float] = None):
        """ Object setting

        Args:
            x (Union[int, float], optional): x argument position. Defaults to None.
            y (Union[int, float], optional): y argument position. Defaults to None.
        """
        super().__init__()

        self.x: int | float = x if x is not None else 0
        self.y: int | float = y if y is not None else 0

        self.hit_box_algorithm = self.main_path = 'None'

    def sprite_loc(self, diretorio, sprite) -> str:
        """ Set folder path to sprite

        Args:
            diretorio (str): game folder
            sprite (str): sprite name

        Returns:
            str: full sprite path
        """
        return path.join(diretorio, sprite)

    def _x(self, size) -> int | float:
        """ x argument position

        Args:
            size (int | float): texture size for placement
        """
        return size * self.x + size / 2

    def _y(self, size) -> int | float:
        """ y argument position

        Args:
            size (int | float): texture size for placement
        """
        return size * self.y + size / 2

    def set_pos(self, size):
        """ Set location

        Args:
            size (int | float): texture size for placement
        """

        self.set_position(self._x(size), self._y(size))

    def set_sprite(self, main_path):
        """ Set first sprite

        Args:
            main_path (str): path to texture
        """

        sprite = load_texture(main_path)
        self.texture = sprite
