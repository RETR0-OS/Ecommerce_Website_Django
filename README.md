# Ecommerce Website
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
- `python3 manage.py makemigrations`
- `python3 manage.py migrate`
- `python3 manage.py runserver`
- Then browse to the url: `localhost:8000`
- The site would be visible.

#### Optional Steps:
If you wish to set up brute force protection on the login pages of the site, you will require Redis Server to be installled on your system.
To set up this feature, follow the following steps:
- Before 8 th step in the above instructions, go to the minionfactory directory by doing `cd minionfactory`.
- Open up the settings.py file and uncomment the follwing lines:
  - ```
    INSTALLED_APPS = [
    #    'defender',
    ```
  - ``` 
    #'defender.middleware.FailedLoginMiddleware', 
    ```
  - ``` 
    #DEFENDER_LOGIN_FAILURE_LIMIT_IP = 10
    #DEFENDER_DISABLE_USERNAME_LOCKOUT = True
    #DEFENDER_LOCKOUT_TEMPLATE = "security/defender_lockout.html"
    #DEFENDER_ACCESS_ATTEMPT_EXPIRATION = 12
    ```
- Next, go to the urls.py file in the same directory and uncomment the following lines:
  - ```
    #import defender
    ```
  - ```
    #    path('admin/defender', include('defender.urls')),
    ```
 - Open a git bash terminal and run `python3 manage.py makemigrations defender`
 - Next run `python3 manage.py migrate defender`
 - Continue with step 8 as stated above and the rest of the steps.
 - Before the 11th step, open a new git bash terminal and run the Redis server by:
    - On Linux: `redis-server`
    - On windows: `redis-server.exe` (assuming that redis is added to path).
    - Note: make sure that redis is running on the default port: port 6379.
 - This feature is using django-defender package. If you wish to understand or tinker with the defender settings, you may the documentation of this package at https://django-defender.readthedocs.io/en/latest/ .
