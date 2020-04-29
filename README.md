# CLASH CREDENZ 19'

### Working project of Clash which is a technical MCQ based event in Credenz organised by PICT IEEE Student Branch

## Steps to run project:

* To install pip: **sudo apt install python3-pip**
* To install virtualenv: **sudo pip3 install virtualenv**
* To start virtualenv: **virtualenv venv**
* To activate virtualenv: **source venv/bin/activate**
* To deactivate virtualenv: **deactivate**
* To install requirements and run project: 
    1. Activate virtualenv
    2. To install dependencies required **pip3 install -r requirements.txt**
    3. Run **python manage.py makemigrations**
    4. Run **python manage.py migrate** to make migrations
    5. Add a few questions in the database to see functioning
    6. To run clash **python manage.py runserver**
    7. Enjoy!

## Technology Used:

* **Front end:**
  1. HTML5
  2. CSS3
  3. Javascript and AJAX
  
* **Back end:**
  1. Django 3.0.5 (Python web framework)
 
* **Database used:**
  1. SQLite3
 
## Modules Used:

* User authentication
* Timer
* Conditional controlling of HTML elements
* Dealing with garbage url 

## Snippets of the project:

### 1. Login page
![clash1](/screenshots/clash1.png)

### 2. Instruction page
![clash2](/screenshots/clash2.png)

### 3. Questions page
![clash3](/screenshots/clash3.png)

### 4. Result Page
![clash4](/screenshots/clash4.png)


