import ctypes
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt

class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [
        ('cbSize', ctypes.c_uint),
        ('dwTime', ctypes.c_uint),
    ]

def get_idle_time():
    """Get system idle time in seconds"""
    lastInputInfo = LASTINPUTINFO()
    lastInputInfo.cbSize = ctypes.sizeof(lastInputInfo)
    ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lastInputInfo))
    millis = ctypes.windll.kernel32.GetTickCount() - lastInputInfo.dwTime
    return millis / 1000.0

def create_tray_icon():
    """Create a basic white icon for the system tray"""
    pixmap = QPixmap(16, 16)
    pixmap.fill(Qt.GlobalColor.white)
    return QIcon(pixmap)