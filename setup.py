import os, sys
from cx_Freeze import setup, Executable

os.environ['TCL_LIBRARY'] = "C:\\Users\\inovic\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\inovic\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tk8.6"


# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os", "PyQt5", "numpy", "h5py", "matplotlib", "tkinter"],
					 "include_files": ["tcl86t.dll", "tk86t.dll"], "include_msvcr": True}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Microgrid Controller Assessment Tool",
        version = "1.0",
        description = "Authors:\nIlja Novickij\nAntonia Butler",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py", base=base, shortcutName="Microgrid Controller Assessment Tool", shortcutDir="DesktopFolder")])