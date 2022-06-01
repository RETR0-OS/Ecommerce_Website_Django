# Banana
NOTE: this project has also been hosted on https://r3tr0m1ll3r.pythonanywhere.com/ where all styling with custom error pages and production level settings is visible.

This is the github repository for a site made by R3tr0. This repository has contains a project showing an ecommerce site made by R3tr0 for a company "Banana" that is run by an enterprising minion. This project is based off of Django web framework and Thus requires the users to run it in a python environment.

<h1> Important notes:</h1>
  <ul>
    <li>This project has got its debug set to "True" as Django does not support delivering static files such as css, javascript and images in prodution via the lightweight server that comes with manage.py. As a result, there would have been no styles available if debug would have been set to False. Since debug has been set to true, there would be no custom error pages visible and sensetive tracebacks might be visible. Anybody using this project as a template for a production site is advised to set the DEBUG setting in minionfactory app's settings.py to false before production. Also, you are advised to update the SECRET_KEY field to a secure string of preferably more than 50 characters as this is a very sensetive setting and should be a unique string that is undisclosed.</li>
    <li>However, this project has also been hosted on https://r3tr0m1ll3r.pythonanywhere.com/ where all styling with custom error pages and production level settings is visible.</li>
  </ul>

<h1>Project Setup</h1>
<h3>Prerequisits</h3>
<ul>
  <li>Python 3.9</li>
  <li>git bash terminal</li>
  <li>dependencies in requirements.txt file</li>
  <li>Redis Server (optional) </li>
</ul>
  
<h3>Steps</h3>
<ul>
  <li> Open a git bash terminal. </li>
  <li>Install python virtual environment by running: pip install virtualenv: 
  <li>Create python virtual environment by running: python3 -m venv name_virtual_env</li>
  <li>Activate Virtul Env:<li/>
  <ul>
    <li>On linux: source name_virtual_env/bin/activate</li>
    <li>On windows: name_virtual_env\Scripts\activate </li>
  </ul>
  <li>Clone repository form: https://github.com/RETR0-OS/Banana.git </li>
  <li>cd Banana </li>
  <li> Install requirements for project by running: pip install -r requirements.txt </li>
  <li>cd minion factory </li>
  <li>python3 manage.py runserver </li>
  <li>Then go to the url: localhost:8000</li>
  <li>The site would be visible.</li>
</ul> 
