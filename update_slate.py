#!/usr/bin/env /bin/python
from argparse import ArgumentParser
from pathlib import Path
from random import shuffle
from shutil import copy
from bs4 import BeautifulSoup as bs
from PIL import Image, ImageOps
from json import load

parser = ArgumentParser("Slate Updater")
parser.add_argument("input", type=Path, default=Path("./slated"))
parser.add_argument("output", type=Path, default=Path("./images"))
parser.add_argument("-s", "--shuffle", default=False, action="store_true")
parser.add_argument("-k", "--keep", default=True, action="store_true")
parser.add_argument("-r", "--resize-thumbs", default=False, action="store_true")
parser.add_argument("-hi", "--height", type=int, default=500)
parser.add_argument("-wi", "--width", type=int, default=500)
args = parser.parse_args()

files = sorted(
    list(
        p for p in args.input.glob("*") 
        if p.suffix in {".jpg", ".jpeg", ".png"}
    )
)

print(files)

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

blurbs = {}
if (args.input / "blurbs.json").exists():
    with open(args.input / "blurbs.json") as fp:
        blurbs = load(fp)

def add_thumb(section, image, title = None, body = None, alt = ""):
    heading_html = ""
    if title:
        heading_html = "<h2>%s</h2>" % title

    para_html = ""
    if body:
        para_html = "<p>%s</p>" % body
    html = f"""
    <article>
        <a class="thumbnail" href="images/fulls/{image.name}"><img src="images/thumbs/{image.name}" alt="{alt}" /></a>
        {heading_html}
        {para_html}
        <a href="images/fulls/{image.name}"><i class="fa fa-expand" aria-hidden="true"></i></a>
    </article>
    """
    section.append(bs(html, 'html.parser'))

blurb_content = blurbs.get("blurbs", [])

for i, file in enumerate(files):
    print(i, file)
    new = copy(file, fdest / file.name)

    try:
        content = blurb_content[i]
        if blurbs:
            title, body, alt = content.get("title"), content.get("body"), content.get("alt")
            print(title)
            add_thumb(thumbs, new, title=title, body=body, alt=alt)
    except IndexError:
        add_thumb(thumbs, new)


    if args.resize_thumbs:
        t = Image.open(file)
        t = ImageOps.fit(
            t, 
            (args.width, args.height), 
            bleed=0, 
            centering=(0.5, 0.5), 
            method=Image.Resampling.LANCZOS
        )
        t.save(tdest / file.name)
    else:
        copy(file, tdest / file.name)

if args.shuffle:
    articles = thumbs.find_all("article")
    shuffle(articles)
    thumbs.clear()
    for a in articles:
        thumbs.append(a)

with open("index.html", "w") as fp:
    fp.write(soup.prettify())