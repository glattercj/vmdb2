# -*- mode: python -*-

# 1) apt install python3-pip python3-yaml python3-jinja2 python3-cliapp
# **NOT IN PYENV***
# 2) pip install pyinstaller
# 3) pyinstaller vmdb2.spec

block_cipher = None


a = Analysis(['vmdb2'],
             pathex=[],
             binaries=[],
             datas=[('vmdb', 'vmdb'), ('vmdb/plugins', 'vmdb/plugins')],
             hiddenimports=[],
             hookspath=[],
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
          name='vmdb2',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
