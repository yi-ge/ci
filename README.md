Continuous Integration System
=============================

This is a basic continuous integration server, designed for GitHub and GitLab.  
The program use together with https://github.com/yi-ge/ci-web or http://git.oschina.net/mgenius/ci-web.

Python Versions
---------------

The System is tested under Python 3.6.2.

Installing
----------

### Virtualenv And Virtualenvwrapper (Option)

To install globally with pip (if you have pip 1.3 or greater installed globally):

```
$ [sudo] pip install virtualenv virtualenvwrapper
```

It will probably install virtualenv on your system. Maybe it’s even in your package manager.

If you use Ubuntu, try:

```
$ sudo apt-get install python-virtualenv virtualenvwrapper
```

Add three lines to your shell startup file (MAC in `~/.bash_profile`, Ubuntu in `~/.bashrc`, etc.) to set the location where the virtual environments should live, the location of your development project directories, and the location of the script installed with this package:

```
export WORKON_HOME=$HOME/WorkStation
export VIRTUALENVWRAPPER_PYTHON=`which python`
mkdir -p $WORKON_HOME
source /usr/local/bin/virtualenvwrapper.sh
```

After editing it, reload the startup file (e.g., run `source ~/.bashrc`).

**You can use：**

```
workon # list virtual environment
workon XXX # enter virtual environment
mkvirtualenv XXX # set up virtual environment
deactivate XXX # leave virtual environment
rmvirtualenv XXX # delete virtual environment
```

Ps：You may try [p](https://github.com/qw3rtman/p) or [pyenv](https://github.com/pyenv/pyenv). It is important that `p` does not support to manage `pip`.

### Install Pipenv

Pipenv: Sacred Marriage of Pipfile, Pip, & Virtualenv.

```
$ pip install --user pipenv
```

or

```
$ mkvirtualenv -p python3 ci
$ pip install pipenv
```

### Installation Dependency and Init Database

```
$ pipenv install
$ python db.py db init
$ python db.py db migrate
$ python db.py db upgrade
```

Delete `migrations` before `python db.py db init`.

### Run Server

```
$ python run.py
```
