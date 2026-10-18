import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap, QMouseEvent
from PyQt5.QtCore import Qt, QTimer

# 自动获取资源路径（本地运行 / exe打包运行 兼容）
def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ====================== 图片文件名配置（图片放在images文件夹） ======================
GIRL_IDLE = get_resource_path("images/girl_idle.png")
GIRL_FRAMES = [
    get_resource_path("images/girl_type_01.png"),
    get_resource_path("images/girl_type_02.png"),
    get_resource_path("images/girl_type_03.png"),
    get_resource_path("images/girl_type_04.png"),
]

ANIMAL_IDLE = get_resource_path("images/animal_idle.png")
ANIMAL_FRAMES = [
    get_resource_path("images/animal_type_01.png"),
    get_resource_path("images/animal_type_02.png"),
    get_resource_path("images/animal_type_03.png"),
    get_resource_path("images/animal_type_04.png"),
]

IDLE_DELAY = 2000
# ============================================================

class KeyboardPet(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint
            | Qt.FramelessWindowHint
            | Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(450, 450)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.resize(self.size())

        self.mode = "chinese"
        self.frame_idx = 0
        self.drag_pos = None

        self.girl_idle_img = QPixmap(GIRL_IDLE)
        self.girl_anim = [QPixmap(p) for p in GIRL_FRAMES]

        self.animal_idle_img = QPixmap(ANIMAL_IDLE)
        self.animal_anim = [QPixmap(p) for p in ANIMAL_FRAMES]

        self.return_idle_timer = QTimer()
        self.return_idle_timer.setSingleShot(True)
        self.return_idle_timer.timeout.connect(self.set_idle)

        self.set_idle()
        self.show()

    def set_idle(self):
        if self.mode == "chinese":
            self.set_pix(self.girl_idle_img)
        else:
            self.set_pix(self.animal_idle_img)
        self.frame_idx = 0

    def set_pix(self, pixmap):
        scaled = pixmap.scaled(
            self.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.label.setPixmap(scaled)

    def play_type_anim(self):
        if self.mode == "chinese":
            frame_list = self.girl_anim
        else:
            frame_list = self.animal_anim

        self.set_pix(frame_list[self.frame_idx])
        self.frame_idx = (self.frame_idx + 1) % len(frame_list)
        self.return_idle_timer.start(IDLE_DELAY)

    def switch_mode(self):
        if self.mode == "chinese":
            self.mode = "english"
        else:
            self.mode = "chinese"
        self.set_idle()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Shift:
            self.switch_mode()
        else:
            self.play_type_anim()
        super().keyPressEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.drag_pos:
            self.move(event.globalPos() - self.drag_pos)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = KeyboardPet()
    sys.exit(app.exec_())
