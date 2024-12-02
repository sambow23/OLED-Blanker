import ctypes
from ctypes import windll, c_short, c_ushort, c_ulong, c_char, Structure, POINTER, sizeof
from ctypes.wintypes import BYTE, WORD, DWORD, WCHAR, BOOL, HMONITOR, HDC, RECT, LPARAM
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, QRect

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

# Display Device Structures
class DISPLAY_DEVICE(Structure):
    _fields_ = [
        ('cb', DWORD),
        ('DeviceName', WCHAR * 32),
        ('DeviceString', WCHAR * 128),
        ('StateFlags', DWORD),
        ('DeviceID', WCHAR * 128),
        ('DeviceKey', WCHAR * 128)
    ]

class MONITORINFOEXW(Structure):
    _fields_ = [
        ('cbSize', DWORD),
        ('rcMonitor', RECT),
        ('rcWork', RECT),
        ('dwFlags', DWORD),
        ('szDevice', WCHAR * 32)
    ]

def get_display_info():
    """Get detailed information about all connected displays"""
    displays = []
    
    def monitor_enum_proc(hMonitor, hdcMonitor, lprcMonitor, dwData):
        monitor_info = MONITORINFOEXW()
        monitor_info.cbSize = sizeof(MONITORINFOEXW)
        if windll.user32.GetMonitorInfoW(hMonitor, ctypes.byref(monitor_info)):
            display_device = DISPLAY_DEVICE()
            display_device.cb = sizeof(display_device)
            
            if windll.user32.EnumDisplayDevicesW(monitor_info.szDevice, 0, ctypes.byref(display_device), 0):
                # Extract display number from DeviceName (usually in format \\.\DISPLAY1)
                display_num = ''.join(filter(str.isdigit, monitor_info.szDevice.split('\\')[-1]))
                
                displays.append({
                    'handle': hMonitor,
                    'name': display_device.DeviceString,
                    'is_primary': bool(monitor_info.dwFlags & 0x1),
                    'display_number': display_num,  # Add this
                    'geometry': {
                        'x': lprcMonitor.contents.left,
                        'y': lprcMonitor.contents.top,
                        'width': lprcMonitor.contents.right - lprcMonitor.contents.left,
                        'height': lprcMonitor.contents.bottom - lprcMonitor.contents.top
                    },
                    'device_name': monitor_info.szDevice,
                    'device_id': display_device.DeviceID
                })
        return True

    MonitorEnumProc = ctypes.WINFUNCTYPE(BOOL, HMONITOR, HDC, POINTER(RECT), LPARAM)
    windll.user32.EnumDisplayMonitors(None, None, MonitorEnumProc(monitor_enum_proc), 0)
    
    return displays