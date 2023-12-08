# BrainyBattles

Algorithms Project IEU 2023

**A Breif Overview:**

This project has been created to aid middle school children study, especially if they have a short attention span. We created a website that quizzes children in a fun way by including gamification elements. This has all been programmed by our fantastic group, for our Algorithms and Data Structures course at IE University taught by Antonio Lopez Rosell. 

**What exactly does the code do?**

When you run the code you will be met with a welcome page, which allows you to login and register. After logging in or registering, you will choose your year, level and preferred subject. You will be quizzed on questions based on this selection. The questions are open answered and they will be shown one at a time. If your answer to the question is wrong, you will be told so and you will lose a life. You have a total of 3 lives in general. If you get the answer correct you will be told so and you'll continue with the number of lives that you have.

**HOW TO RUN**

Implementation may vary depending on your preffered python app. Here is how to run it in PyCharm:

1. Download the zip from github.
2. Unzip
3. Create a new python project in pycharm.
4. Drag and drop the downloaded file from your downloads into your python project folder.

Now you will have the github folder in your python project folder. Next you will need to install the necessary packages into your pycharm. This can be done by running the code below in your terminal:

pip install Alembic bcrypt blinker click et-xmlfile Flask Flask-Bcrypt Flask-Login Flask-Migrate Flask-SQLAlchemy Flask-WTF itsdangerous  Jinja2 Mako MarkupSafe numpy openpyxl pandas pip python-dateutil pytz setuptools six SQLAlchemy  typing_extensions tzdata Werkzeug wheel WTForms

Once you have these packages installed, find the file "algorithms questions.xlsx" in the downloaded folder, within your python project. Right click on the file and copy its absolute file path. You will then search for the phrase filepath in the code file "project fr + edited". This can be done by clicking on the file and clicking on the code and using the search tool (command F). Once you find the line containing the filepath, replace the current filepath with the one you copied earlier. 

Run the code.

After running you will be prompted in the running window saying : "WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:8000"

Click the link where it says "running on", you will be directed to a login page.


**HOW TO USE**

Once you are in the login page you must register an account, do so by entering a username and password. Once you do this you can enter the site and will be prompted to enter your year and what difficulty you would like the questions to have. Now have fun learning!!

**NOTES**

Packages:
pip install Flask Flask-SQLAlchemy Flask-Login Flask-WTF Flask-Bcrypt pandas Flask-Migrate


Since the creation of this website is for educational purposes, we did not use a huge dataset. In any case, we recommend changing the search algorithms in the code to suit the dataset that you want (if you want to change the current one).
