# Setup

django-tz-detect uses `uv` and `tox` to run tests.
The following commands show what you need to get started.

```
uv sync --group dev
uv run pre-commit install
uv run pytest
```

To run the full test matrix (every supported Python and Django version):

```
uv tool install tox --with tox-uv --with tox-gh
tox
```

# JavaScript

In production (`DEBUG = False`) the `detector.html` template loads the
minified `tzdetect.min.js`, not `tzdetect.js`. After changing
`tzdetect.js`, rebuild the minified file and commit both:

```
cd tz_detect/static/tz_detect/js
npx --yes terser@5.36.0 tzdetect.js --compress --mangle -o tzdetect.min.js
```

# Release checklist

These are notes for how to make a release.

* Update `VERSION`
* Update `CHANGES.txt`
* Update `classifiers` in `setup.py`
* Build package: `python -m build`
* Tag release: `git tag -a <version> -m "Version <version>"`
* Push to GitHub with new tag: `git push --follow-tags`
* Release! `twine upload dist/*`
