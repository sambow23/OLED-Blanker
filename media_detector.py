import asyncio
from PyQt6.QtCore import QThread, pyqtSignal
import winsdk.windows.media.control as media_control

class MediaDetector(QThread):
    media_detected = pyqtSignal(bool)
    
    def __init__(self):
        super().__init__()
        self.running = True
        
    async def get_media_playing(self) -> bool:
        try:
            sessions = await media_control.GlobalSystemMediaTransportControlsSessionManager.request_async()
            current_session = sessions.get_current_session()
            if current_session:
                info = await current_session.try_get_media_properties_async()
                playback_info = current_session.get_playback_info()
                if playback_info.playback_status == media_control.GlobalSystemMediaTransportControlsSessionPlaybackStatus.PLAYING:
                    return True
            return False
        except Exception:
            return False

    def run(self):
        while self.running:
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                is_playing = loop.run_until_complete(self.get_media_playing())
                loop.close()
                
                self.media_detected.emit(is_playing)
            except Exception as e:
                print(f"Media detection error: {e}")
            
            self.msleep(1000)  # Check every second
            
    def stop(self):
        self.running = False