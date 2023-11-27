# Personal Website

My personal website, subject to change on a whim.

## Gallery Updater

First, in order to run the script you will need `poetry`. Install using your
package manager, then run `poetry install`. After, you can run `poetry shell` to
drop into a shell with all the dependencies

- _alternatively you can just install the deps yourself manually from
  `pyproject.toml`_

To run: Simply place images you want to display in the gallery in the `slated`
folder and then run `python update_gallery.py slated/* --resize-thumbs`

The script will copy them to `./images/fulls` and `./images/thumbs` (with the
latter being resized if using `--resize-thumbs`) _and_ will add the appropriate
articles to `index.html`

Additionally if you add a `blurbs.json` each title, description, and alt text, 
will be added to each image. Like so:
```json
{
    "blurbs": [{
            "title": "The Border",
            "body": "... And dreadfully distinct against the dark, a tall white fountain played.",
            "alt": "A tall white lotus fountain"
        },
        {
            "title": "Vana",
            "body": "",
            "alt": ""
        },
        {
            "title": "Healing Waters",
            "body": "",
            "alt": ""
        },
        {
            "title": "Truth",
            "body": "There are three things that cannot long be hidden: the sun, the moon and the truth.",
            "alt": ""
        },
        {
            "title": "Luveh-Keraphf",
            "body": "... and with strange aeons, even death may die.",
            "alt": ""
        },
        {
            "title": "Saṃsāra",
            "body": "",
            "alt": ""
        }
    ]
}
```

Note: Order matters, so put the description objects in order of how it is 
listed in the slated folder