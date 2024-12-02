# OLED Blanker <img src="https://i.imgur.com/G2BG9CF.png" width="40">
A system tray application designed to blank OLED displays on Windows without DDC/CI or other hardware tools. Built with Python and Qt6.

## Features
- System tray controls for quick access
- Monitor-specific blanking (supports multi-monitor setups)
- Automatic screen blanking after user-defined idle time
- Media playback detection (prevents blanking during media playback)
- Manual screen blanking option

## Requirements
```
pip install PyQt6 winsdk
```

## Usage
Run the script:
```
python main.py
```

The application will appear in your system tray. Right-click the tray icon to access:
- Toggle Screen: Manually blank/unblank the selected monitor
- Enable Timer: Toggle automatic blanking
- Settings: Configure monitor selection and idle timeout
- Quit: Exit the application

### Controls
- Click anywhere on the blanked screen to exit manual blanking mode
- Movement or media playback will automatically unblank the screen in timer mode
- Manual blanking can only be disabled by clicking the screen

## Configuration

Settings are automatically saved to `settings.json` in the script directory and include:
- Selected monitor
- Idle timeout duration
- Timer enabled/disabled state
