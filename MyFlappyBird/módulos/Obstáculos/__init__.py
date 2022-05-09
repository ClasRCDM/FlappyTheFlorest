"""Class to sprites for Obstacles world."""

# & /Imports Obstacles\ & #
# ------ General defs ------ #
from random import randint
from operator import add, sub
# ------ Game variables ------ #
from variáveis import O_SPRITE_SIZE, O_SPRITE_TSCALING, O_BOXCOLLISION
from variáveis import ARQUIVO_OBSTACLES, O_MAX_HORIZONTAL
from variáveis import B_SPRITE_TSCALING, B_SPRITE_SIZE
# ------ Window modules ------ #
from módulos.Objeto import Object, Object_sprite
# & \Imports Obstacles/ & #


# Sprite obstacles -- Obstacles __ OBT, BC
class Obstacles(Object):
    """Obstacle | Trunk to florest."""

    __slots__ = ('opert', 'truck_stt', 'side_truck',
                 'tronco_baixo', 'tronco_cima')

    def __init__(self, x, y,
                 diretorio, index,
                 image):
        """Variables trunk."""
        from arcade import Sprite
        super().__init__(diretorio, ARQUIVO_OBSTACLES)

        self.x, self.y = x, y
        self.image, self.index = image, index

        self.opert = sub if randint(0, 1) == 0 else add
        self.truck_stt = 'cima', 'baixo'
        self.side_truck = 'cima' if self.opert == sub else 'baixo'

        # Conjunto de texturas/Carregando texturas
        self.tronco_baixo = Sprite(
            f"{self.main_path}{self.image}_{self.index}.png",
            hit_box_algorithm='Simple')
        self.tronco_cima = Sprite(
            f"{self.main_path}{self.image}_{self.index}.png",
            hit_box_algorithm='Simple', flipped_vertically=True)

        self.set_size()

    def set_size(self):
        """Define the starting position of the trunks."""
        def pos_troncos(am, y_rand, tronco):
            self.set_location(tronco, O_SPRITE_SIZE,
                              (O_SPRITE_SIZE * self.x + O_SPRITE_SIZE / 2,
                               O_SPRITE_SIZE * self.y+am+y_rand + O_SPRITE_SIZE / 2), v_pro=True)

        # Set pos to trunks
        y_rand = randint(-150, 220)

        pos_troncos(0, y_rand, self.tronco_baixo)
        pos_troncos(640, y_rand, self.tronco_cima)

        self.set_scaling(self.tronco_baixo, O_SPRITE_TSCALING)
        self.set_scaling(self.tronco_cima, O_SPRITE_TSCALING)

    def return_sprite(self, tronco):
        """Return trunk sprite."""
        return tronco

    def loop_movimento(self, física):
        """Loop | Returns them to the top of the screen."""
        y_rand, x_rand = randint(-150, 220), randint(-200, -100)

        self.set_move(x_rand, 0, y_rand, self.tronco_baixo, física)
        self.set_move(x_rand, 650, y_rand, self.tronco_cima, física)

    def set_move(self, x, y, m, tronco, física):
        """Move trunks."""
        if tronco._position[0] >= O_MAX_HORIZONTAL:
            self.opert = sub if randint(0, 1) == 0 else add
            física.set_position(
                tronco, (x, int(O_SPRITE_SIZE * self.y+m+y + O_SPRITE_SIZE / 2)))

    def moving(self, física,
               vel, tronco, m_V=False):
        """Set velocity and Angle/Loop moves."""
        self.loop_movimento(física)

        física.set_velocity(self.tronco_baixo, (vel[0], self.move_v(m_V, vel[1])))
        física.set_velocity(self.tronco_cima, (vel[0], self.move_v(m_V, vel[1])))

        self.tronco_baixo.angle = self.tronco_cima.angle = 0

    def move_v(self, T, v) -> int | float:
        """Move the logs vertically."""
        def set_up_down(opert_C, vt) -> bool:
            if opert_C and self.side_truck == vt: return True
            return False
        if T:
            if set_up_down(870 >= self.tronco_cima.center_y <= 480, self.truck_stt[0]):
                self.opert, self.side_truck = add, self.truck_stt[1]
            elif set_up_down(480 <= self.tronco_cima.center_y >= 870, self.truck_stt[1]):
                self.opert, self.side_truck = sub, self.truck_stt[0]
            return self.opert(v, 50)
        return v


class Box_collision(Object_sprite):
    """Obstacle | Box_collision trunks."""

    def __init__(self, pos, diretorio):
        """Variables Collision."""
        super().__init__(pos[0], pos[1])

        self.scale: float = B_SPRITE_TSCALING

        # Add texture
        self.set_sprite(self.sprite_loc(diretorio, O_BOXCOLLISION))

        self.set_pos(B_SPRITE_SIZE)

    def move(self, x, y):
        """Move along the trunks."""
        self.set_position(x, y)
