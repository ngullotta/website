#!/usr/bin/env /bin/python
from argparse import ArgumentParser
from pathlib import Path
from random import shuffle
from shutil import copy
from bs4 import BeautifulSoup as bs
from PIL import Image

parser = ArgumentParser("Slate Updater")
parser.add_argument("input", type=Path, default=Path("./slated"))
parser.add_argument("output", type=Path, default=Path("./images"))
parser.add_argument("-s", "--shuffle", default=False, action="store_true")
parser.add_argument("-k", "--keep", default=True, action="store_true")
parser.add_argument("-r", "--resize-thumbs", default=False, action="store_true")
parser.add_argument("-hi", "--height", type=int, default=500)
parser.add_argument("-wi", "--width", type=int, default=500)
args = parser.parse_args()

files = list(
    p for p in args.input.glob("*") 
    if p.suffix in {".jpg", ".jpeg", ".png"}
)

if args.shuffle:
    shuffle(files)

fdest = args.output / "fulls"
if not fdest.exists():
    fdest.mkdir()
    
for file in fdest.glob("*"):
    file.unlink()

tdest = args.output / "thumbs"
if not tdest:
    tdest.mkdir()

for file in tdest.glob("*"):
    file.unlink()

soup = bs(Path("./index.html").read_text(), 'html.parser')

thumbs = soup.find(id="thumbnails")
if thumbs:
    thumbs.clear()

print(thumbs)

def add_thumb(section, image):
    html = f"""
    <article>
        <a class="thumbnail" href="images/fulls/{image.name}"><img src="images/thumbs/{image.name}" alt="" /></a>
        <h2>Diam tempus accumsan</h2>
        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
        <a href="images/fulls/{image.name}"><i class="fa fa-expand" aria-hidden="true"></i></a>
    </article>
    """
    section.append(bs(html, 'html.parser'))

for i, file in enumerate(files):
    print(i, file)
    new = copy(file, fdest / file.name)
    add_thumb(thumbs, new)

    if args.resize_thumbs:
        t = Image.open(file)
        new_t = t.resize((args.width, args.height))
        new_t.save(tdest / file.name)
    else:
        copy(file, tdest / file.name)

with open("index.html", "w") as fp:
    fp.write(soup.prettify())