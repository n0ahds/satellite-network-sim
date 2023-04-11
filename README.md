# satellite-network-simulation

This module simulates a simple satellite network using Python and pygame. It allows users to create and configure a network of LEO and MEO satellites and ground stations, simulate packet routing, and visualize the network state over time.

## How to run

Install the latest version of python at https://www.python.org/.

Upgrade pip and setuptools:

```
pip install --upgrade setuptools
pip install --upgrade pip
```

In the project's root directory, install a python virtual environment using `python -m venv venv`

Activate the virtual environment:

- Windows: `& .\venv\Scripts\Activate.ps1`

- MacOS & Linux: `source venv/bin/activate`

Install required libraries with `pip install -r requirements.txt`

Finally, run the program using `python -u main.py`

<img src="screen_recording.gif">

<br/>

## How to contribute

After cloning the repository, ensure that the 'develop' branch is selected before commiting changes.

`git checkout -b develop`

`git branch --set-upstream-to=origin/develop develop`

`git push --set-upstream origin develop`