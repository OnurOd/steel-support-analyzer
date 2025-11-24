from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTabWidget, QLabel
from PySide6.QtCore import Qt
from panda3d.core import loadPrcFileData
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from PySide6.QtWidgets import QDockWidget
import sys
sys.path.append('src/core')
from core.model import FrameModel
from core.analysis import run_basic_analysis

# Panda3D config for embed
loadPrcFileData('', 'window-type none')

class PandaViewer(ShowBase):
    def __init__(self, parent):
        ShowBase.__init__(self)
        self.parent = parent
        # Load simple 3D model (we'll add GLTF tomorrow for real channels)
        self.setup_scene()
        self.taskMgr.add(self.spin_camera, "spin")

    def setup_scene(self):
        # Basic goalpost viz (lines for now — full models next)
        from panda3d.core import LineSegs, NodePath
        segs = LineSegs()
        model = FrameModel().generate_complex_goalpost()
        for member in model.members:
            start = model.nodes[member.start_node]["pos"]
            end = model.nodes[member.end_node]["pos"]
            segs.moveTo(start[0], start[1], start[2])
            segs.drawTo(end[0], end[1], end[2])
        node = segs.create()
        np = self.render.attachNewNode(node)
        np.setColor(0.8, 0.2, 0.2, 1)  # Steel red
        self.camera.setPos(10, -10, 5)
        self.camera.lookAt(5, 0, 2)

    def spin_camera(self, task):
        angle = task.time * 10
        self.camera.setPos(10 * np.sin(angle / 100), 10 * np.cos(angle / 100), 5)
        self.camera.lookAt(5, 0, 2)
        return Task.cont

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Steel Support Analyzer - Eurocode Edition")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: #2b2b2b; color: #ffffff;")  # Dark theme

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Tabs
        tabs = QTabWidget()
        layout.addWidget(tabs)

        # 3D Viewer Tab
        viewer_tab = QWidget()
        viewer_layout = QVBoxLayout(viewer_tab)
        self.label = QLabel("Loading 3D model...")
        viewer_layout.addWidget(self.label)
        # Embed Panda3D (simplified — full Qt embed tomorrow)
        self.viewer = PandaViewer(self)
        self.label.setText("3D Viewer Active: Orbit with mouse (complex 4-col support loaded!)")
        tabs.addTab(viewer_tab, "3D Model")

        # Analysis Tab
        analysis_tab = QWidget()
        anal_layout = QVBoxLayout(analysis_tab)
        self.run_button = QLabel("Click to Analyze (Basic PyNite running...)")
        anal_layout.addWidget(self.run_button)
        model = FrameModel().generate_complex_goalpost()
        results = run_basic_analysis(model)
        self.results_label = QLabel(f"Max Deflection: {results['max_deflection']*1000:.2f} mm\nReactions: {results['reactions']}")
        anal_layout.addWidget(self.results_label)
        self.results_label.setStyleSheet("color: green; font-weight: bold;")
        tabs.addTab(analysis_tab, "Analysis")

        # Properties Dock (right side)
        dock = QDockWidget("Properties", self)
        dock_widget = QWidget()
        dock.setWidget(dock_widget)
        prop_layout = QVBoxLayout(dock_widget)
        prop_layout.addWidget(QLabel("Select Member: (Click in 3D tomorrow)"))
        prop_layout.addWidget(QLabel("Section: HEA240 | Material: S355 | Length: 4.0m"))
        self.addDockWidget(Qt.RightDockWidgetArea, dock)

        print("App launched! Check console for model info.")
