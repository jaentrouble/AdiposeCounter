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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='AdiposeCounter2.1.2',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='icon.ico')
