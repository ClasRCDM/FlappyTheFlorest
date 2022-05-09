"""
Name: FlappyBird: The Forest!.

Description: ->
A Flappy Bird where the objective is to pick up fruits
and go through the logs and reach as many points as possible. <-

Author: Clas_RCDM
Email: raphaelcalixto2013@gmail.com
Created from: Ainda não terminado

Python: 3.10.4
Librays versions: Arcade - 2.6.13
                  Numpy - all_versions

Copyright: (c) Clas_RCDM
"""

###################
#  Init my World  #
###################

from FlappyBirdTheForest import Jogo
from módulos.GUI.GUI_Objects import Set_window

if __name__ == '__main__':
    Set_window(Jogo)
