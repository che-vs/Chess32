import sys
from cx_Freeze import setup, Executable

#Dependencies
build_exe_options = {
    "packages": ["pygame", "chess"],  #add other packages your game uses
    "include_files": [
        "images",           #images folder
        "bots",             #bots folder
        "codekiddy.bin",
        "lessons"
    ],
    "include_msvcr": True  #include MS runtime DLLs
}

#Base for GUI apps
base = None
if sys.platform == "win32":
    base = "Win32GUI"  #hides console window

setup(
    name="Chess32",
    version="1.0",
    description="Chess32 Game",
    options={"build_exe": build_exe_options},
    executables=[Executable("Chess32.py", base=base, icon="images/logo.ico")]
)
