# How to use this Template!

Hello, thank you for using this template. This template is set up with the skeleton for deployment, and this readme will explain how to build the body. Although, you dont need to deploy and you can run the frontend normally according to Vite, and the backend according to Flask. (If you do want to work locally at this time, update the SQLALCHEMY_DATABASE_URI to 'sqlite:///app.db')

```bash
npm run dev
```

```bash
flask run 
```
or
```bash
python3 server/app.py 
```

If you do want to deploy, first we need to set up our system for the postgresql database and also set our postgresql database on render

- [Set up our system for the postgresql database](#postgresql-database-environment-setup)
- [Set our postgresql database on render](#creating-a-postgresql-database-on-render)

Perfect! Great job installing postgresql on your computer, setting up your Render postgresql database and assigning it in your .env file!

Our flask is now set up to operate with our Render postgresql database! we can start creating our database and view our Vite project locally without deploying at this time. At this time we can run this command to run our frontend and backend parallel:

```console
$ honcho start -f Procfile.dev
```

To deploy we will follow the next two steps to build our production build and finally deploy it on Render!

- [Build our production Vite files and alter our Flask app](#Deployment-Build)
- [Render Deployment Guide](#Render-Build-Process)

This Vite and Flask template made for deployment is built on top of a template not made for deployment and without Vite. The original Readme can be found using the link below. This will include the Flask commands for running your application and a basic walkthrough of how to get started

- [Original Readme!](#phase-4-full-stack-application-project-template)

## Postgresql Database Environment Setup

To make sure you're able to deploy your application, you'll need to do the
following to set up backend database on render as a postgresql database:

### Sign Up for a Render Account

You can sign up at for a free account at
[https://dashboard.render.com/][render dashboard]. We recommend signing up using
your GitHub account- this will streamline the process of connecting your
applications to Render later on.

### Install PostgreSQL

Render requires that you use PostgreSQL for your database instead of SQLite.
PostgreSQL (or just Postgres for short) is an advanced database management
system with more features than SQLite. If you don't already have it installed,
you'll need to set it up.

#### PostgreSQL Installation for WSL

To install Postgres for WSL, run the following commands from your Ubuntu
terminal:

```console
$ sudo apt update
$ sudo apt install postgresql postgresql-contrib libpq-dev
```

Then confirm that Postgres was installed successfully:

```console
$ psql --version
```

Run this command to start the Postgres service:

```console
$ sudo service postgresql start
```

Finally, you'll also need to create a database user so that you are able to
connect to the database from Flask. First, check what your operating system
username is:

```console
$ whoami
```

If your username is "ian", for example, you'd need to create a Postgres user
with that same name. To do so, run this command to open the Postgres CLI:

```console
$ sudo -u postgres -i
```

From the Postgres CLI, run this command (replacing "ian" with your username):

```console
$ createuser -sr ian
```

Then enter `control + d` or type `logout` to exit.

[This guide][postgresql wsl] has more info on setting up Postgres on WSL if you
get stuck.

#### Postgresql Installation for OSX

To install Postgres for OSX, you can use Homebrew:

```console
$ brew install postgresql
```

Once Postgres has been installed, run this command to start the Postgres
service:

```console
$ brew services start postgresql
```

Phew! With that out of the way, let's get started on building our Flask
application and deploying it to Render.

***

### Creating a PostgreSQL Database on Render

Using SQLite, our database was generated in a file in our application directory.
With PostgreSQL, the database is stored elsewhere- typically on a server
dedicated to databases. Ours will be stored on a server at Render.

From your Render dashboard, click the "New+" button and select PostgreSQL:

![dropdown menu containing static site, web service, private service, background
worker, cron job, postgresql, redis, and blueprint. postgresql is selected.](
https://curriculum-content.s3.amazonaws.com/python/python-p4-deployment-render-postgres.png
)

Next, configure your database with a name, database name, user, and timezone.
These can be whichever values you feel are best, note that some are optional and can be left blank.

![form with fields name, database, user, region, postgresql version, and datadog
api key](
https://curriculum-content.s3.amazonaws.com/python/python-p4-deployment-render-postgres-config.png
)

Finally, create your database. It will expire after 90 days; you can always make
a new one, but there are paid options available as well. For now, select the
free tier:

![payment options for render databases. the free tier is selected. there is a
create database button at the bottom that will allow users to finish creating
their database](
https://curriculum-content.s3.amazonaws.com/python/python-p4-deployment-render-postgres-payment.png
)

From here, scroll down in the new database configuration page and copy the
"External Database URL". Modify the protocol to say `postgresql` instead of
`postgres` (SQLAlchemy is picky) and update the DATABASE_URI in the .env, like below:

```python
DATABASE_URI="External Database URL goes here"
```



Now we're ready to start building our app.

# Deployment Build

- These steps will make a static version of our project that will be ready for deployment and also ready to run locally using our 'honcho' command

- first, Render wont use our pipfile to create a shell like we typically do locally, instead it will install all of our packages from a requirements.txt. This code will create a requirements.txt according to our pipenv packages:
```console
$ pipenv requirements > requirements.txt
```

- second, we want to build the production version of our React app, this will create a static version that lives in our client under dist:

```console
$ npm run build --prefix client
```

- third, our server/config.py has two app=flask commands, comment the deployment code in, it should match the below code(it is set up for Vite):

```py
app = Flask(
    __name__,
    static_url_path='',
    static_folder='../client/build',
    template_folder='../client/build'
)
```
above code for create-react-app and below code for vite

```py
app = Flask(
    __name__,
    static_url_path='',
    static_folder='../client/dist',
    template_folder='../client/dist'
)
```

- fourth, both of these routes are in the bottom of the server/app.py, comment back in one of the methods, they will allow our flask app to deploy our frontend by default. It is recommended that we setup our backend routes to start with an extra preface such as '/api'.

```py
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")
```
use either the above or below functions (but not both) 

```py
@app.errorhandler(404)
def not_found(e):
    return render_template("index.html")

```

- fifth, Lets make sure our 'Procfile.dev' is created and correct:

```bash
web: PORT=4000 npm start --prefix client
api: gunicorn -b 127.0.0.1:5555 --chdir ./server app:app
```
above code for create-react-app and below code for vite
```bash
web: npm run dev --prefix client
api: gunicorn -b 127.0.0.1:5000 --chdir ./server app:app
```

- lastly, push the code to github (which will trigger a new update of our deployed project) or run below the code in our terminal to run it locally (we also need to change our app = Flask to the local version in the config):

```console
$ honcho start -f Procfile.dev
```


# Now that our project is uploaded on github and configured to deployment, lets set up render!

## Render Build Process

Think about the steps to build our React application locally. What did we have
to do to build the React application in such a way that it could be served by
our Flask application? Well, we had to:

- Run `npm install --prefix client` to install any dependencies.
- Use `npm run build --prefix client` to create the production app.
- Install `pip` dependencies for the Flask app.
- Run `gunicorn --chdir server app:app` to run the Flask server.

We would also need to repeat these steps any time we made any changes to the
React code, i.e., to anything in the `client` folder. Ideally, we'd like to be
able to **automate** those steps when we deploy this app to Render, so we can
just push up new versions of our code to Render and deploy them like we were
able to do in the previous lesson.

Thankfully, Render lets us do just that! Let's get started with the deploying
process and talk through how this automation works.

Commit all of your work to your fork on GitHub and copy the project URL.

Navigate to [your Render dashboard][https://dashboard.render.com] and create
a new web service. Find your forked repository through "Connect a repository"
or search by the copied URL under "Public Git repository."

Change your "Build Command" to the following:

```console
$ pip install -r requirements.txt && npm install --prefix client && npm run build --prefix client
```

Change your "Start Command" to the following:

```console
$ gunicorn --chdir server app:app
```

These commands will:

- Install any Python dependencies with `pip`.
- Install any Node dependencies with `npm`.
- Build your static site with `npm`.
- Run your Flask server.

Once you have saved these changes, navigate to the "Environment" tab and make
sure the following values are set:

```txt
DATABASE_URI=postgresql://{retrieve this from from render}
PYTHON_VERSION=YOUR_PYTHON_VERSION
```

Click "Save Changes" and wait for a while. (Render's free tier can take up to
an hour to get everything set up, so you might want to grab a bagel and coffee
while you wait.) Navigate to "Events" to check for progress and errors. When
Render tells you the site is "Live", navigate to your site URL and view Birdsy
in all its glory!

---


# Phase 4 Full-Stack Application Project Template

## Learning Goals

- Discuss the basic directory structure of a full-stack Flask/React application.
- Carry out the first steps in creating your Phase 4 project.

---

## Introduction

Fork and clone this lesson for a template for your full-stack application. Take
a look at the directory structure before we begin (NOTE: node_modules will be
generated in a subsequent step):

```console
$ tree -L 2
$ # the -L argument limits the depth at which we look into the directory structure
.
├── CONTRIBUTING.md
├── LICENSE.md
├── Pipfile
├── README.md
├── client
│   ├── index.html
│   ├── vite.config.js
│   ├── README.md
│   ├── package.json
│   ├── public
│   └── src
└── server
    ├── app.py
    ├── config.py
    ├── models.py
    └── seed.py
```

A `migrations` folder will be added to the `server` directory in a later step.

The `client` folder contains a basic React application, while the `server`
folder contains a basic Flask application. You will adapt both folders to
implement the code for your project .

NOTE: If you did not previously install `tree` in your environment setup, MacOS
users can install this with the command `brew install tree`. WSL and Linux users
can run `sudo apt-get install tree` to download it as well.

## Where Do I Start?

Just as with your Phase 3 Project, this will likely be one of the biggest
projects you've undertaken so far. Your first task should be creating a Git
repository to keep track of your work and roll back any undesired changes.

### Removing Existing Git Configuration

If you're using this template, start off by removing the existing metadata for
Github and Canvas. Run the following command to carry this out:

```console
$ rm -rf .git .canvas
```

The `rm` command removes files from your computer's memory. The `-r` flag tells
the console to remove _recursively_, which allows the command to remove
directories and the files within them. `-f` removes them permanently.

`.git` contains this directory's configuration to track changes and push to
Github (you want to track and push _your own_ changes instead), and `.canvas`
contains the metadata to create a Canvas page from your Git repo. You don't have
the permissions to edit our Canvas course, so it's not worth keeping around.

### Creating Your Own Git Repo

First things first- rename this directory! Once you have an idea for a name,
move one level up with `cd ..` and run
`mv python-p4-project-template <new-directory-name>` to change its name (replace
<new-directory-name> with an appropriate project directory name).

> **Note: If you typed the `mv` command in a terminal within VS Code, you should
> close VS Code then reopen it.**

> **Note: `mv` actually stands for "move", but your computer interprets this
> rename as a move from a directory with the old name to a directory with a new
> name.**

`cd` back into your new directory and run `git init` to create a local git
repository. Add all of your local files to version control with `git add --all`,
then commit them with `git commit -m'initial commit'`. (You can change the
message here- this one is just a common choice.)

Navigate to [GitHub](https://github.com). In the upper-right corner of the page,
click on the "+" dropdown menu, then select "New repository". Enter the name of
your local repo, choose whether you would like it to be public or private, make
sure "Initialize this repository with a README" is unchecked (you already have
one), then click "Create repository".

Head back to the command line and enter
`git remote add origin git@github.com:github-username/new-repository-name.git`.
NOTE: Replace `github-username` with your github username, and
`new-repository-name` with the name of your new repository. This command will
map the remote repository to your local repository. Finally, push your first
commit with `git push -u origin main`.

Your project is now version-controlled locally and online. This will allow you
to create different versions of your project and pick up your work on a
different machine if the need arises.

---

## Setup

### `server/`

The `server/` directory contains all of your backend code.

`app.py` is your Flask application. You'll want to use Flask to build a simple
API backend like we have in previous modules. You should use Flask-RESTful for
your routes. You should be familiar with `models.py` and `seed.py` by now, but
remember that you will need to use Flask-SQLAlchemy, Flask-Migrate, and
SQLAlchemy-Serializer instead of SQLAlchemy and Alembic in your models.

The project contains a default `Pipfile` with some basic dependencies. You may
adapt the `Pipfile` if there are additional dependencies you want to add for
your project.

To download the dependencies for the backend server, run:

```console
pipenv install
pipenv shell
```

You can run your Flask API on [`localhost:5555`](http://localhost:5555) by
running:

```console
python server/app.py
```

Check that your server serves the default route `http://localhost:5555`. You
should see a web page with the heading "Phase 4 Project Server".

### `client/`

The `client/` directory contains all of your frontend code. The file
`package.json` has been configured with common React application dependencies, not
including `react-router-dom`. The file also sets the `proxy` field to forward
requests to `"http://localhost:5000". Feel free to change this to another port-
just remember to configure your Flask app to use another port as well!

To download the dependencies for the frontend client, run:

```console
npm install --prefix client
```

You can run your React app on [`localhost:3000`](http://localhost:3000) by
running:

```sh
npm dev --prefix client
```

Check that your the React client displays a default page
`http://localhost:3000`. You should see a web page with the heading "Phase 4
Project Client".

## Generating Your Database

NOTE: The initial project directory structure does not contain the `instance` or
`migrations` folders. Change into the `server` directory:

```console
cd server
```

Then enter the commands to create the `instance` and `migrations` folders and
the database `app.db` file:

```
flask db init
flask db upgrade head
```

Type `tree -L 2` within the `server` folder to confirm the new directory
structure:

```console
.
├── app.py
├── config.py
├── instance
│   └── app.db
├── migrations
│   ├── README
│   ├── __pycache__
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions
├── models.py
└── seed.py
```

Edit `models.py` and start creating your models. Import your models as needed in
other modules, i.e. `from models import ...`.

Remember to regularly run
`flask db revision --autogenerate -m'<descriptive message>'`, replacing
`<descriptive message>` with an appropriate message, and `flask db upgrade head`
to track your modifications to the database and create checkpoints in case you
ever need to roll those modifications back.

> **Tip: It's always a good idea to start with an empty revision! This allows
> you to roll all the way back while still holding onto your database. You can
> create this empty revision with `flask db revision -m'Create DB'`.**

If you want to seed your database, now would be a great time to write out your
`seed.py` script and run it to generate some test data. Faker has been included
in the Pipfile if you'd like to use that library.

---

#### `config.py`

When developing a large Python application, you might run into a common issue:
_circular imports_. A circular import occurs when two modules import from one
another, such as `app.py` and `models.py`. When you create a circular import and
attempt to run your app, you'll see the following error:

```console
ImportError: cannot import name
```

If you're going to need an object in multiple modules like `app` or `db`,
creating a _third_ module to instantiate these objects can save you a great deal
of circular grief. Here's a good start to a Flask config file (you may need more
if you intend to include features like authentication and passwords):

```py
# Standard library imports

# Remote library imports
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

# Local imports

# Instantiate app, set attributes
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Define metadata, instantiate db
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)
migrate = Migrate(app, db)
db.init_app(app)

# Instantiate REST API
api = Api(app)

# Instantiate CORS
CORS(app)

```

Now let's review that last line...

#### CORS

CORS (Cross-Origin Resource Sharing) is a system that uses HTTP headers to
determine whether resources from different servers-of-origin can be accessed. If
you're using the fetch API to connect your frontend to your Flask backend, you
need to configure CORS on your Flask application instance. Lucky for us, that
only takes one line:

```py
CORS(app)

```

By default, Flask-CORS enables CORS on all routes in your application with all
fetching servers. You can also specify the resources that allow CORS. The
following specifies that routes beginning with `api/` allow CORS from any
originating server:

```py
CORS(app, resources={r"/api/*": {"origins": "*"}})

```

You can also set this up resource-by-resource by importing and using the
`@cross_origin` decorator:

```py
@app.route("/")
@cross_origin()
def howdy():
  return "Howdy partner!"

```

---

## Updating Your README.md

`README.md` is a Markdown file that describes your project. These files can be
used in many different ways- you may have noticed that we use them to generate
entire Canvas lessons- but they're most commonly used as homepages for online
Git repositories. **When you develop something that you want other people to
use, you need to have a README.**

Markdown is not a language that we cover in Flatiron's Software Engineering
curriculum, but it's not a particularly difficult language to learn (if you've
ever left a comment on Reddit, you might already know the basics). Refer to the
cheat sheet in this lesson's resources for a basic guide to Markdown.

### What Goes into a README?

This README should serve as a template for your own- go through the important
files in your project and describe what they do. Each file that you edit (you
can ignore your migration files) should get at least a paragraph. Each function
should get a small blurb.

You should descibe your application first, and with a good level of detail. The
rest should be ordered by importance to the user. (Probably routes next, then
models.)

Screenshots and links to resources that you used throughout are also useful to
users and collaborators, but a little more syntactically complicated. Only add
these in if you're feeling comfortable with Markdown.

---

## Conclusion

A lot of work goes into a full-stack application, but it all relies on concepts
that you've practiced thoroughly throughout this phase. Hopefully this template
and guide will get you off to a good start with your Phase 4 Project.

Happy coding!

---

## Resources

- [Setting up a respository - Atlassian](https://www.atlassian.com/git/tutorials/setting-up-a-repository)
- [Create a repo- GitHub Docs](https://docs.github.com/en/get-started/quickstart/create-a-repo)
- [Markdown Cheat Sheet](https://www.markdownguide.org/cheat-sheet/)
- [Python Circular Imports - StackAbuse](https://stackabuse.com/python-circular-imports/)
- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/)

