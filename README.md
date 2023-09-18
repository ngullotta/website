# Personal Website

## "Slate Updater"

First, in order to run the script you will need `poetry`. Install using your
package manager, then run `poetry install`. After, you can run `poetry shell` to
drop into a shell with all the dependencies

- _alternatively you can just install the deps yourself manually from
  `pyproject.toml`_

To run: Simply place images you want to display in the gallery in the `slated`
folder and then run `python update_slate.py ./slated ./images --resize-thumbs`

The script will copy them to `./images/fulls` and `./images/thumbs` (with the
latter being resized if using `--resize-thumbs`) _and_ will add the appropriate
articles to `index.html`
