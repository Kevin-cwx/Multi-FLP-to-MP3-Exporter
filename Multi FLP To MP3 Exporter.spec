# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Multi FLP To MP3 Exporter.py'],
    pathex=[],
    binaries=[],
    datas=[('Media/Icons', 'Media/Icons')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Multi FLP To MP3 Exporter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='version.txt',
    icon=['C:\\Users\\Kfoen\\Documents\\Docs KF\\MyPythonProjects\\findusic\\Media\\Icons\\FL21 - Icon.ico'],
)
