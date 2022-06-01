# Banana
NOTE: this project has also been hosted on https://r3tr0m1ll3r.pythonanywhere.com/ where all styling with custom error pages and production level settings is visible.

This is the github repository for a site made by R3tr0. This repository has contains a project showing an ecommerce site made by R3tr0 for a company "Banana" that is run by an enterprising minion. This project is based off of Django web framework and Thus requires the users to run it in a python environment.

# Important notes:

- This project has got its debug set to "True" as Django does not support delivering static files such as css, javascript and images in prodution via the lightweight server that comes with manage.py. As a result, there would have been no styles available if debug would have been set to False. Since debug has been set to true, there would be no custom error pages visible and sensetive tracebacks might be visible. Anybody using this project as a template for a production site is advised to set the DEBUG setting in minionfactory app's settings.py to false before production. Also, you are advised to update the SECRET_KEY field to a secure string of preferably more than 50 characters as this is a very sensetive setting and should be a unique string that is undisclosed.

- However, this project has also been hosted on https://r3tr0m1ll3r.pythonanywhere.com/ where all styling with custom error pages and production level settings is visible.

# Project Setup
### Prerequisites
  - Python 3.9 and added to path.
  - git bash terminal.
  - git installed on your terminal and added to path.
  - Redis Server (optional).
  
### Steps
- Open a git bash terminal.

- Install python virtual environment by running: `pip install virtualenv`. 

- Create python virtual environment by running: `python3 -m venv name_virtual_env`

- Activate Virtual Env:
  - On linux: `source name_virtual_env/bin/activate`
  - On windows: `name_virtual_env\Scripts\activate`

- Clone repository with: `git clone https://github.com/RETR0-OS/Banana.git`

- `cd Banana`

- Install requirements for project by running: `pip install -r requirements.txt`

- `python3 manage.py runserver`
- `python3 manage.py makemigrations`
- `python3 manage.py migrate`
- Then browse to the url: `localhost:8000`
- The site would be visible.

