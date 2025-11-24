import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTabWidget, QLabel, QDockWidget
from PySide6.QtCore import Qt
from panda3d.core import loadPrcFileData
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
import numpy as np

# Correct imports
from src.core.model import FrameModel
from src.core.analysis import run_basic_analysis

# Panda3D config
loadPrcFileData('', 'window-type none')

class PandaViewer(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.setup_scene()
        self.taskMgr.add(self.spin_camera, "spin")

    def setup_scene(self):
        from panda3d.core import LineSegs
        segs = LineSegs()
        segs.setThickness(5)
        segs.setColor(0.8, 0.3, 0.3, 1)

        model = FrameModel().generate_complex_goalpost(num_cols=4, height=4.5)
        for member in model.members:
            start = model.nodes[member.start_node]["pos"]
            end = model.nodes[member.end_node]["pos"]
            segs.moveTo(start[0], start[1], start[2])
            segs.drawTo(end[0], end[1], end[2])
        node = segs.create()
        self.render.attachNewNode(node)

        # Simple ground
        segs = LineSegs()
        segs.setColor(0.5, 0.5, 0.5, 1)
        for x in range(-10, 11, 2):
            segs.moveTo(x, -10, 0)
            segs.drawTo(x, 10, 0)
            segs.moveTo(-10, x, 0)
            segs.drawTo(10, x, 0)
        grid = segs.create()
        self.render.attachNewNode(grid)

        self.camera.setPos(15, -18,