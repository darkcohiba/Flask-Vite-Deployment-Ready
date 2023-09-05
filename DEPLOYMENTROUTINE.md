# Steps to deploy!

- first, we want to make sure our requirements.txt is up to date with our pipfile
```console
$ pipenv requirements > requirements.txt
```

- second, we want to build the production version of our React app:

```console
$ npm run build --prefix client
```

- third, add or check if our static routes have been added to flask, flask static routes go in the config while the errorhandler goes inside the app.py
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

- fourth, run the Flask server:

```console
$ gunicorn --chdir server app:app
```

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


we had to remove the vite proxy because it only runs during development, code below:

proxy: {
      "/api":{
        // we can adjust the target based on our backend port
        target: "http://127.0.0.1:8000",
        changeOrigin:true,
        secure: false,
        rewrite: (path)=>path.replace(/^\/api/,"")
      }
    }