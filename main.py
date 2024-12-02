import sys
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QAction

from utils import get_idle_time, create_tray_icon, get_display_info
from media_detector import MediaDetector
from ui_components import BlackScreen, SettingsDialog
from settings_manager import SettingsManager

class ScreenDimmer:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.screens = QApplication.screens()
        
        # Initialize settings manager
        self.settings_manager = SettingsManager()
        
        # Create settings dialog with settings manager
        self.settings_dialog = SettingsDialog(self.screens, self.settings_manager)
        
        self.black_screen = None
        self.manual_mode = False
        self.update_black_screen()
        
        # Setup tray icon
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(create_tray_icon())
        self.menu = QMenu()
        self.setup_menu()
        self.tray.setContextMenu(self.menu)
        self.tray.setVisible(True)
        
        # Setup timers and detectors
        self.idle_timer = QTimer()
        self.idle_timer.timeout.connect(self.check_idle)
        self.idle_timer.start(1000)
        
        self.media_detector = MediaDetector()
        self.media_detector.media_detected.connect(self.on_media_detected)
        self.media_detector.start()
        
        # State tracking
        self.is_active = False
        self.media_playing = False
        self.timer_enabled = self.settings_manager.get("timer_enabled", True)
        
        self.settings_dialog.monitor_combo.currentIndexChanged.connect(self.update_black_screen)
    
    def update_black_screen(self):
        displays = get_display_info()  # Add import at top of file if needed
        selected_index = self.settings_dialog.get_selected_monitor_index()
        
        if selected_index < len(displays):
            selected_display = displays[selected_index]
            if self.black_screen:
                was_visible = self.black_screen.isVisible()
                self.black_screen.hide()
                self.black_screen.deleteLater()
                self.black_screen = BlackScreen(selected_display, self)
                if was_visible:
                    self.black_screen.show()
            else:
                self.black_screen = BlackScreen(selected_display, self)
    
    def setup_menu(self):
        toggle_action = QAction("Toggle Screen", self.menu)
        toggle_action.triggered.connect(self.manual_toggle)
        
        settings_action = QAction("Settings", self.menu)
        settings_action.triggered.connect(self.settings_dialog.show)
        
        timer_action = QAction("Enable Timer", self.menu)
        timer_action.setCheckable(True)
        timer_action.setChecked(self.settings_manager.get("timer_enabled", True))
        timer_action.triggered.connect(self.toggle_timer)
        
        quit_action = QAction("Quit", self.menu)
        quit_action.triggered.connect(self.quit_app)
        
        self.menu.addAction(toggle_action)
        self.menu.addAction(timer_action)
        self.menu.addAction(settings_action)
        self.menu.addSeparator()
        self.menu.addAction(quit_action)
    
    def manual_toggle(self):
        if self.black_screen.isVisible():
            self.black_screen.hide()
            self.is_active = False
            self.manual_mode = False
        else:
            self.black_screen.show()
            self.black_screen.activateWindow()
            self.is_active = True
            self.manual_mode = True
    
    def toggle_timer(self, enabled=None):
        if isinstance(enabled, bool):
            self.timer_enabled = enabled
            self.settings_manager.set("timer_enabled", enabled)
            return
            
        if not self.media_playing and not self.manual_mode:
            if not self.black_screen.isVisible():
                self.black_screen.show()
                self.black_screen.activateWindow()
                self.is_active = True
                self.manual_mode = False
    
    def check_idle(self):
        if not self.timer_enabled or self.manual_mode:
            return
            
        idle_time = get_idle_time()
        timeout = self.settings_dialog.timeout_spinbox.value() * 60
        
        if idle_time > timeout and not self.is_active and not self.media_playing:
            self.toggle_timer()
        elif idle_time < 1 and self.is_active and not self.manual_mode:
            self.black_screen.hide()
            self.is_active = False
    
    def on_media_detected(self, detected):
        self.media_playing = detected
        if detected and self.is_active and not self.manual_mode:
            self.black_screen.hide()
            self.is_active = False
    
    def quit_app(self):
        self.media_detector.stop()
        self.media_detector.wait()
        self.app.quit()
    
    def run(self):
        return self.app.exec()

if __name__ == "__main__":
    dimmer = ScreenDimmer()
    sys.exit(dimmer.run())