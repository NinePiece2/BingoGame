# This script is used to build an executable application from the code
#  as well as an .msi installer that can be used for releases.

import cx_Freeze
import sys
import os

base = None
if sys.platform == "win32":
    base = "Win32GUI"

path = os.path.join(os.environ['LOCALAPPDATA'], f"Bingo")

executables = [cx_Freeze.Executable("sources/main.py", base=base, shortcut_name="Bingo", shortcut_dir="DesktopFolder", target_name="Bingo.exe", 
                                    icon='sources/resources/bingo_icon.ico')]

cx_Freeze.setup(
    name="Bingo",
    options={"build_exe": {"packages":["pygame", "random", "datetime", "base64", "json", "tkinter", "os", "shutil", "sys"],
                           "include_files":["sources/resources/bingo_icon.svg", "sources/resources/bingo_icon.ico"]},
            "bdist_msi": {'initial_target_dir': path}},
    executables = executables

)