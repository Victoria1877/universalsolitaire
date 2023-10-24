import sys
from cx_Freeze import setup, Executable

# Dependencies required by your script
build_exe_options = {
    "packages": ["arcade", "random"],
    "includes": ["pyglet"],
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Use this for a GUI application on Windows

executables = [
    Executable("solitaire.py", base=base)
]

setup(
    name="Universal Solitaire",
    version="1.0",
    description="A Universal Python Arcade Based Solitaire Game",
    options={"build_exe": build_exe_options},
    executables=executables
)
