import cx_Freeze

executables = [cx_Freeze.Executable("sources/main.py")]

cx_Freeze.setup(
    name="A bit Racey",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["sources/resources/bingo_icon.bmp"]}},
    executables = executables

)