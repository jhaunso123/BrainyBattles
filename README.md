# BrainyBattles
Algorithms Project IEU 2023

A Breif Overview:
This project has been created to teach kids educational material from a young age in a fun way. This has all been programmed by our fantastic group, for a Algorithms and Data Structures course in IE University taught by Antonio Lopez Rosell. This is our first time creating a project in python at this scale, so dont scrutinize us too hard. :)


What exactly does the code do?
When you run the code you will me met with a welcome page, which allows you to login and register. After logging in or registering, you will choose your year, level and prefered subject. This will effect the types of questions you will be asked. Now you will be prompted to answer questions one at a time. Based on your answer you will be told if you are correct or incorrect.

HOW TO RUN
Implementation may vary depending on your preffered python app. Here is how to install into pycharm:

1. Download the zip from github.
2. Unzip
3. Create a new python project in pycharm.
4. Drag and drop the downloaded file from your downloads into your python project folder.

Now you will have the foldr in your python project folder. Next you will need to install necessary packages into your pycharm. This can be done by running the code below in your terminal:

pip install Alembic bcrypt blinker click et-xmlfile Flask Flask-Bcrypt Flask-Login Flask-Migrate Flask-SQLAlchemy Flask-WTF itsdangerous  Jinja2 Mako MarkupSafe numpy openpyxl pandas pip python-dateutil pytz setuptools six SQLAlchemy  typing_extensions tzdata Werkzeug wheel WTForms

Once you have these packages installed find the file "algorithms questions.xlsx" in the downloaded folder, within your python project. Right click on the file and copy its absolute file path. You will then search for the phrase filepath in the code file "project fr + edited". This can be done by clicking on the file and clicking on the code and using the search tool (command F). Once you find the line containing the filepath, replace the current filepath with the one you copied earlier. 

Run the code.

After running you will be prompted in the running window saying : "WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:8000"

Click the link where it says "running on", you will be directed to a login page.


HOW TO USE
Once you are in the login page you must register an account, do so by entering a username and password. Once you do this you can enter the site and will be prompted to enter your year and what difficulty you would like the questions to have. Now have fun learning






Packages:
pip install Flask Flask-SQLAlchemy Flask-Login Flask-WTF Flask-Bcrypt pandas Flask-Migrate
