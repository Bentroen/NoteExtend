import os
import re
from pathlib import Path
from typing import Any, Callable, Union
from zipfile import ZipFile

import pydub
import pynbs
from beet import ResourcePack, Sound

SONG_PATH = "test.nbs"
OUTPUT_PATH = "output.zip"

PathLike = Union[str, bytes, os.PathLike]


def load_song(path: PathLike) -> pynbs.File:
    return pynbs.read(path)


def sanitize_instrument_name(name: str) -> str:
    # Replace all non-alphanumeric characters with underscores
    return re.sub(r"\W+", "_", name).lower()


def load_audio_file(path: PathLike) -> pydub.AudioSegment:
    return pydub.AudioSegment.from_file(path)


def change_speed(sound: pydub.AudioSegment, speed: float) -> pydub.AudioSegment:
    return sound._spawn(
        sound.raw_data, overrides={"frame_rate": int(sound.frame_rate * speed)}
    ).set_frame_rate(sound.frame_rate)


def build_resource_pack(
    song: pynbs.File, callback: Callable[..., Any] | None = None
) -> ResourcePack:
    rp = ResourcePack()
    sounds_folder = Path(Path.home(), "Minecraft Note Block Studio", "Data", "Sounds")
    subtitle = "subtitles.block.note_block.note"

    for i, instrument in enumerate(song.instruments):
        print(f"Processing instrument #{i+1}: {instrument.name}")

        if callback:
            callback()

        if not instrument.file:
            print(f"Instrument {instrument.name} has no sound file; skipping")
            continue

        sound_path = Path(sounds_folder, instrument.file)

        try:
            sound = load_audio_file(sound_path)
        except FileNotFoundError:
            print(f"Sound file {os.path.basename(sound_path)} not found; skipping")
            continue

        if not instrument.name:
            instrument.name = f"Instrument #{i+1}"
        ins_name = sanitize_instrument_name(instrument.name)

        # Create lower and higher-pitched versions of the sound
        sound_lower = change_speed(sound, 0.25).export(format="ogg")
        sound_default = sound.export(format="ogg")
        sound_higher = change_speed(sound, 4.0).export(format="ogg")

        sound_asset_lower = Sound(
            _content=sound_lower.read(),
            event=f"{ins_name}_-1",
            subtitle=subtitle,
        )
        sound_asset_default = Sound(
            _content=sound_default.read(), event=f"{ins_name}", subtitle=subtitle
        )
        sound_asset_higher = Sound(
            _content=sound_higher.read(),
            event=f"{ins_name}_1",
            subtitle=subtitle,
        )

        # Add the sounds to the resource pack
        base_path = "minecraft:block/note_block"
        rp[f"{base_path}/{ins_name}_-1"] = sound_asset_lower
        rp[f"{base_path}/{ins_name}"] = sound_asset_default
        rp[f"{base_path}/{ins_name}_1"] = sound_asset_higher

    return rp


def generate_pack(
    song_path: PathLike,
    output_path: PathLike,
    callback: Callable[..., Any] | None = None,
):
    print("Generating pack...")

    song = load_song(song_path)
    rp = build_resource_pack(song, callback)

    if not os.path.isfile(output_path):
        output_path = Path(
            output_path, f"{os.path.splitext(os.path.basename(song_path))[0]}.zip"
        )

    with ZipFile(output_path, "w") as zf:
        rp.dump(zf)

    sound_count = len(rp.sounds)
    print(f"Done! {sound_count} sounds were generated.")


if __name__ == "__main__":
    generate_pack(SONG_PATH, OUTPUT_PATH)
