"""Tiled World class file"""

# & /Imports Tiled World\ & #
# ------ Game variables ------ #
from variáveis import PF_MAX_HORIZONTAL, PF_PONTO_DE_VOLTA
from variáveis import PF_SEQUENCIA_SPRITES, PF_SEQUENCIA_SSPEED
# ------ Window modules ------ #
from módulos.Obstáculos import Obstacles, Box_collision
from módulos.Decorações import Big_rock

from módulos.Parallax import Parallax, Water
from módulos.Parallax import Spawn_leaves, Iterator
# & \Imports Tiled World/ & #


# General Tile -- Tiled World __ TW
class Tiled_world:
    """ Background and Foreground Sprites """

    def __init__(self, diretorio):
        """ Init TiledWorld """
        from arcade import SpriteList

        # Sprites
        self.tile = self.set_tiles(diretorio)

        # -- Group sprites
        # Forest, Forest reflection
        self.tile_floresta, self.tile_reflexo = SpriteList(), SpriteList()
        self.tile_reflexo.alpha_normalized = 0.8

        # Obstacles
        self.tile_obstacles, self.tile_objects = SpriteList(), SpriteList()

        # Effects, Collisions
        self.tile_effects, self.tile_collision = SpriteList(), SpriteList()

    def set_tiles(self, diretorio) -> dict:
        """ Create all tiles """

        # -- Objects -- #
        # -Parallax-
        Parallax = self.tile_parallax(diretorio)

        # -Water/Reflection-
        Water = self.tile_WaterReflection(diretorio)

        # -Collision obstacles-
        Obstacles = self.tile_collobstacles(diretorio)

        # -- GUI -- #
        GUI = self.tile_GUI(diretorio)

        return {'Parallax': Parallax,
                'Water': Water,
                'Obstacles': Obstacles,
                'GUI': GUI}

    def tile_parallax(self, diretorio) -> dict:
        return {'layer_1': self.set_pllx(diretorio, 3.6, 6.4, 2, 'Floresta_Troncos'),
                'layer_1_sheet': self.set_pllx(diretorio, 3.6, 6.4, 2, 'Floresta_Folhas'),
                'layer_2': self.set_pllx(diretorio, 3.4, 6, 1, 'Floresta'),
                'layer_3': self.set_pllx(diretorio, 3.5, 6.8, 0, 'Floresta'),
                'layer_4': self.set_pllx(diretorio, 2.5, 15, 0, 'Lights'),
                'layer_5': self.set_pllx(diretorio, 15, 16.5, 1, 'Lights')}

    def tile_WaterReflection(self, diretorio) -> dict:
        """ Set to sprites Water """
        return {'layer_6': Water(201, 22, 60, 402, diretorio),
                'layer_7': self.set_pllx(diretorio, 3.5, -0.89, 0, 'Reflexo', True),
                'layer_11': self.set_pllx(diretorio, 3.5, -0.89, 0, 'Effect_water', True)}

    def tile_collobstacles(self, diretorio) -> dict:
        """ Set to sprites Obstacles """
        return {'layer_8': Obstacles(-60, 0, diretorio, 0, 'Tronco'),
                'layer_9': Obstacles(-190, 0, diretorio, 1, 'Tronco'),
                'layer_collision': Box_collision((2, 6), diretorio)}

    def tile_GUI(self, diretorio) -> dict:
        """ Set to sprites GUI """
        return {'layer_10': Big_rock((3.3, -0.05), diretorio)}

    def append_tiles(self, diretorio, física):
        """ Add all tiles """

        # -$ Sprite group $-

        # -- Set Parallax sprites -- #
        nuns = Iterator(PF_SEQUENCIA_SPRITES, op=1)
        for index in nuns:
            self.return_parallax(self.tile_floresta, f'layer_{index}')
        self.return_parallax(self.tile_objects, 'layer_1_sheet')

        # -- Add reflection sprites to sprite group
        self.return_sprites(self.tile_reflexo,
                            self.tile['Water']['layer_7']._return,
                            (self.tile['Water']['layer_7'].layer,
                             self.tile['Water']['layer_7'].layer),
                            (0, 1))

        self.return_sprites(self.tile_reflexo,
                            self.tile['Water']['layer_11']._return,
                            (self.tile['Water']['layer_11'].layer,
                             self.tile['Water']['layer_11'].layer),
                            (0, 1))

        # -- Set Obstacles sprites -- #
        self.return_sprites(self.tile_obstacles,
                            self.tile['Obstacles']['layer_8'].return_sprite,
                            (self.tile['Obstacles']['layer_8'].tronco_baixo,
                             self.tile['Obstacles']['layer_8'].tronco_cima))

        self.return_sprites(self.tile_obstacles,
                            self.tile['Obstacles']['layer_9'].return_sprite,
                            (self.tile['Obstacles']['layer_9'].tronco_baixo,
                             self.tile['Obstacles']['layer_9'].tronco_cima))

        # -- Add Objects sprites -- #
        self.tile_objects.append(self.tile['GUI']['layer_10'])
        self.leaves = Spawn_leaves(self.tile['Parallax']['layer_3'].layer.x_y,
                                   diretorio, física)

        # -- EFFECTS -- #
        # First leaves
        self.spawns_leaves()

    def append_after_jump(self):
        """ Add collision point """
        # -- Set collision for Obstacles sprites
        self.tile_collision.append(self.tile['Obstacles']['layer_collision'])

    def update_movs(self, física):
        """ Moving the sprites  """

        nuns = Iterator(PF_SEQUENCIA_SSPEED, op=2)
        for index, speed in nuns:
            self.set_move(f'layer_{index+1}', 'Parallax', speed)
        self.set_move('layer_1_sheet', 'Parallax', PF_SEQUENCIA_SSPEED[0])

        # Water reflection movement
        self.set_move('layer_7', 'Water', 2)
        self.set_move('layer_11', 'Water', 2)

        # Wooden logs movement
        self.tile['Obstacles']['layer_8'].moving(física, (100, 0))
        self.tile['Obstacles']['layer_9'].moving(física, (100, 0))

        if self.tile['Obstacles']['layer_8'].tronco_baixo.center_x < 280:
            self.tile['Obstacles']['layer_collision'].move(
                self.tile['Obstacles']['layer_8'].tronco_baixo.center_x,
                self.tile['Obstacles']['layer_8'].tronco_baixo.center_y+320)
        elif self.tile['Obstacles']['layer_9'].tronco_baixo.center_x < 310:
            self.tile['Obstacles']['layer_collision'].move(
                self.tile['Obstacles']['layer_9'].tronco_baixo.center_x,
                self.tile['Obstacles']['layer_9'].tronco_baixo.center_y+320)

        # moving stone
        self.tile['GUI']['layer_10'].move(PF_SEQUENCIA_SSPEED[0])

        # -- General effects
        self.spawns_leaves()

    def set_move(self, layer, slot, vel):
        """ Move parallax sprite """
        self.tile[slot][layer].update(self.tile[slot][layer].layer, vel)

    def spawns_leaves(self):
        """ Leaf spawn with physics  """

        if len(self.tile_effects) <= 0:
            for effect in self.leaves.generate():
                effect.random_pos()
                self.tile_effects.append(effect)

    def return_parallax(self, tiles, layer):
        """ Set the parallax to the group sprite """

        tiles.append(self.tile['Parallax'][layer]._return(
            0, self.tile['Parallax'][layer].layer))
        tiles.append(self.tile['Parallax'][layer]._return(
            1, self.tile['Parallax'][layer].layer))

    def return_sprites(self, tiles, object1, object2, v=None):
        """ Add sprites to drawing lists """
        if v is None:
            tiles.append(object1(object2[0]))
            tiles.append(object1(object2[1]))
        elif v is not None:
            tiles.append(object1(v[0], object2[0]))
            tiles.append(object1(v[1], object2[1]))

    def set_pllx(self,
                 diretorio,
                 x, y, index,
                 modelo, flip=False) -> Parallax:
        """ Create object Parallax """

        return Parallax(x, y, diretorio, index, modelo,
                        PF_MAX_HORIZONTAL, PF_PONTO_DE_VOLTA, flipp=flip)

    def set_física(self, física):
        """ Create physics for the obstacles """
        from arcade import PymunkPhysicsEngine

        física.add_sprite_list(self.tile_obstacles,
                               friction=0.6,
                               collision_type="wall",
                               body_type=PymunkPhysicsEngine.DYNAMIC)

    def draw(self):
        """ Draw sprites groups """
        self.tile_collision.draw(pixelated=True)

        self.tile_floresta.draw(pixelated=True)
        self.tile['Water']['layer_6'].draw()

        self.tile_effects.draw(pixelated=True)
        self.tile_objects.draw(pixelated=True)

        self.tile_reflexo.draw(pixelated=True)
        self.tile_obstacles.draw(pixelated=True)
