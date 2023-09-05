# Special Guide for this deployment build

- update the .env to include the postgressql  database.
- create a requirements.txt from the pipfile
```console
$ pipenv requirements > requirements.txt
```

## Running Locally

- run below command to run the frontend and backend locally
```console
$ honcho start -f Procfile.dev
```


## React Production Build

One of the great features that Create React App provides to developers is the
ability to build different versions of a React application for different
environments.

When working in the **development** environment, a typical workflow for adding
new features to a React application is something like this:

- Run `npm start` to run a development server.
- Make changes to the app by editing the files.
- View those changes in the browser.

To enable this _excellent_ developer experience, Create React App uses
[webpack](https://webpack.js.org/) under the hood to create a development server
with hot module reloading, so any changes to the files in our application will
be instantly visible to us in the browser. It also has a lot of other nice
features in development mode, like showing us good error and warning messages
via the console.

Create React App is _also_ capable of building an entirely different version of
our application for **production**, also thanks to webpack. The end goal of our
application is to get it into the hands of our users via our website. For our
app to run in production, we have a different set of needs:

- **Build** the static HTML, JavaScript and CSS files needed to run our app in
  the browser, keeping them as small as possible.
- **Serve** the application's files from a server hosted online, rather than a
  local webpack development server.
- Don't show any error messages/warnings that are meant for developers rather
  than our website's users.

### Building a Static React App

When developing the frontend of a site using Create React App, our ultimate goal
is to create a **static site** consisting of pre-built HTML, JavaScript, and CSS
files, which can be served by Flask when a user makes a request to the server to
view our frontend. To demonstrate this process of **building** the production
version of our React app and **serving** it from the Flask app, follow these
steps.

**1.** Build the production version of our React app:

```console
$ npm run build --prefix client
```

This command will generate a bundled and minified version of our React app in
the `client/build` folder.

Check out the files in that directory, and in particular the JavaScript files.
You'll notice they have very little resemblance to the files in your `src`
directory! This is because of that **bundling** and **minification** process:
taking the source code you wrote, along with any external JavaScript libraries
your code depends on, and squishing it as small as possible.

**2.** Add static routes to Flask:

If you check `app.py`, you will see that the following additions have been made
since you last saw the bird API:

```py
app = Flask(
    __name__,
    static_url_path='',
    static_folder='../client/build',
    template_folder='../client/build'
)

...

@app.errorhandler(404)
def not_found(e):
    return render_template("index.html")

```

These configure our Flask app for where to search for static and template files-
both in our `client/build/` directory.

We also set up a catch-all here for any route that doesn't match those already defined on the server. This means when Flask receives a request,it will render the index.html that was generated to run the client application. The client still handles its own routing
through clicks and form submissions, but with this configuration, Flask can find the resources by URL as well. This is important for when people refresh the page, or visit your site, either manually, from bookmarks, or an external link.

> **NOTE: Often, you may be setting up RESTful client-side routes, allowing people to go to `/birds` or `/birds/:id` to see all of the birds, or one at a time, respectively. These routes wouldn't be accessible on the frontend if they're already set up on the server (like they are in this app). To solve this, it's common to rewrite the backend routes so they all start with `/api/`, like `/api/birds` and `/api/birds/<int:id>` in order to free up the non-api urls to be used for client side routing. Just remember to also update your fetches to match backend urls.**

**3.** Run the Flask server:

```console
$ gunicorn --chdir server app:app
```

Visit [http://localhost:8000](http://localhost:8000) in the browser. You should
see the production version of the React application!

Explore the React app in the browser using the React dev tools. What differences
do you see between this version of the app and what you're used to when running
in development mode?

Now you've seen how to build a production version of the React application
locally, and some of the differences between this version and the development
version you're more familiar with.

Now that you've seen how to create a production version of our React app
locally and integrated it with Flask, let's talk about
how to deploy the application to Render.

---

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
PYTHON_VERSION="your python version"
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




