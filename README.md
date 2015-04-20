# YourNextMP (Read)

Helping voters get to know their General Election 2015 candidates.

This site combines the various outputs of
[Democracy Club](https://twitter.com/democlub) into one place.

## Requirements

 * Jekyll >= 2.4.0 ([installation instructions](http://jekyllrb.com/docs/installation/))
 * Python 2.7 ([installation instructions](https://www.python.org/downloads/))

You will also need the following Python packages installed:

 * [geopy](https://pypi.python.org/pypi/geopy/)

## Installation

```
# clone this repo
git clone https://github.com/DemocracyClub/YourNextMP-Read.git

# run the setup scripts
cd YourNextMP-Read
_scripts/setup.sh
_scripts/build.sh
```

## Running the server

For development, only a mini version of the site is built by default.

```
# build the site, and start the server running
jekyll serve
```

To build for all constituencies, use:

```
jekyll serve --config _config.yml,_config_prod.yml
```
