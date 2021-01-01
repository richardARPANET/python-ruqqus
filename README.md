# python-ruqqus

Python Wrapper for Ruqqus API

## Installation

From withing a Python virtualenv.

```bash
pip install ruqqus
```

For development:

```bash
pip install -r requirements-dev.txt
python setup.py develop
```

## Example Usage

See ``example.py``.

## Making a new release

Run the below command and follow the wizard instructions. This will package the release and upload to pypi.

```bash
pip install -r requirements-dev.txt
fullrelease
```

## Code formatting

This project uses the [brunette](https://pypi.org/project/brunette/) code formatter.

How to use:

```bash
brunette *.py
```
