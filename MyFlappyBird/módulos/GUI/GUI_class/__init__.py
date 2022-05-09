"""Class to GUI/HUD world."""

# & /Imports GUI\ & #
# ------ General defs ------ #
from arcade import Sprite
from arcade import draw_text, color
# ------ Window modules ------ #
from módulos.GUI.GUI_Objects import *
# & \Imports GUI/ & #


# General GUI -- GUI __ GW
class GUI_world:
    """GUI World settings."""

    __slots__ = ('GUI_manager', 'game_mode', 'backfore',
                 '_Score_endpoints', 'GUI_menu', 'GUI_defeat',
                 'GUI_closets', 'v_box', 'GUI_buttons', 'GUI')

    def __init__(self, game_mode, backfore, diretorio, window):
        """GUI variables/HUD."""
        from arcade import SpriteList
        from arcade.gui import UIManager, UIBoxLayout

        # --- UI
        self.GUI_manager = UIManager()
        self.GUI_manager.enable()

        self.game_mode = game_mode
        self.Score_endpoints = 0
        self.backfore = backfore

        # -- Groups GUI
        # Start Game
        self.GUI_menu, self.GUI_defeat = SpriteList(), SpriteList()
        self.GUI_closets = SpriteList()

        # Create a vertical BoxGroup to align buttons
        self.v_box = UIBoxLayout(vertical=False)

        # -- Sprites, Buttons
        self.GUI_buttons = self.set_buttons()
        self.GUI = self.set_gui(diretorio)

        self.buttons(window)
        # --

    # GUI __ Settings
    def buttons(self, window):
        """Create buttons Exit/Restart for window."""
        from arcade.gui import UIAnchorWidget

        self.add_view_buttons(
            window, self.GUI_buttons['exit_buttom'], self.GUI_buttons['restart_button'])

        # Create a widget to hold the v_box widget, that will center the buttons
        self.GUI_manager.add(
            UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="top",
                child=self.v_box)
        )

    def set_buttons(self) -> dict:
        """Return buttions in to viewport lose."""
        # Create the buttons
        from arcade.gui import UIFlatButton

        return {'exit_buttom': UIFlatButton(text="Exit", width=70, height=42),
                'restart_button': UIFlatButton(text="Restart", width=120, height=42)}

    def add_view_buttons(self, window, exit, restart):
        """Add buttions in to viewport lose."""
        # Add to viewport buttons
        self.v_box.add(
            exit.with_space_around(right=20, top=241, left=34))
        self.v_box.add(
            restart.with_space_around(right=20, top=241, left=-13.5))

        self.buttons_events(
            exit, restart, window)

    def buttons_events(self, exit, restart, window):
        """Events and actions to buttons, Exit/Restart."""
        from arcade import exit as arcade_exit

        @exit.event("on_click")
        def on_click_exit(event):
            arcade_exit()

        @restart.event("on_click")
        def on_click_restart(event):
            window.setup()

    def set_gui(self, diretorio: str) -> dict:
        """Create all GUI variables."""
        return {'DERROTA': Defeat((3.6, 11.5), diretorio),
                'MENU_restart': Menu_restart((3.6, 8.26), diretorio),
                'PT_placar': Points_score((0.75, 12.26), diretorio),
                'PT_lose': Scoreboard_menu((7, 9.52), diretorio),
                'PT': Score((1.47, 12.24), diretorio),
                'PT_at1': Score((1.1, 12.45), diretorio, 2.3),
                'PT_at2':  Score((0.92, 12.45), diretorio, 2.3)}

    def append_tiles(self):
        """Add GUI for screen."""
        # -$ Sprite group $-

        # -- Set GUI_loser sprites -- #
        self.GUI_defeat.append(self.GUI['DERROTA'])
        self.GUI_defeat.append(self.GUI['MENU_restart'])
        self.GUI_defeat.append(self.GUI['PT_lose'])

        # -- Set GUI score_points - PT = POINT -- #
        self.GUI_closets.append(self.GUI['PT_placar'])

        self.GUI_closets.append(self.GUI['PT'])
        self.GUI_closets.append(self.GUI['PT_at1'])
        self.GUI_closets.append(self.GUI['PT_at2'])

    def add_score(self, collision: Sprite,
                  bird: Sprite, diretorio: str,
                  add_score: list[int],
                  current_score: bool) -> bool:
        """Sets and adds the points on the scoreboard."""

        if not collision.center_x >= bird.center_x <= collision.center_x or not current_score:
            return collision.center_x <= bird.center_x
        add_score[0] += 1
        self.backfore.tronco_speed[0] += 5
        self.Score_endpoints += 1

        if add_score[0] > 9:
            add_score[1] += 1
            self.GUI['PT_at2'].set_sprite_number(
                diretorio, add_score[1])
            add_score[0] = 0

        self.GUI['PT'].set_sprite_number(
            diretorio, add_score[0])

    def draw(self):
        """Draw GUI in screen."""
        def draw_points(x, y):
            draw_text(f"{self.Score_endpoints}",
                      x, y,
                      color.BROWN_NOSE, 10.5,
                      font_name="Kenney Blocks")
        self.GUI_menu.draw(pixelated=True)

        if self.game_mode == 'Morte':
            self.GUI_manager.draw()
            self.GUI_defeat.draw(pixelated=True)

            if self.Score_endpoints <= 9:
                draw_points(372, 482)
            elif self.Score_endpoints <= 99:
                draw_points(367, 482)
            elif self.Score_endpoints <= 999:
                draw_points(361.5, 482)

        elif self.game_mode in ('Gameplay', 'Tela_Inicial'):
            self.GUI_closets.draw(pixelated=True)

    # GUI __ property's
    @property
    def Score_endpoints(self):
        """Return points table."""
        return self._Score_endpoints

    @Score_endpoints.setter
    def Score_endpoints(self, endpoints):
        if isinstance(endpoints, int) and endpoints < 0:
            self._Score_endpoints = abs(endpoints)
        elif isinstance(endpoints, str) and endpoints.isnumeric():
            self._Score_endpoints = int(endpoints)
        else:
            self._Score_endpoints = endpoints
