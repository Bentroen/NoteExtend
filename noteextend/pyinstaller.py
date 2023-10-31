from pathlib import Path

import PyInstaller.__main__

HERE = Path(__file__).parent.absolute()
path_to_main = str(HERE / "gui.py")


def install():
    PyInstaller.__main__.run(
        [
            path_to_main,
            "--name=NoteExtend",
            "--onedir",
            "--noconsole",
            "--windowed",
            "--icon=img/icon.ico",
            "--add-data=img/icon.ico;.",
            "--add-data=ffmpeg.exe;.",
            "--add-data=ffprobe.exe;.",
        ]
    )
