"""
蓝白金键盘桌宠
功能：
  1. 中文形态：女孩形象；英文形态：神兽动物形象（按 Shift 切换）
  2. 按下键盘任意按键 → 播放抬手→抬高→下落→触键 4帧敲击动画
  3. 停止按键 2 秒后自动回到待机姿势
  4. 鼠标左键可拖动桌宠位置
  5. 窗口置顶、无边框、透明背景
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap, QMouseEvent
from PyQt5.QtCore import Qt, QTimer

# ====================== 图片路径配置 ======================
def resource_path(relative_path):
    """获取资源文件路径（兼容开发模式和 PyInstaller 打包模式）"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller 打包后，资源解压到临时目录
        base_path = sys._MEIPASS
    else:
        # 开发模式，脚本所在目录
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

IMG_DIR = resource_path("images")

# 女孩（中文形态）
GIRL_IDLE = os.path.join(IMG_DIR, "girl_idle.png")
GIRL_FRAMES = [
    os.path.join(IMG_DIR, "girl_type_01.png"),
    os.path.join(IMG_DIR, "girl_type_02.png"),
    os.path.join(IMG_DIR, "girl_type_03.png"),
    os.path.join(IMG_DIR, "girl_type_04.png"),
]

# 神兽动物（英文形态）
ANIMAL_IDLE = os.path.join(IMG_DIR, "animal_idle.png")
ANIMAL_FRAMES = [
    os.path.join(IMG_DIR, "animal_type_01.png"),
    os.path.join(IMG_DIR, "animal_type_02.png"),
    os.path.join(IMG_DIR, "animal_type_03.png"),
    os.path.join(IMG_DIR, "animal_type_04.png"),
]

IDLE_DELAY = 2000  # 停止按键后回到待机的时间（毫秒）
WINDOW_SIZE = 450  # 窗口大小（像素）
# ============================================================


class KeyboardPet(QWidget):
    def __init__(self):
        super().__init__()

        # 窗口属性：置顶、无边框、工具窗口（不占任务栏）
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint
            | Qt.FramelessWindowHint
            | Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(WINDOW_SIZE, WINDOW_SIZE)

        # 图片显示标签
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.resize(self.size())

        # 状态变量
        self.mode = "chinese"       # chinese / english
        self.frame_idx = 0
        self.drag_pos = None

        # 加载女孩图片
        self.girl_idle_img = QPixmap(GIRL_IDLE)
        self.girl_anim = [QPixmap(p) for p in GIRL_FRAMES]

        # 加载动物图片
        self.animal_idle_img = QPixmap(ANIMAL_IDLE)
        self.animal_anim = [QPixmap(p) for p in ANIMAL_FRAMES]

        # 回到待机的定时器（单次触发）
        self.return_idle_timer = QTimer()
        self.return_idle_timer.setSingleShot(True)
        self.return_idle_timer.timeout.connect(self.set_idle)

        # 初始显示待机图
        self.set_idle()
        self.show()

    def set_idle(self):
        """切换到待机画面"""
        if self.mode == "chinese":
            self.set_pix(self.girl_idle_img)
        else:
            self.set_pix(self.animal_idle_img)
        self.frame_idx = 0

    def set_pix(self, pixmap):
        """缩放并显示图片"""
        scaled = pixmap.scaled(
            self.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.label.setPixmap(scaled)

    def play_type_anim(self):
        """播放抬手敲击动画：按一次键前进一帧"""
        if self.mode == "chinese":
            frame_list = self.girl_anim
        else:
            frame_list = self.animal_anim

        self.set_pix(frame_list[self.frame_idx])
        self.frame_idx = (self.frame_idx + 1) % len(frame_list)
        self.return_idle_timer.start(IDLE_DELAY)

    def switch_mode(self):
        """切换女孩 / 动物形态"""
        self.mode = "english" if self.mode == "chinese" else "chinese"
        self.set_idle()

    def keyPressEvent(self, event):
        """键盘按下事件"""
        if event.key() == Qt.Key_Shift:
            self.switch_mode()
        else:
            self.play_type_anim()
        super().keyPressEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        """鼠标按下，准备拖动"""
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        """鼠标移动，拖动窗口"""
        if self.drag_pos:
            self.move(event.globalPos() - self.drag_pos)
            event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = KeyboardPet()
    sys.exit(app.exec_())
