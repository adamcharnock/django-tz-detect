# Setup

django-tz-detect uses `tox` to run tests.
The following commands show what you need to get started.

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements/dev.txt
tox --py current
```

# Release checklist

These are notes for how to make a release.
First, make sure release tools are installed.

```
pip install -r requirements/dev.txt
```

* Update `VERSION`
* Update `CHANGES.txt`
* Update `classifiers` in `setup.py`
* Build package: `python -m build`
* Tag release: `git tag -a <version> -m "Version <version>"`
* Push to GitHub with new tag: `git push --follow-tags`
* Release! `twine upload dist/*`
