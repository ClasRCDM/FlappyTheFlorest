"""Class to objects for GUI"""

# & /Imports objects for GUI\ & #
# ------ General defs ------ #
from arcade import View, draw_rectangle_filled
from arcade import run, Window

from os import path, getcwd
# ------ Game variables ------ #
from variáveis import W_LARGURA, W_ALTURA, W_TÍTULOS
from variáveis import FADE_RATE, ARQUIVO

from variáveis import GD_SPRITE, GM_RESTART, GP_SCORE
from variáveis import GP_SCOREBOARD_lose, GP_SCOREBOARD
from variáveis import B_SPRITE_TSCALING, B_SPRITE_SIZE
# ------ Window modules ------ #
from módulos.Objeto import Object_sprite
# & \Imports objects for GUI/ & #


# Sprites -- GUI __ DF, MR, PS, S, SBM
class Defeat(Object_sprite):
    def __init__(self, pos, diretorio):
        super().__init__(pos[0], pos[1])

        self.scale: float = B_SPRITE_TSCALING

        # Add texture
        self.set_sprite(self.sprite_loc(diretorio, GD_SPRITE))

        self.set_pos(B_SPRITE_SIZE)


class Menu_restart(Object_sprite):
    def __init__(self, pos, diretorio):
        super().__init__(pos[0], pos[1])

        self.scale: float = B_SPRITE_TSCALING

        # Add texture
        self.set_sprite(self.sprite_loc(diretorio, GM_RESTART))

        self.set_pos(B_SPRITE_SIZE)


class Points_score(Object_sprite):
    def __init__(self, pos, diretorio):
        super().__init__(pos[0], pos[1])

        self.scale: float = B_SPRITE_TSCALING

        # Add texture
        self.set_sprite(self.sprite_loc(diretorio, GP_SCOREBOARD))

        self.set_pos(B_SPRITE_SIZE)


class Score(Object_sprite):
    def __init__(self, pos, diretorio, size=0):
        super().__init__(pos[0], pos[1])

        self.scale: float = B_SPRITE_TSCALING-size

        # -- Numbers
        self.numbers: str = GP_SCORE

        # Add texture
        self.set_sprite(self.sprite_loc(
            diretorio, self.numbers[0]))

        self.set_pos(B_SPRITE_SIZE)

    def set_sprite_number(self, diretorio, index):
        self.set_sprite(self.sprite_loc(
            diretorio, self.numbers[index]))


class Scoreboard_menu(Object_sprite):
    def __init__(self, pos, diretorio):
        super().__init__(pos[0], pos[1])

        self.scale: float = B_SPRITE_TSCALING

        # Add texture
        self.set_sprite(self.sprite_loc(diretorio, GP_SCOREBOARD_lose))

        self.set_pos(B_SPRITE_SIZE)


# Window -- GUI __ FV, SW
class FadingView(View):
    """ View transition """
    diretorio: str = path.join(getcwd(), ARQUIVO)

    def __init__(self):
        super().__init__()
        self.fade_out = None
        self.fade_in = 255

    def update_fade(self, next_view=None):
        if self.fade_out is not None:
            self.fade_out += FADE_RATE
        if self.fade_out is not None and self.fade_out > 255 and next_view is not None:
            game_view = next_view()
            game_view.setup()
            self.window.show_view(game_view)

        if self.fade_in is not None:
            self.fade_in -= FADE_RATE
            if self.fade_in <= 0: self.fade_in = None

    def draw_fading(self, fade):
        draw_rectangle_filled(self.window.width / 2, self.window.height / 2,
                              self.window.width, self.window.height,
                              (0, 0, 0, fade))

    def draw_fadings(self):
        if self.fade_out is not None:
            self.draw_fading(self.fade_out)
        elif self.fade_in is not None:
            self.draw_fading(self.fade_in)


# -- DEFs -- #
def Set_window(modulo):
    """ Create window """
    window = Window(W_LARGURA, W_ALTURA, W_TÍTULOS)

    # Start the module and add it to the window
    init = modulo()
    window.show_view(init)
    init.setup()

    run()
