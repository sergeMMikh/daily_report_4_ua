from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules

root = Path(SPECPATH)
a = Analysis(
    [str(root / "app.py")],
    pathex=[str(root)],
    binaries=[],
    datas=[(str(root / "templates"), "templates")],
    hiddenimports=collect_submodules("openai") + ["tzdata"],
    hookspath=[], runtime_hooks=[], excludes=["tkinter", "django"], noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, a.binaries, a.datas, [], name="DailyReport", debug=False,
          bootloader_ignore_signals=False, strip=False, upx=False, console=False)
