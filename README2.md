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

# Next up!

## after this point we should have forked this repo and updated our .env with the appropiate DATABASE URL

- These steps will make a static version of our project that will be ready for deployment and also ready to run locally using our 'honcho' command

- first, we want to make sure our requirements.txt is up to date with our pipfile
```console
$ pipenv requirements > requirements.txt
```

- second, we want to build the production version of our React app, this will create a static version that lives in our client side under dist:

```console
$ npm run build --prefix client
```

- third, add or make sure our static routes have been added to flask, flask static routes go in the config

```py
app = Flask(
    __name__,
    static_url_path='',
    static_folder='../client/build',
    template_folder='../client/build'
)
```
- above code for create-react-app and below code for vite

```py
app = Flask(
    __name__,
    static_url_path='',
    static_folder='../client/dist',
    template_folder='../client/dist'
)
```

- fourth, add either of the below routes to the bottom of our app.py, this will set up an index page at / to show all of the site's static files.

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

- fourth, Lets make sure our 'Procfile.dev' is created and correct:

```
web: PORT=4000 npm start --prefix client
api: gunicorn -b 127.0.0.1:5555 --chdir ./server app:app
```
- above code for create-react-app and below code for vite
```
web: npm run dev --prefix client
api: gunicorn -b 127.0.0.1:5000 --chdir ./server app:app
```

- fifth, push the code to github (which will trigger a new update of our deployed project) or run below code to run it locally:

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