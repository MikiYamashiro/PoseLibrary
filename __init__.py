from . import gui
from . import Define
from maya import cmds


def run():
    if cmds.window(Define.WINDOW_NAME, ex=1):
        cmds.deleteUI(Define.WINDOW_NAME)
    ui = gui.GUI()
    ui.show()


