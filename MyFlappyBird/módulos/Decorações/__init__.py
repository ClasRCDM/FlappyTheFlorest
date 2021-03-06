"""Class to sprites for Decorations world."""

# & /Imports decorations\ & #
# ------ Game variables ------ #
from variáveis import B_SPRITE_TSCALING, B_SPRITE_SIZE
from variáveis import D_SPRITE_ROCK, D_COPYTIGHT
# ------ Window modules ------ #
from módulos.Objeto import Object_sprite
# & \Imports decorations/ & #


# Sprites -- Decoration __ BR, CCo
class Big_rock(Object_sprite):
    """Sprite | Starting stone."""

    def __init__(self, pos, diretorio):
        """Variables to starting stone."""
        super().__init__(pos[0], pos[1])

        self.scale: float = B_SPRITE_TSCALING

        # Add texture
        self.set_sprite(self.sprite_loc(diretorio, D_SPRITE_ROCK))

        self.set_pos(B_SPRITE_SIZE)

    def move(self, vel):
        """Move stone out of the window."""
        if self.center_x <= 500:
            self.center_x += vel


class Clas_copyright(Object_sprite):
    """Sprite | Copyright for game."""

    def __init__(self, pos, diretorio):
        """Variables for sprite copyright."""
        super().__init__(pos[0], pos[1])

        self.scale: float = B_SPRITE_TSCALING-3
        self.at_alpha: int = 0

        # Add texture
        self.set_sprite(self.sprite_loc(diretorio, D_COPYTIGHT))

        self.set_pos(B_SPRITE_SIZE)
