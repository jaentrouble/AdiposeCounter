# -*- mode: python ; coding: utf-8 -*-

import os
import importlib
block_cipher = None


a = Analysis(['Test.py'],
             pathex=['C:\\Users\\vlffl\\Documents\\GitHub\\AdiposeCounter'],
             binaries=[],
             datas=[(os.path.join(os.path.dirname(importlib.import_module('tensorflow').__file__),
                              "lite/experimental/microfrontend/python/ops/_audio_microfrontend_op.so"),
                 "tensorflow/lite/experimental/microfrontend/python/ops/")],
             hiddenimports=[],
             hookspath=['sources'],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='AdiposeCounter2.2.0-debug',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True , icon='icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='AdiposeCounter2.2.0-debug')
