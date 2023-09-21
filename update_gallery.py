#!/usr/bin/env /bin/python
import functools
from argparse import ArgumentParser
from json import load
from pathlib import Path
from random import shuffle
from shutil import copy as cp
from tempfile import NamedTemporaryFile

from bs4 import BeautifulSoup as soup
from PIL import Image, ImageOps

parser = ArgumentParser("Gallery Updater")
parser.add_argument("images", type=Path, nargs="+")
parser.add_argument("-o", "--output", type=Path, default=Path("./images"))
parser.add_argument("-s", "--shuffle", default=False, action="store_true")
parser.add_argument("-k", "--keep", default=False, action="store_true")
parser.add_argument(
    "-r", "--resize-thumbs", default=False, action="store_true"
)
parser.add_argument("--height", type=int, default=500)
parser.add_argument("--width", type=int, default=500)
args = parser.parse_args()

# Ensure output path exists, or `mkdir` it now
if not args.output.exists():
    try:
        args.output.mkdir()
    except OSError as ex:
        print(
            f"[!] Output path @ {args.output} does not exist and/or could not "
            f"be created: {ex}"
        )
        exit(1)

# Now ensure subdir paths "fulls" and "thumbs exist"
for subdir in ["fulls", "thumbs"]:
    dest = args.output / subdir
    if not dest.exists():
        try:
            args.output.mkdir()
        except OSError as ex:
            print(
                f"[!] Subdir path @ {dest} does not exist and/or could not be "
                f"created: {ex}"
            )
            exit(1)
    else:
        for _file in dest.glob("*"):
            try:
                _file.unlink()
            except OSError as ex:
                print(f"[!] Could not unlink file @ {_file}: {ex}")


def transform(image: Image, ops: List[callable], *args, **kwargs) -> Image:
    for op in ops:
        image = op(image, *args, **kwargs)
    return image


def add_article():
    pass


def shuffle_articles():
    pass


def copy(path: Path, name: str = None, full_size: bool = True) -> Path:
    name = name or path.name
    path = Path(path)
    destination = (
        (args.output / "fulls") if full_size else (args.output / "thumbs")
    )
    try:
        return cp(path, destination)
    except OSError as ex:
        print(f"[!] Could not copy file @ {path} => {destination}: {ex}")
    return path


for i, _file in enumerate(files):
    # First, copy the full sized image
    copy(_file)

    # Even though it is full size, the dest will be thumbs
    if not args.resize_thumbs:
        copy(_file, full_size=False)
        continue

    # Next, make a thumbnail, and save it to temp
    # ToDo -> Handle errors here!
    with NamedTemporaryFile() as fp:
        image = Image.open(_file)
        image = transform(
            image,
            [ImageOps.fit],
            (args.width, args.height),
            method=Image.Resampling.LANCZOS,
        )
        image.save(fp.name)
        copy(fp.name, name=_file.name, full_size=False)
