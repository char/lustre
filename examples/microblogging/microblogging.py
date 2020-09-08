# This is a microblogging application written with the Lustre web framework,
# but it also serves as a literate 'Learn Lustre in Y minutes' document.

# Real applications will not be written as one file, you can view one of the other examples
# to get a sense of how to structure a multi-file project.

from lustre import Lustre

app = Lustre()  # An application in Lustre is an instance of Lustre
app.debug = True  # Debug mode shows error traces an exception is raised.

# We need a database to provide user registration and login.
# If we use SQLite for the database, the 'aiosqlite' module is required.
# Lustre supports PostgreSQL and MySQL as well, with their respective requisite modules.
from lustre.database import DatabaseURL

DATABASE_URL = app.config(
    "DATABASE_URL", default="sqlite:///db.sqlite", cast=DatabaseURL
)

app.setup_database(DATABASE_URL)


# Next, we set up sessions -- Sessions in Lustre are just signed data stored on the client,
# meaning that we can do cool things like trustable stateful authentication tokens.
# Keep in mind that sessions are trivially client-readable, but not client-changable.
from lustre.config import Secret

SESSION_SECRET_KEY = app.config("SESSION_SECRET_KEY", cast=Secret)
app.setup_sessions(str(SESSION_SECRET_KEY))


# Database access is made very simple in Lustre using encode.io's orm module.
# This lets us express complex database relations and constraints as Python classes,
# and fetch them asynchronously using a query DSL.
import orm

# For our microblogging application, we just need 'Users' and 'Posts',
# so let's create them now:

# Lustre has a featureful built-in authentication system,
# using stateful authentication tokens under-the-hood so as to only
# hit the database when it is necessary.
from lustre.auth import AuthUser

# The setup_auth decorator initialises the authentication subsystem
# using an auth object type. The auth object type must inherit from AuthObject
@app.setup_auth
class User(app.db.Model, AuthUser):
    __tablename__ = "users"

    id = orm.Integer(primary_key=True)
    username = orm.String(max_length=16, unique=True)
    password_hash = orm.String(max_length=60)

    @property
    def display_name(self):
        return self.username

    @classmethod
    def create_from_token(cls, token: str):
        user = User(username=token)
        return user

    async def full(self):
        full_user = await User.objects.get(username=self.username)
        return full_user

    @classmethod
    def display_name_from_token(cls, token):
        return token

    def to_token(self):
        return self.username


class Post(app.db.Model):
    __tablename__ = "posts"

    id = orm.Integer(primary_key=True)
    author = orm.ForeignKey(User)
    timestamp = orm.DateTime()
    content = orm.Text()

    @property
    def post_time(self):
        from datetime import datetime

        return datetime.strptime(self.timestamp, "%Y-%m-%d %H:%M:%S.%f")


# HTML minification is a first-class feature of Lustre,
# but it requires the 'htmlmin' package.
#
# Responses from endpoint handlers with the MIME type text/html
# are rewritten to minify the content.
from lustre.minification import setup_html_minification

setup_html_minification()

# In order to serve the CSS, we can just add a static folder.
#
# You can also pass in html=true to add_static_folder for it to
# automatically find index.html files and the like.
app.add_static_folder("static")  # Same as add_static_folder("static", "/static")


# We come to the meat of the application: The endpoints! Rendering Jinja2 templates is simple:
from lustre import Request, render_template, redirect


# For the main page, we want to show the latest 20 posts to any logged in users.
# Since the ORM we're using is so new, we drop into a raw SQL query to use 'ORDER BY'
# but can easily escape-hatch back out to our ORM objects:
@app.route("/")
async def main_page(request: Request):
    context = {}
    if request.user.is_authenticated:
        context["posts"] = []

        users, posts = User.__tablename__, Post.__tablename__

        query = f"""SELECT * FROM {posts}
        INNER JOIN {users} ON {users}.id = {posts}.author
        ORDER BY timestamp DESC LIMIT 20"""

        results = await app.db.database.fetch_all(query)
        context["posts"] = [
            Post.from_row(r, select_related=["author"]) for r in results
        ]

    return render_template("main_page.html.j2", context)


