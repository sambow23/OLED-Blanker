import os
from pathlib import Path

# Get the absolute path to the project root
PROJ_ROOT = os.getcwd()

block_cipher = None

a = Analysis(
    [os.path.join(PROJ_ROOT, 'main', 'main.py')],  # Main script path
    pathex=[PROJ_ROOT],
    binaries=[],
    datas=[],
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'winsdk.windows.media.control',
        'winsdk.windows.media',
        'winsdk.windows',
        'asyncio',
        'json',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='OLEDBlanker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to True if you want to see console output for debugging
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon=os.path.join(PROJ_ROOT, 'assets', 'icon.ico'),  # Uncomment and add icon path if you have one
)