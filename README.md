# satellite-network-simulation

Simulate a network of satellite nodes to compare performance compared to regular ground nodes.

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

## How to contribute

After cloning the repository, ensure that the 'develop' branch is selected before commiting changes.

`git checkout -b develop`

`git branch --set-upstream-to=origin/develop develop`

`git push --set-upstream origin develop`