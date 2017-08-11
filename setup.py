import sys
from cx_Freeze import setup, Executable

addtional_mods = ['numpy.core._methods', 'numpy.lib.format']

setup(
    name="Microgrid Controller Assessment Tool",
    version="1.0",
    description="This is a tool used to assess the performance of Microgrid Controllers",
    options = {'build_exe': {'includes': addtional_mods}},
    executables= [Executable("main.py", base = "Win32GUI")])
