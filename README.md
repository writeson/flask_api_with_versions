# Sandro API

This repo contains an example Flask application to provide a restful API that accepts XML content and
responds by calling other API's based on the content of the XML. Those other calls can be directed to
other sites with other response body types (JSON, XML, who knows)

# Installation

I used [pyenv](https://github.com/pyenv/pyenv) to create a Python VirtualEnv to run this application. I also had previously installed Python version 3.9.5, which I used here. This application should run without problems with not so current versions of Python

To install using pyenv follow these steps:

```console
git clone <this repository>
cd <cloned directory>
pyenv local 3.9.6
python -m venv .venv
pip install --upgrade pip
pip install -r requirements.txt
```

This will clone the repository into a directory, install a Python virtual environment in that directory, update the `pip` command and install the Python module requirements of the project.
