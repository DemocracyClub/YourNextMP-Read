# YourNextMP (Read)

Helping voters get to know their General Election 2015 candidates.

This site combines the various outputs of
[Democracy Club](https://twitter.com/democlub) into one place.

## Requirements

 * Jekyll >= 2.4.0 ([installation instructions](http://jekyllrb.com/docs/installation/))
 * Python 2.7 ([installation instructions](https://www.python.org/downloads/))

You will also need the Python packages listed in `requirements.txt`.

## Installation

```
# clone this repo
git clone https://github.com/DemocracyClub/YourNextMP-Read.git
cd YourNextMP-Read

# install the requirements
# (you might want to use rbenv & virtualenv)
gem install jekyll
pip install -r requirements.txt

# run the build script

_scripts/build.sh
```

## Running the server

For development, only a mini version of the site is built by default.

```
# copy over a small selection of constituencies and people for development
python _scripts/build_data_small.py

# build the site, and start the server running
jekyll serve
```

To build for all constituencies, use:

```
jekyll serve --config _config.yml,_config_prod.yml
```
