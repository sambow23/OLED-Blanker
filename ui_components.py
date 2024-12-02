from PyQt6.QtWidgets import QWidget, QDialog, QLabel, QSpinBox, QVBoxLayout, QComboBox
from PyQt6.QtCore import Qt

class BlackScreen(QWidget):
    def __init__(self, screen, dimmer):
        super().__init__()
        self.dimmer = dimmer
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        
        self.setStyleSheet("background-color: black;")
        geometry = screen.geometry()
        self.setGeometry(geometry)
        
        self.blank_cursor = Qt.CursorShape.BlankCursor
        
    def showEvent(self, event):
        self.setCursor(self.blank_cursor)
        super().showEvent(event)
        
    def hideEvent(self, event):
        self.unsetCursor()
        super().hideEvent(event)
        
    def mousePressEvent(self, event):
        if not self.dimmer.manual_mode:
            self.hide()
            self.dimmer.is_active = False
        elif self.dimmer.manual_mode:
            if event.button() == Qt.MouseButton.LeftButton:
                self.hide()
                self.dimmer.is_active = False
                self.dimmer.manual_mode = False

class SettingsDialog(QDialog):
    def __init__(self, screens, settings_manager, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Screen Dimmer Settings")
        self.setAttribute(Qt.WidgetAttribute.WA_QuitOnClose, False)
        self.settings_manager = settings_manager
        
        layout = QVBoxLayout()
        
        # Monitor selection
        monitor_label = QLabel("Select Monitor:")
        self.monitor_combo = QComboBox()
        for i, screen in enumerate(screens):
            geometry = screen.geometry()
            self.monitor_combo.addItem(f"Monitor {i+1} ({geometry.width()}x{geometry.height()})")
        
        # Set saved monitor selection
        saved_monitor = self.settings_manager.get("selected_monitor", 0)
        self.monitor_combo.setCurrentIndex(min(saved_monitor, len(screens) - 1))
        
        # Timeout setting
        timeout_label = QLabel("Idle timeout (minutes):")
        self.timeout_spinbox = QSpinBox()
        self.timeout_spinbox.setRange(1, 60)
        
        # Set saved timeout
        saved_timeout = self.settings_manager.get("idle_timeout", 5)
        self.timeout_spinbox.setValue(saved_timeout)
        
        # Connect change events to save settings
        self.monitor_combo.currentIndexChanged.connect(self.save_monitor_setting)
        self.timeout_spinbox.valueChanged.connect(self.save_timeout_setting)
        
        layout.addWidget(monitor_label)
        layout.addWidget(self.monitor_combo)
        layout.addWidget(timeout_label)
        layout.addWidget(self.timeout_spinbox)
        self.setLayout(layout)
    
    def save_monitor_setting(self, index):
        self.settings_manager.set("selected_monitor", index)
    
    def save_timeout_setting(self, value):
        self.settings_manager.set("idle_timeout", value)
        
    def get_selected_monitor_index(self):
        return self.monitor_combo.currentIndex()