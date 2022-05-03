"""Global constants file"""

# -----------------------------------#
# /absolute variables of the world\ #
W_ALTURA, W_LARGURA = 700, 400
TELA_CHEIA: tuple[int, int] = W_ALTURA, W_LARGURA
W_TÍTULOS: str = 'Flappy: The Forest!!'

W_GRAVIDADE: int | float = 1500

ARQUIVO: str = 'MyFlappyBird'
def TEXTURAS(a): return f'texturas/{a}/'


FADE_RATE = 3
DEFAULT_DAMPING: float = 1.0
# \absolute variables of the world/ #
# -----------------------------------#

# ____________________#
# /global variables\ #

# $ Bird $ ## --- B --- #
B_SPRITE_ISIZE: int | float = 13
B_SPRITE_PSCALING = B_SPRITE_TSCALING = 3.9
B_DAMPING: float | int = 0.4
B_FRICTION: float | int = 1.0
B_MASSA: float | int = 1.96
B_JUMP_IMPULSE: int | float = 1700
B_MAXH_SPEED: int | float = 450
B_MAXV_SPEED: int | float = 1200
B_MAXC_ROTAÇÃO, B_MAXB_ROTAÇÃO = -45, 45
B_ANIMFLY_SPEED, B_SET_ANGULO = 0.38, 6
B_SPRITE_SIZE = int(B_SPRITE_ISIZE * B_SPRITE_PSCALING)

# $ Background $ #
# --- F = Fundo/Background --- #
F_SPRITE_ISIZE: int | float = 13
F_SPRITE_PSCALING = F_SPRITE_TSCALING = 4.0
F_SPRITE_SIZE = int(F_SPRITE_ISIZE * F_SPRITE_PSCALING)

# $ Forest Background $ #
# --- PF = Parallax Forest --- #
PF_MAX_HORIZONTAL: float | int = 1100
PF_PONTO_DE_VOLTA: float | int = -1459
ARQUIVO_BACKGROUND: str = TEXTURAS('background') + 'background'
PF_SEQUENCIA_SPRITES: tuple = 3, 4, 2, 5, 1
PF_SEQUENCIA_SSPEED: tuple = 1.8, 1, 0.3, 0.3, 1.2

# $ Obstacles Foreground $ #
# --- O = Obstacles --- #
O_SPRITE_ISIZE: int | float = 1
O_SPRITE_PSCALING = O_SPRITE_TSCALING = 3.5
O_SPRITE_SIZE = int(O_SPRITE_ISIZE * O_SPRITE_PSCALING)
ARQUIVO_OBSTACLES: str = TEXTURAS('obstacles')
O_MAX_HORIZONTAL: int | float = 600
O_BOXCOLLISION: str = TEXTURAS('obstacles') + 'colisão_passar_tronco.png'

# $ Water $ ## --- WA --- #
WA_ARQUIVO: str = TEXTURAS('background') + 'effect_water.png'

# $ Decorations $ ## --- D --- #
D_SPRITE_ROCK: str = TEXTURAS('decorations') + 'Pedra_grande_Placa.png'
D_COPYTIGHT: str = TEXTURAS('decorations') + 'Copyright.png'


# % Effects % # -----------------------------------------
# --- E --- #

# $ Leaves $ ## --- L --- #
EL_SPRITE_LEAVES: list = [
    TEXTURAS('effects') + f'Leaves/Leave_{num}.png' for num in range(5)]
EL_LEAVES_POS: list = [(7, 11), (4, 12), (2, 13.5), (0, 11), (6.5, 13)]

# $ Dust to init jump $ #
# --- DJ = dust jump --- #
EDJ_SPRITE: list = [
    TEXTURAS('effects') + f'dustjump/FX052_{num+1}.png' for num in range(5)]


# % GUI % # -------------------------------------------
# --- G --- #

# $ Defeat $ ## --- D --- #
GD_SPRITE: str = TEXTURAS('GUI') + 'derrota.png'

# $ Menu $ ## --- M --- #
GM_RESTART: str = TEXTURAS('GUI') + 'menu_defeat.png'

# $ Placar $ ## --- P --- #
GP_SCOREBOARD: str = TEXTURAS('GUI') + 'placar.png'
GP_SCORE: list = [
    TEXTURAS('GUI') + f'números/pf_{num}.png' for num in range(10)]
GP_SCOREBOARD_lose: str = TEXTURAS('GUI') + 'menu_scoreboard.png'