# Brace syntax is used for path parameters, and accessed through the request object.
# Parameters can also have types like /u/{path_to_file:path} or /num/{n:float}.
@app.route("/@{username}")
async def user_feed(request: Request):
    username = request.path_params["username"]

    users, posts = User.__tablename__, Post.__tablename__
    query = f"""SELECT * FROM {posts}
    INNER JOIN {users} ON {users}.id = {posts}.author
    WHERE {users}.username = :username
    ORDER BY timestamp DESC LIMIT 20"""
    results = await app.db.database.fetch_all(query, values={"username": username})
    posts = [Post.from_row(r, select_related=["author"]) for r in results]

    return render_template("user_feed.html.j2", {"posts": posts, "username": username})


# Flashes in Lustre are like Flask: You give it a category and a message,
# and the information shows up on the next page navigated to by the user.
# See templates/_flashes.html.j2 for rendering.
# from lustre import flash
def flash(*args):
    pass


# Since we will soon be logging in, it's best to support logging out first:
@app.route("/logout/")
def logout_page(request: Request):
    if not request.user.is_authenticated:
        return redirect("/")

    return render_template("logout.html.j2")


@app.route("/logout", methods=["POST"])
def logout_handler(request: Request):
    app.auth.log_out()
    flash("success", "Logged out.")
    return redirect("/")


# And we can also use Lustre's form subsystem to render HTML forms
# and automatically validate their data when receiving it:
import lustre.forms as form
from lustre import render_form

# The simplest form in our application will be the single-text-field post submission:
class SendPostForm(form.Schema):
    content = form.Text(title="Content")


@app.route("/send_post", methods=["POST"])
async def send_post(request: Request):
    from datetime import datetime

    if not request.user.is_authenticated:
        return redirect("/login/")

    form_data = await request.form()
    send_post_form = SendPostForm.validate(form_data)

    post = await Post.objects.create(
        author=await request.user.full(),
        content=send_post_form.content,
        timestamp=datetime.now(),
    )

    return redirect(f"/")


# Here, we set up the login form as just a username and a password.
class LoginForm(form.Schema):
    username = form.String(title="Username")
    password = form.String(title="Password", format="password")


# Lustre also
@app.form_renderer(LoginForm, "/login/")
def login_form_renderer(request: Request, values: dict, errors: dict):
    return render_template(
        "login.html.j2",
        {"login_form": render_form(LoginForm, values=values, errors=errors)},
    )


@app.form_handler(LoginForm, "/login", methods=["POST"])
async def login_form_handler(request: Request, login_form: LoginForm):
    from bcrypt import checkpw

    try:
        user = await User.objects.get(username=login_form.username)
    except (orm.NoMatch, orm.MultipleMatches):
        flash("failure", "No matching user was found.")
        return None

    password_bytes = login_form.password.encode("utf-8")
    password_hash_bytes = user.password_hash.encode("utf-8")

    if not checkpw(password_bytes, password_hash_bytes):
        # Having a different message allows for user enumeration here, but it's okay.
        flash("failure", "The given password is incorrect.")
        return None

    flash("success", "Logged in.")
    app.auth.log_in(user)
    return redirect("/")


# It's really simple to do the exact same thing for registration,
# but we also define a regex for what a valid username can look like:
class RegisterForm(form.Schema):
    import re

    username = form.String(
        title="Username",
        min_length=3,
        max_length=16,
        pattern=re.compile(r"[a-zA-Z0-9\-]{1,16}"),
    )

    password = form.String(
        title="Password",
        min_length=8,
        max_length=72,
        format="password",
    )

    confirm_password = form.String(
        title="Confirm Password",
        min_length=8,
        max_length=72,
        format="password",
    )


@app.form_renderer(RegisterForm, "/register/")
def register_form(request: Request, values: dict, errors: dict):
    return render_template(
        "register.html.j2",
        {"register_form": render_form(RegisterForm, values=values, errors=errors)},
    )


@app.form_handler(RegisterForm, "/register", methods=["POST"])
async def register(request: Request, register_form: RegisterForm):
    from bcrypt import hashpw, gensalt

    if register_form.confirm_password != register_form.password:
        flash("error", "'Confirm Password' must match 'Password'!")
        return None

    password_bytes = register_form.password.encode("utf-8")
    password_hash = hashpw(password_bytes, gensalt(12)).decode("utf-8")

    user = await User.objects.create(
        username=register_form.username, password_hash=password_hash
    )
    app.auth.log_in(user)
    flash("success", "Successfully registered.")

    return redirect("/")
