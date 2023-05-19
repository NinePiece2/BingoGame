import cx_Freeze
import sys

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [cx_Freeze.Executable("sources/main.py", base=base, shortcutName="Bingo", targetName="Bingo.exe")]

cx_Freeze.setup(
    name="Bingo",
    options={"build_exe": {"packages":["pygame", "random", "datetime", "base64", "json", "tkinter", "os", "shutil"],
                           "include_files":["sources/resources/bingo_icon.bmp"]}},
    executables = executables

)