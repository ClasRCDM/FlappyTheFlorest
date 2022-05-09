"""Main program file the FlappyBirdTheForest."""

# & /Imports World\ & #
# ------ General defs ------ #
from arcade import Sprite, SpriteList
from arcade import PymunkPhysicsEngine, key
from arcade import set_background_color, csscolor

from typing import Optional
# ------ Game variables ------ #
from variáveis import DEFAULT_DAMPING, W_GRAVIDADE
# ------ Window modules ------ #
from módulos.Pássaro import Bird
from módulos.FundoFrente import Tiled_world
from módulos.Decorações import Clas_copyright

from módulos.GUI.GUI_class import GUI_world
from módulos.GUI.GUI_Objects import FadingView
# & \Imports World/ & #


########################
# Configuring my World #
########################

class Jogo(FadingView):
    """Main class of the game."""

    __slots__ = ('Score', 'Score_can', 'GUI',
                 'backfore', 'physics_engine',
                 'pássaro', 'pássaro_lista', 'pássaro_pulo')

    def __init__(self):
        """Jogo init function."""
        super().__init__()
        # arcade.enable_timings()  # habilitar quando for ver o fps

        # Janela/Windows
        set_background_color(csscolor.BLACK)

        # Game
        self.Modo_jogo: str

        # Scoreboard
        self.Score: list[int]
        self.Score_can: bool

        # Pássaro/Bird
        self.pássaro: Optional[Sprite] = None
        self.pássaro_lista: Optional[SpriteList] = None
        self.pássaro_pulo: bool

        # Tiled/GUI
        self.backfore = self.GUI = None

        # Physics engine
        self.physics_engine: Optional[PymunkPhysicsEngine] = None

    # World __ Settings
    def setup(self):
        """Inicia o jogo. E caso seja chamado o reinicia."""
        self.Modo_jogo: str = 'Tela_Inicial'
        self.pássaro_pulo: bool = True

        # Points score
        self.Score_points: list = [0, 0]
        self.Score_can: bool = True

        # Tile
        self.backfore = Tiled_world(self.diretorio)

        # GUI
        self.GUI = GUI_world(self.Modo_jogo, self.backfore, self.diretorio, self)

        # Grupo/Sprite do pássaro/Bird
        self.pássaro_lista = SpriteList()
        self.pássaro = Bird((3.5, 6.1), self.diretorio, self.Modo_jogo)

        # --- Pymunk Physics Engine Setup --- #
        damping = DEFAULT_DAMPING
        gravity = (0, -W_GRAVIDADE)

        self.physics_world = PymunkPhysicsEngine(
            damping=damping, gravity=gravity)
        self.physics_leave = PymunkPhysicsEngine(
            damping=damping, gravity=(0, -100))

        # == Add Sprites
        # - Backgrounds_
        self.backfore.append_tiles(self.diretorio, self.physics_leave)
        # -- Bird_
        self.pássaro_lista.append(self.pássaro)
        # --- GUI_
        self.GUI.append_tiles()

        # %__ Physics __$ #
        self.pássaro.set_física(self.physics_world)  # For Bird
        self.backfore.set_física(self.physics_world)  # For Obstacles

        # %__ Physics/Collision response to obstacle __$ #
        def wall_collid(sprite, _wall_sprite, _arbiter, _space, _data):
            """Call for Player/Wall collision."""
            if self.pássaro_pulo and self.Modo_jogo != 'Morte':
                self.pássaro_pulo, self.Modo_jogo = False, 'Morte'

        # Add response physics
        self.physics_world.add_collision_handler(
            "player", "wall", post_handler=wall_collid)

    def on_draw(self):
        """Renderisa tudo que a na tela."""
        self.clear()

        # Draw tiles
        self.backfore.draw()
        self.GUI.draw()

        self.pássaro_lista.draw(pixelated=True)
        self.draw_fadings()

    def on_update(self, delta_time):
        """Movimentos e lógicas do jogo."""
        self.update_fade(next_view=Copyright)

        self.pássaro.update()
        self.GUI.game_mode = self.Modo_jogo

        if self.Modo_jogo in 'Gameplay' and not self.pássaro.check_windowpos():
            self.physics_world.step()
            self.backfore.update_movs(self.physics_world)

            self.Score_can = \
                self.GUI.add_score(self.backfore.tile['Obstacles']['layer_collision'],
                                   self.pássaro, self.diretorio,
                                   self.Score_points, self.Score_can)

        elif self.Modo_jogo != 'Tela_Inicial':
            self.Modo_jogo = 'Morte'
            self.physics_world.step()

            self.backfore.move_obstacles(self.physics_world, (1, 0))

        self.physics_leave.step()
        # print(arcade.get_fps())  # Get fps

    def on_key_press(self, chave, modifiers):
        """Chama sempre que uma tecla é pressionada."""
        if chave == key.SPACE and self.Modo_jogo not in ('Gameplay', 'Morte'):
            self.Modo_jogo = 'Gameplay'

            self.pássaro.game_mode = self.Modo_jogo
            self.pássaro.frames_texture = 7

            self.backfore.append_after_jump()
            self.pássaro_lista.append(self.pássaro.dash_jump)

        elif self.pássaro_pulo and self.Modo_jogo != 'Morte':
            self.pássaro.pular(chave, self.physics_world)

    # World __ property's
    @property
    def Modo_jogo(self):
        """Return Game Mode."""
        return self._Modo_jogo

    @Modo_jogo.setter
    def Modo_jogo(self, game_mode):
        self._Modo_jogo = game_mode if isinstance(game_mode, str) else 'Tela_Inicial'


class Copyright(FadingView):
    """Show creation details."""

    __slots__ = 'copyright', 'copyright_list'

    def __init__(self):
        """Clas copyright."""
        super().__init__()
        self.window.center_window()

        # Set the window color
        set_background_color((16, 16, 16))

        self.copyright: Optional[Sprite] = None
        self.copyright_list: Optional[SpriteList] = None

    def setup(self):
        """Creation variables."""
        self.copyright = Clas_copyright((3.5, 6.6), self.diretorio)
        self.copyright_list = SpriteList()
        self.copyright_list.append(self.copyright)

    def on_update(self, delta_time):
        """Fade window."""
        self.update_fade(next_view=Jogo)

        if self.fade_out is None and self.fade_in <= 5:
            self.fade_out = 0

    def on_draw(self):
        """Draw copyright."""
        self.clear()

        self.copyright_list.draw()
        self.draw_fadings()

    def on_key_press(self, chave, _modifiers):
        """."""
        self.mode_view(chave)

    def mode_view(self, chave):
        """
        Handle key presses.

        In this case, we'll just count a 'space' as
        game over and advance to the game over view.
        """
        if self.fade_out is None and chave == key.SPACE:
            self.fade_out = 0
